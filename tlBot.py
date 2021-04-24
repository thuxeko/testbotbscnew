# Lib
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import logging
import time

# Config
from tlConfig.credentials import bot_token, URL, typeGroup

# Include
import checkbsc
import utils

TOKEN = bot_token
# PORT = int(os.environ.get('PORT', 8443))
bot = Bot(TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def getToken(update: Update, context: CallbackContext) -> None:
    token = update.message.text.replace('/p', '').strip()
    if token:
        try:
            strOut = checkbsc.getTokenWithSymbol(
                token, 1, update.message.from_user['first_name'], update.message.from_user['id'])

            mesoutbybot = bot.send_message(chat_id=update.effective_message.chat_id,
                                           text=strOut, parse_mode='HTML')
            print(update.message)
            update.message.delete()
            typeChat = mesoutbybot['chat']['supergroup']
            if typeChat == typeGroup:
                cvTime = int(time.mktime(mesoutbybot.date.timetuple()))
                utils.updateChat(
                    mesoutbybot['message_id'], mesoutbybot['chat']['id'], cvTime)

            
        except Exception as e:
            print(e)

    else:
        update.message.reply_text("Sai câu lệnh")


def getContract(update: Update, context: CallbackContext) -> None:
    token = update.message.text.replace('/ct', '').strip()
    if token:
        strOut = checkbsc.getTokenWithSymbol(
            token, 2, update.message.from_user['first_name'], update.message.from_user['id'])
        update.message.reply_text(strOut)
        update.message.delete()
    else:
        update.message.reply_text("Sai câu lệnh")


def infoBot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Em chào anh, nhà em 3 đời làm bot 🤖, hiện tại bot này nhà em có: \n/p - Nhập mã Token để lấy thông tin \n/ct - Nhập mã Token để lấy Contract\n/info - Gọi em ra để dooddeed nè')


def error(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main():
    try:
        """Start the bot."""
        updater = Updater(TOKEN, use_context=True)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("p", getToken))
        dp.add_handler(CommandHandler("ct", getContract))
        dp.add_handler(CommandHandler("info", infoBot))

        # Log error
        dp.add_error_handler(error)

        # Webhook start bot
        updater.start_webhook(listen="0.0.0.0",
                              port=8443,
                              url_path=TOKEN,
                              key='private.key',
                              cert='cert.pem',
                              webhook_url=URL + TOKEN)
        updater.idle()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()