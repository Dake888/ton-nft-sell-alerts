import requests
import json

from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
from tonsdk.utils import from_nano, to_nano, b64str_to_bytes
from ton.utils import read_address
from tonsdk.boc import Cell

from config import cmc_url, cmc_params, cmc_headers, tonorg_price_url, markets, markets_links, td_collections


async def parse_sale_stack(stack):
    if stack[0][1] == '0x415543':
        return parse_auction_stack(stack)
    action = 'SaleFixPrice'
    is_complete = bool(int(stack[1][1], 16))
    created_at = int(stack[2][1], 16)
    marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).to_string(True, True, True)
    nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes']))).to_string(True, True, True)
    try:
        nft_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[5][1]['bytes']))).to_string(True, True, True)
    except:
        nft_owner_address = None
    full_price = from_nano(int(stack[6][1], 16), 'ton')

    return action, is_complete, created_at, marketplace_address, nft_address, nft_owner_address, full_price


async def parse_auction_stack(stack):
    action = 'SaleAuction'
    is_end = bool(int(stack[1][1], 16))
    created_at = int(stack[17][1], 16)
    marketplace_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[3][1]['bytes']))).to_string(True, True, True)
    nft_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[4][1]['bytes']))).to_string(True, True, True)
    nft_owner_address = read_address(Cell.one_from_boc(b64str_to_bytes(stack[5][1]['bytes']))).to_string(True, True, True)
    min_bid = from_nano(int(stack[16][1], 16), 'ton')
    max_bid = from_nano(int(stack[15][1], 16), 'ton')
    min_step = from_nano(int(stack[8][1], 16), 'ton')
    last_bid_at = int(stack[18][1], 16)
    last_member = read_address(Cell.one_from_boc(b64str_to_bytes(stack[7][1]['bytes'])))
    if last_member is not None:
        last_member = last_member.to_string(True, True, True)
    last_bid = from_nano(int(stack[6][1], 16), 'ton')
    is_canceled = bool(int(stack[19][1], 16))
    end_time = int(stack[2][1], 16)

    return action, is_end, created_at, marketplace_address, nft_address, nft_owner_address, min_bid, max_bid, \
        min_step, last_bid_at, last_member, last_bid, is_canceled, end_time


async def convert_ton_to_usd_old(ton):
    try:
        usd = json.loads(requests.get(tonorg_price_url).text)['the-open-network']['usd']
        usd_price = round(float(ton) * usd, 2)
        return usd_price

    except Exception as e:
        print(f'Error in Get ton usd price (OLD_version). Check the logs:\n{e})')


async def convert_ton_to_usd(ton):
    try:
        session = requests.Session()
        session.headers.update(cmc_headers)

        usd = json.loads(session.get(cmc_url, params=cmc_params).text)['data']['11419']['quote']['USD']['price']
        usd_price = round(float(ton) * usd, 2)

        return usd_price

    except Exception as e:
        print(f'Error in Get ton usd price. Check the logs:\n{e}')
        print(f'Try to convert with OLD method...')
        await convert_ton_to_usd_old(ton)


async def keyboard_buttons(price_ton, nft_address, col_address, sale_contract_address, market_address):
    price_nanoton = to_nano(price_ton, 'ton')

    if markets[market_address] == 'Getgems' and col_address in td_collections:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Getgems', url=markets_links['Getgems'] + nft_address),
             InlineKeyboardButton(text='Diamonds', url=markets_links['Diamonds'] + nft_address)],
            [InlineKeyboardButton(text='Купить через Tonkeeper',
                                  url=f'https://app.tonkeeper.com/transfer/{sale_contract_address}?amount={price_nanoton}')],
        ])
    elif markets[market_address] == 'Getgems':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Getgems', url=markets_links['Getgems'] + nft_address)],
            [InlineKeyboardButton(text='Купить через Tonkeeper',
                                  url=f'https://app.tonkeeper.com/transfer/{sale_contract_address}?amount={price_nanoton}')],
        ])
    elif markets[market_address] == 'Tonex':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Tonex', url=markets_links['Tonex'] + nft_address),
             InlineKeyboardButton(text='Getgems', url=markets_links['Getgems'] + nft_address)],
        ])
    elif markets[market_address] == 'Disintar':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Disintar', url=markets_links['Disintar'] + nft_address),
             InlineKeyboardButton(text='Getgems', url=markets_links['Getgems'] + nft_address)],
            [InlineKeyboardButton(text='Купить через Tonkeeper',
                                  url=f'https://app.tonkeeper.com/transfer/{sale_contract_address}?amount={price_nanoton}')],
        ])
    elif markets[market_address] == 'Diamonds':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Diamonds', url=markets_links['Diamonds'] + nft_address),
             InlineKeyboardButton(text='Getgems', url=markets_links['Getgems'] + nft_address)],
            [InlineKeyboardButton(text='Купить через Tonkeeper',
                                  url=f'https://app.tonkeeper.com/transfer/{sale_contract_address}?amount={price_nanoton}')],
        ])

    return keyboard