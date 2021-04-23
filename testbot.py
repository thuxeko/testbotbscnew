from telegram import *
from telegram.ext import *

bot = Bot("1574629803:AAE8FgoEOn4IidjdbkLT_lZOKscr1UGLhIo")
updater = Updater("1574629803:AAE8FgoEOn4IidjdbkLT_lZOKscr1UGLhIo", use_context=True)

dispatcher = updater.dispatcher

def getToken(update: Update, context: CallbackContext) -> None:
    userMes = '[{username}](tg://user?id={id_user}) \nTest'.format(
        username=update.message.from_user['first_name'], id_user=update.message.from_user['id'])
    
    bot.send_message(chat_id=update.effective_message.chat_id,
                     text=userMes, parse_mode='MarkdownV2')
    
    update.message.delete()

dispatcher.add_handler(CommandHandler("p", getToken))

updater.start_polling()