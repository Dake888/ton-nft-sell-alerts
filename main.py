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
    try:
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

    except Exception as e:
        print(f'Error in Get pytonlib client. Check the logs:\n{e})')


async def markets_tr(market):
    try:
        utimes = list()
        last_utime = int(open(f'{current_path}/lastUtime', 'r').read())

        client = await get_client()

        trs = json.loads(requests.get(f'{toncenter_url}getTransactions',
                                      params={'address': market,
                                              'limit': 50,
                                              'to_lt': 0,
                                              'archival': 'false',
                                              'api_key': toncenter_token}).text)['result']

        for tr in trs[::-1]:
            if tr['utime'] <= last_utime or len(tr['out_msgs']) == 0:
                continue

            address = tr['out_msgs'][0]['destination']

            try:
                response = await client.raw_run_method(address=address,
                                                       method='get_sale_data',
                                                       stack_data=[])

            except Exception as e:
                print(f'Error in Get sale data. Some problems with ({address}) NFT-sale contract. Check the logs:\n{e}')
                await client.close()
                continue

            if response is not None and response['exit_code'] == 0:
                sale_contract_data = await parse_sale_stack(response['stack'])

                if sale_contract_data is not None and not sale_contract_data[1]:
                    sale_nft_data = await get_nft_data(sale_contract_data[4])

                    if sale_nft_data is not None and sale_nft_data[0] in collections_list:
                        collection_floor_data = await get_collection_floor(sale_nft_data[0])

                        if sale_contract_data[0] == 'SaleFixPrice':
                            tg_message(sale_contract_data[0], sale_contract_data[3], sale_contract_data[4],
                                       sale_nft_data[0], address, sale_contract_data[5], sale_contract_data[6],
                                       sale_nft_data[3], sale_nft_data[2], collection_floor_data[0],
                                       collection_floor_data[1], None, None, None)

                        elif sale_contract_data[0] == 'SaleAuction':
                            tg_message(sale_contract_data[0], sale_contract_data[3], sale_contract_data[4],
                                       sale_nft_data[0], address, sale_contract_data[5], sale_contract_data[6],
                                       sale_nft_data[3], sale_nft_data[2], collection_floor_data[0],
                                       collection_floor_data[1], sale_contract_data[7], sale_contract_data[8],
                                       sale_contract_data[13])

                        else:
                            pass

                        utimes.append(tr['utime'])

        await client.close()

        try:
            return utimes[-1]
        except Exception as e:
            pass

    except Exception as e:
        print(f'Error in markets_tr. Check the logs:\n{e}')


async def scheduler():
    while True:
        utimes = await asyncio.gather(*map(markets_tr, markets_list))
        utimes = list(filter(None, utimes))
        try:
            if len(utimes) > 0:
                open(f'{current_path}/lastUtime', 'w').write(str(max(utimes)))
        except Exception as e:
            print(f'Error in Scheduler:\n{e}')

        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(scheduler())
