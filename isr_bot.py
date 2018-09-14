import logging
from telegram.ext import MessageHandler, Filters, CommandHandler, Updater
from telegram import Bot
import telepot
import requests
import json
import datetime

# Token
Token = '643187363:AAESdh4f8Anyc90VsSD_HHBE7sb13-fFS2E'
ChatID = "@insureum"

# Create bot object
bot = telepot.Bot(Token)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		    level = logging.INFO)

logger = logging.getLogger(__name__)

# ISRETH ticker price
url = "http://api.coinbene.com/v1/market/ticker"
eth_params = {"symbol":"ISRETH"}
btc_params = {"symbol":"ISRBTC"}

# Define command handlers. Takes arguments bot and update. Error handlers recieve raised TelegramError object in error
# def start(bot,update):
#     # Sends message when command /start is issued
#     update.message.reply_text("Started")
# 
def help(bot,update):
    # Sends message when command /help is issued
    update.message.reply_text('List of commands:\n/ethprice\n/btcprice')

# def echo(bot,update):
#    # Echos user message
#    update.message.reply_text(update.message.text)

def error(bot,update,error):
    # Log errors caused by updates
    logger.warning('Update "%s" caused error "%s"', update, error)

def ethprice(bot,update):
    r = requests.get(url,eth_params).content.decode("utf-8")
    d = json.loads(r)
    ts = d.get('timestamp')
    dt = datetime.datetime.fromtimestamp(ts/1e3).strftime("%Y-%m-%d %H:%M:%S")
    ethisr = d.get('ticker')[0]
    last_ethisr = ethisr['last']
    msg = "Latest ISR/ETH = " + last_ethisr + " ETH\nLast Updated: " + dt
    update.message.reply_text(msg)

def btcprice(bot,update):
    r = requests.get(url,btc_params).content.decode("utf-8")
    d = json.loads(r)
    ts = d.get('timestamp')
    dt = datetime.datetime.fromtimestamp(ts/1e3).strftime("%Y-%m-%d %H:%M:%S")
    btcisr = d.get('ticker')[0]
    last_btcisr = btcisr['last']
    msg = "Latest ISR/BTC = " + last_btcisr + " BTC\nLast Updated: " + dt
    update.message.reply_text(msg)

# def usdprice(bot,update):
#     r = requests.get(url,parameters).content.decode("utf-8")
#     d = json.loads(r)
#     isr = d.get('ticker')[0]
#     last = isr['last']
#     msg = "Latest ISR/ETH = " + last + " ETH"
#     update.message.reply_text(msg)
# 
# def krwprice(bot,update):
#     r = requests.get(url,parameters).content.decode("utf-8")
#     d = json.loads(r)
#     isr = d.get('ticker')[0]
#     last = isr['last']
#     msg = "Latest ISR/ETH = " + last + " ETH"
#     update.message.reply_text(msg)
 
# Start Bot
def main():
    # Create EventHandler and pass to bot's token
    updater = Updater(Token)
    
    # Get dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ethprice", ethprice))
    dp.add_handler(CommandHandler("btcprice", btcprice))

    # on noncommand i.e. message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run bot until <C-c> is pressed
    updater.idle()

if __name__ == '__main__':
    main()
