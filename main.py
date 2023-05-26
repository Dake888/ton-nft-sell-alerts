import requests
import json
import asyncio

from pathlib import Path

from pytonlib import TonlibClient

from nftData import get_nft_data, get_collection_floor
from functions import parse_sale_stack
from tgMessage import tg_message
from config import current_path, ton_config_url, toncenter_url, toncenter_token, markets_list, collections_list


async def get_client():
    config = requests.get(ton_config_url).json()
    keystore_dir = '/tmp/ton_keystore'
    Path(keystore_dir).mkdir(parents=True,
                             exist_ok=True)

    client = TonlibClient(ls_index=2,
                          config=config,
                          keystore=keystore_dir,
                          tonlib_timeout=10)
    await client.init()

    return client


async def markets_tr(market):
    utimes = list()
    last_utime = int(open(f'{current_path}/lastUtime', 'r').read())

    client = await get_client()

    trs = json.loads(requests.get(f'{toncenter_url}getTransactions',
                                  params={'address': market,
                                          'limit': 100,
                                          'to_lt': 0,
                                          'archival': 'false',
                                          'api_key': toncenter_token}).text)['result']

    for tr in trs[::-1]:
        if tr['utime'] <= last_utime or len(tr['out_msgs']) == 0:
            continue

        response = await client.raw_run_method(address=tr['out_msgs'][0]['destination'],
                                               method='get_sale_data',
                                               stack_data=[])

        if response['exit_code'] == 0:
            sale_contract_data = parse_sale_stack(response['stack'])

            if not sale_contract_data[1]:
                sale_nft_data = get_nft_data(sale_contract_data[4])

                if sale_nft_data[0] in collections_list:
                    collection_floor_data = get_collection_floor(sale_nft_data[0])

                    if sale_contract_data[0] == 'SaleFixPrice':
                        tg_message(sale_contract_data[0], sale_contract_data[3], sale_contract_data[4],
                                   sale_contract_data[5], sale_contract_data[6], sale_nft_data[3],
                                   sale_nft_data[2], collection_floor_data[0], collection_floor_data[1],
                                   None, None, None)

                    elif sale_contract_data[0] == 'SaleAuction':
                        tg_message(sale_contract_data[0], sale_contract_data[3], sale_contract_data[4],
                                   sale_contract_data[5], sale_contract_data[6], sale_nft_data[3], sale_nft_data[2],
                                   collection_floor_data[0], collection_floor_data[1], sale_contract_data[7],
                                   sale_contract_data[8], sale_contract_data[13])

                    else:
                        pass

                    utimes.append(tr['utime'])

    await client.close()

    try:
        return utimes[-1]
    except:
        pass


async def scheduler():
    while True:
        utimes = await asyncio.gather(*map(markets_tr, markets_list))
        utimes = list(filter(None, utimes))
        try:
            if len(utimes) > 0:
                open(f'{current_path}/lastUtime', 'w').write(str(max(utimes)))
        except:
            pass

        await asyncio.sleep(20)


if __name__ == '__main__':
    asyncio.run(scheduler())
