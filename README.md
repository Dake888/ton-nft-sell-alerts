# ton-nft-sell-alerts
A simple bot for tracking the putting up for sale of the NFT from collections you are interested in on TON blockchain.

_**The bot will be useful for those who want to set up monitoring of NFT put up for sale at a fixed price or as part of an auction.
Information about the NFT available for purchase will be sent to your Telegram group.**_

The bot processes addresses that interact with sales contracts asynchronously.
The code uses public modules for TON: [pytonlib by toncenter](https://github.com/toncenter/pytonlib), [pytonlib by psylopunk](https://github.com/psylopunk/pytonlib), [tonsdk](https://github.com/tonfactory/tonsdk).

## Quick start

Before you start working with the bot, you should make sure that all modules from **requirements.txt** installed in your environment.
An easy way to quickly install all requirements: `pip install -r /path/to/requirements.txt`

You will also need to fill out a **secretData.py** with your token data.
```
tonapi_token = ''
toncenter_token = ''
bot_token = ''
cmc_token = ''
```

### Configure your parameters in the config.py:
1. **Fill in the id of your Telegram group.** _Please note that the bot, the token from which you specified earlier, must have access to the publication of messages in target group.
2. **Select the addresses of marketplaces to track by changing the markets_list.** _Please note that some marketplaces create contracts that don't comply with TON NFT standards, so there may be some problems with data processing (for example, Disintar)._
3. **Select the addresses of NFT collections to track by changing the collections_list.**

You can change the time cutoff data at any time by changing the number in lastUtime to the date and time you need in unix format.

Was the bot helpful to you? I am very happy, if it is ^^
For donations - EQC7QQ4yZGuNr-qJYOcg-w8hP7EdF29rok-d84fXTKRuUq0-
