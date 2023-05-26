from datetime import datetime

from functions import convert_ton_to_usd
from config import bot, notify_chat, markets, markets_links, getgems_user_url


def tg_message(action, market_address, nft_address, real_owner, price_ton, nft_name,
               nft_preview, floor_ton, floor_link, max_bid, min_step, end_time):

    emoji = '💎'
    tag = ''
    market_name = markets[market_address]
    market_link = markets_links[market_name]

    price_usd = convert_ton_to_usd(price_ton)

    if price_usd is not None:
        price_usd_text = f' (${price_usd})'

    else:
        price_usd_text = ''

    if floor_ton is not None:
        floor_usd = convert_ton_to_usd(floor_ton)

        if floor_usd is not None:
            floor_usd_text = f' (${floor_usd})'

        else:
            floor_usd_text = ''

        floor_text = f'🔽 <b>Current <a href="{market_link}{floor_link}">floor</a>:</b> {floor_ton} TON{floor_usd_text}'

        if price_ton <= float(floor_ton) * 1.1:
            emoji = '🔥'
            tag = '#HotPrice'

        elif price_ton >= floor_ton * 2:
            emoji = '🔝'
            tag = '#UpTheFloor'

    else:
        floor_text = ''
        
    if action == 'SaleFixPrice':
        action_message = f'{emoji} On sale for <b>{price_ton} TON{price_usd_text} on {market_name}</b>\n\n'
        action_tag = 'Sale'

    else:
        end_time = datetime.utcfromtimestamp(end_time).strftime('%d.%m.%Y %H:%M:%S')

        if max_bid == 0:
            max_bid_text = ''

        else:
            max_bid_usd = convert_ton_to_usd(max_bid)

            if max_bid_usd is not None:
                max_bid_usd_text = f' (${max_bid_usd})'

            else:
                max_bid_usd_text = ''

            max_bid_text = f'Max bid: {max_bid} TON{max_bid_usd_text}\n'

        if min_step < 0.1:
            min_step_text = ''

        else:
            min_step_text = f'Min step: {min_step}\n'

        action_message = f'The auction started with an <b>initial price of {price_ton} TON{price_usd_text} ' \
                         f'on {market_name}</b>\n\n' \
                         f'<i><b>Auction params:</b>\n' \
                         f'{max_bid_text}' \
                         f'{min_step_text}' \
                         f'Will end on: {end_time}</i>\n\n'
        action_tag = 'Auction'

    if real_owner is not None:
        seller_text = f'🛒 <b><i><a href="{getgems_user_url}{real_owner}">Link</a> to the sellers Getgems</i></b>\n\n'
    else:
        seller_text = ''

    message_text = f'🖼 <b><a href="{market_link}{nft_address}">{nft_name}</a></b>\n\n' \
                   f'{action_message}' \
                   f'{floor_text}\n\n' \
                   f'{seller_text}' \
                   f'<b>#{action_tag} #On{market_name} {tag}</b>'

    try:
        bot.sendPhoto(notify_chat, photo=nft_preview, caption=message_text, parse_mode='HTML')
    except Exception as e:
        print(f'Photo Send ({notify_chat}) - ({nft_address}) Failed: {e}')
        try:
            bot.sendMessage(notify_chat, message_text, parse_mode='HTML', disable_web_page_preview=True)
        except Exception as e:
            print(f'Message Send ({notify_chat}) - ({nft_address}) Failed: {e}')
