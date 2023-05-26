import json
import requests

from pytonlib.utils import address
from tonsdk.utils import from_nano

from config import tonapi_url, tonapi_header, getgems_api_url, getgems_query


async def get_nft_data(nft_address):
    try:
        response = json.loads(requests.get(f'{tonapi_url}nft/getItems',
                                           params={'addresses': nft_address},
                                           headers=tonapi_header).text)['nft_items'][0]
        if 'collection' in response:
            collection_address = address.detect_address(response['collection']['address'])['bounceable']['b64url']
            collection_name = response['collection']['name']
        if 'previews' in response:
            preview_link = response['previews'][2]['url']
        if response['metadata'] != {}:
            nft_name = response['metadata']['name']
            if 'animation_url' in response['metadata']:
                image_link = response['metadata']['animation_url']
                preview_link = image_link
            else:
                image_link = response['metadata']['image']
            if 'attributes' in response['metadata']:
                nft_attributes = response['metadata']['attributes']

        return collection_address, collection_name, preview_link, nft_name, image_link, nft_attributes

    except Exception as e:
        print(f'Error in Get NFT data. Some problems with ({nft_address}) NFT. Check the logs:\n{e}')


async def get_collection_floor(col_address):
    try:
        json_data = {'operationName': 'nftSearch',
                     'query': getgems_query,
                     'variables': {
                         'count': 30,
                         'query': '{"$and":[{"collectionAddress":"' + col_address + '"}]}',
                         'sort': '[{"isOnSale":{"order":"desc"}},{"price":{"order":"asc"}},{"index":{"order":"asc"}}]'}
                     }

        data = json.loads(requests.post(getgems_api_url,
                                        json=json_data).text)['data']['alphaNftItemSearch']['edges']

        for item in data:
            if 'fullPrice' not in item['node']['sale']:
                continue

            floor_price = from_nano(int(item['node']['sale']['fullPrice']), 'ton')
            floor_link = item['node']['address']
            
            return floor_price, floor_link

    except Exception as e:
        print(f'Error in Get collection floor data. Some problems with ({col_address}) collection. Check the logs:\n{e}')
