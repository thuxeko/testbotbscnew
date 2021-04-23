# Lib
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import logging

#Config
from tlConfig.credentials import bot_token, URL

#Include
import checkbsc

TOKEN = bot_token
PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def getToken(update: Update, context: CallbackContext) -> None:
    # token = update.message.text.replace('/p','').strip()
    # if token:
    #     strOut = checkbsc.getTokenWithSymbol(token, 1)
    #     update.message.reply_html(strOut)
    #     update.message.delete()
    # else:
    #     update.message.reply_text("Sai câu lệnh")
    print(update.message)
    print(update.message.from_user['id'])
    id_user = update.message.from_user['id']
    
    url_delete = '[Thu](tg://user?id={userid}) \nTest'.format(userid = id_user)
    update.message.reply_text(url_delete)
    # update.message.delete()

def getContract(update: Update, context: CallbackContext) -> None:
    token = update.message.text.replace('/ct','').strip()
    if token:
        strOut = checkbsc.getTokenWithSymbol(token, 2)
        update.message.reply_text(strOut)
        update.message.delete()
    else:
        update.message.reply_text("Sai câu lệnh")

def infoBot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Em chào anh, nhà em 3 đời làm bot 🤖, hiện tại bot này nhà em có: \n/p - Nhập mã Token để lấy thông tin \n/ct - Nhập mã Token để lấy Contract\n/info - Gọi em ra để dooddeed nè')

def error(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def main():
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
                          port=PORT,
                          url_path=TOKEN)

    updater.bot.set_webhook(URL + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()