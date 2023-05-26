import pathlib
import telepot

from secretData import *

current_path = pathlib.Path(__file__).parent.resolve()
bot = telepot.Bot(bot_token)


toncenter_url = 'https://toncenter.com/api/v2/'
tonapi_url = 'https://tonapi.io/v1/'
getgems_api_url = 'https://api.getgems.io/graphql'
getgems_user_url = 'https://getgems.io/user/'
ton_config_url = 'https://ton.org/global-config.json'
cmc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
tonorg_price_url = 'https://ton.org/getpriceg/'

notify_chat = ''

markets_list = [
                #'EQBYTuYbLf8INxFtD8tQeNk5ZLy-nAX9ahQbG_yl1qQ-GEMS',  # Getgems Sales
                #'EQCjc483caXMwWw2kwl2afFquAPO0LX1VyZbnZUs3toMYkk9',  # Getgems Auction
                #'EQCgRvXbOJeFSRKnEg1D-i0SqDMlaNVGvpSSKCzDQU_wDAR4',  # Tonex
                #'EQAezbdnLVsLSq8tnVVzaHxxkKpoSYBNnn1673GXWsA-Lu_w',  # TD Market
                # 'EQDrLq-X6jKZNHAScgghh0h1iog3StK71zn8dcmrOj8jPWRA',  # Disintar
                ]

markets = {
           'EQBYTuYbLf8INxFtD8tQeNk5ZLy-nAX9ahQbG_yl1qQ-GEMS': 'Getgems',
           'EQCjc483caXMwWw2kwl2afFquAPO0LX1VyZbnZUs3toMYkk9': 'Getgems',
           'EQCgRvXbOJeFSRKnEg1D-i0SqDMlaNVGvpSSKCzDQU_wDAR4': 'Tonex',
           'EQDrLq-X6jKZNHAScgghh0h1iog3StK71zn8dcmrOj8jPWRA': 'Disintar',
           'EQAezbdnLVsLSq8tnVVzaHxxkKpoSYBNnn1673GXWsA-Lu_w': 'Diamonds',
          }

markets_links = {
                 'Getgems': 'https://getgems.io/nft/',
                 'Tonex': 'https://tonex.app/nft/market/nfts/',
                 'Disintar': 'https://beta.disintar.io/object/',
                 'Diamonds': 'https://ton.diamonds/explorer/',
                }

collections_list = [
                    'EQCzuSjkgUND61l7gIH3NvVWNtZ0RX1hxz1rWnmJqGPmZh7S',  # Toned Ape Club
                    'EQDgZmQpDJbO6laHvvibaXYXMlEAYEH6LnUtA5J19W18dENp',  # G-BOTS SD
                    'EQAo92DYMokxghKcq-CkCGSk_MgXY5Fo1SPW20gkvZl75iCN',  # TON Punks
                    'EQCvYf5W36a0zQrS_wc6PMKg6JnyTcFU56NPx1PrAW63qpvt',  # Rich Cats
                    'EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir',  # TON Diamond
                    ]

td_collections = [
                  'EQAG2BH0JlmFkbMrLEnyn2bIITaOSssd4WdisE4BdFMkZbir',  # TON Diamond
                  'EQB8D8A9OoDoRmL7qVbUBrd_po9vNKcl44HCSw6b-c3nvcj9',  # Annihilation
                  'EQD7eDxP_wLX18kr8uyYfs6srlgoNMfRbXNYM8dmMXT2vxwk',  # CALLIGRAFUTURISM — 24: Units
                  'EQA63JHaG-ufF4ewKtkV-9DMGNsDSMD8SCOggBbFNGcM0C52',  # Mutant Toadz
                  'EQDgZmQpDJbO6laHvvibaXYXMlEAYEH6LnUtA5J19W18dENp',  # G-BOTS SD
                 ]

getgems_query = "query nftSearch($count: Int!, $cursor: String, $query: String, $sort: String) " \
                "{\n  alphaNftItemSearch(first: $count, after: $cursor, query: $query, sort: $sort) " \
                "{\n    edges {\n      node {\n        ...nftPreview\n        __typename\n      }" \
                "\n      cursor\n      __typename\n    }\n    info {\n      hasNextPage\n      __typename\n    }" \
                "\n    __typename\n  }\n}\n\nfragment nftPreview on NftItem {\n  name\n  previewImage: content " \
                "{\n    ... on NftContentImage {\n      image {\n        sized(width: 500, height: 500)" \
                "\n        __typename\n      }\n      __typename\n    }\n    ... on NftContentLottie " \
                "{\n      lottie\n      fallbackImage: image {\n        sized(width: 500, height: 500)" \
                "\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  address\n  collection " \
                "{\n    name\n    address\n    __typename\n  }\n  sale {\n    ... on NftSaleFixPrice " \
                "{\n      fullPrice\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"

cmc_params = {'slug': 'toncoin',
              'convert': 'USD'}

cmc_headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': cmc_token}

tonapi_header = {'Authorization': 'Bearer ' + tonapi_token}
