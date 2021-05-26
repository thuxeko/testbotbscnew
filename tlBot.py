# Lib
from telegram import Update, Bot, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import logging
import time
import json

# Include
import checkToken
import utils
import dbrun

TOKEN = dbrun.getConfig('bot_token')
URL_BOT = dbrun.getConfig('URL')
dataConfig = utils.readConfigJson()

bot = Bot(TOKEN)
timeConfig = 60

SWL = range(1)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


# region Get Token BSC
def getToken(update: Update, context: CallbackContext) -> None:
    token = update.message.text.split(' ')
    if token[1].strip():
        try:
            resinsert =  dbrun.insertToDb(update.message.to_json(), 1) # Insert user/group
            print(resinsert)

            strOut = checkToken.getTokenWithSymbol(
                token[1], 1, update.message.from_user['first_name'],
                update.message.from_user['id'], 'bsc')

            mesoutbybot = bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=strOut,
                parse_mode='HTML')

            update.message.delete()
            typeChat = mesoutbybot['chat']['type']
            if typeChat == dataConfig['typeGroup']:
                cvTime = int(time.mktime(mesoutbybot.date.timetuple()))
                utils.updateChat(mesoutbybot['message_id'],
                                 mesoutbybot['chat']['id'],
                                 (cvTime + timeConfig))
        except Exception as e:
            dbrun.writeLog('getToken', str(e))

    else:
        update.message.reply_text("Sai câu lệnh")


def getContract(update: Update, context: CallbackContext) -> None:
    try:
        token = update.message.text.split(' ')
        if token[1].strip():
            resinsert =  dbrun.insertToDb(update.message.to_json(), 1) # Insert user/group
            print(resinsert)

            strOut = checkToken.getTokenWithSymbol(
                token[1], 2, update.message.from_user['first_name'],
                update.message.from_user['id'], 'bsc')

            mesoutbybot = update.message.reply_text(strOut)

            typeChat = mesoutbybot['chat']['type']
            if typeChat == dataConfig['typeGroup']:
                cvTime = int(time.mktime(mesoutbybot.date.timetuple()))
                utils.updateChat(mesoutbybot['message_id'],
                                 mesoutbybot['chat']['id'], (cvTime + timeConfig))

                utils.updateChat(update.message.message_id,
                                 update.message.chat_id, (cvTime + timeConfig))
        else:
            update.message.reply_text("Sai câu lệnh")
    except Exception as e:
        dbrun.writeLog('getContract', str(e))
# endregion

#region Get Token ETH
def getTokenETH(update: Update, context: CallbackContext) -> None:
    token = update.message.text.split(' ')
    if token[1].strip():
        try:
            resinsert =  dbrun.insertToDb(update.message.to_json(), 1) # Insert user/group
            print(resinsert)

            strOut = checkToken.getTokenWithSymbol(
                token[1], 1, update.message.from_user['first_name'],
                update.message.from_user['id'], 'eth')

            mesoutbybot = bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=strOut,
                parse_mode='HTML')

            update.message.delete()
            typeChat = mesoutbybot['chat']['type']
            if typeChat == dataConfig['typeGroup']:
                cvTime = int(time.mktime(mesoutbybot.date.timetuple()))
                utils.updateChat(mesoutbybot['message_id'],
                                 mesoutbybot['chat']['id'],
                                 (cvTime + timeConfig))
        except Exception as e:
            dbrun.writeLog('getTokenETH', str(e))

    else:
        update.message.reply_text("Sai câu lệnh")


def getContractETH(update: Update, context: CallbackContext) -> None:
    try:
        token = update.message.text.split(' ')
        if token[1].strip():
            resinsert =  dbrun.insertToDb(update.message.to_json(), 1) # Insert user/group
            print(resinsert)

            strOut = checkToken.getTokenWithSymbol(
                token[1], 2, update.message.from_user['first_name'],
                update.message.from_user['id'], 'eth')

            mesoutbybot = update.message.reply_text(strOut)

            typeChat = mesoutbybot['chat']['type']
            if typeChat == dataConfig['typeGroup']:
                cvTime = int(time.mktime(mesoutbybot.date.timetuple()))
                utils.updateChat(mesoutbybot['message_id'],
                                 mesoutbybot['chat']['id'], (cvTime + timeConfig))

                utils.updateChat(update.message.message_id,
                                 update.message.chat_id, (cvTime + timeConfig))
        else:
            update.message.reply_text("Sai câu lệnh")
    except Exception as e:
        dbrun.writeLog('getContractETH', str(e))
#endregion

#region Add Token
def addTokenBSC(update: Update, context: CallbackContext) -> None:
    try:
        # Check User
        check = dbrun.checkUserAdmin(update.message.chat_id)
        if check:
            contract = update.message.text.split(' ')
            if contract[1].strip():
                result = dbrun.insertToDb(contract[1].strip(), 2, 'bsc')
                update.message.reply_text(result)
            else:
                update.message.reply_text('Điền cái éo gì thế???')
        else:
            update.message.reply_text('Phắn đê bạn êi')
    except Exception as e:
        dbrun.writeLog('addTokenBSC', str(e))


def addTokenETH(update: Update, context: CallbackContext) -> None:
    try:
        # Check User
        check = dbrun.checkUserAdmin(update.message.chat_id)
        if check:
            contract = update.message.text.split(' ')
            if contract[1].strip():
                result = dbrun.insertToDb(contract[1].strip(), 2, 'eth')
                update.message.reply_text(result)
            else:
                update.message.reply_text('Điền cái éo gì thế???')
        else:
            update.message.reply_text('Phắn đê bạn êi')
    except Exception as e:
        dbrun.writeLog('addTokenETH', str(e))
#endregion

# region An xin
def setWallet(update: Update, _: CallbackContext) -> int:
    typeChat = update.message['chat']['type']
    if typeChat == dataConfig['typePerson']:
        update.message.reply_text(
            'Vui lòng nhập nội dung ví theo định dạng bạn mong muốn\nVí dụ: Ủng hộ quỹ hưu trí: \nVí BNB: xxxx\nVí ETH: xxx\nNhập /cancel để huỷ bỏ', reply_markup=ReplyKeyboardRemove())

        return SWL
    else:
        update.message.reply_text('Group giàu bỏ mẹ éo cho set ví nhớ 🤨🤨🤨')
        return ConversationHandler.END


def SaveWL(update: Update, _: CallbackContext) -> int:
    with open('save_wallet.json', 'r') as dl_file:
        data = json.load(dl_file)
        user = [x for x in data if x['user_id'] == update.message.from_user.id]

    if (len(user) > 0):
        user[0]['mes_user'] = update.message['text']
        with open('save_wallet.json', 'w') as data_file:
            json.dump(data, data_file)
    else:
        objUser = {
            'user_id': update.message.from_user.id,
            'mes_user': update.message['text']
        }

        data.append(objUser)
        with open('save_wallet.json', 'w') as data_file:
            json.dump(data, data_file)

    update.message.reply_text('Nhập thông tin thành công')
    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    return ConversationHandler.END


def anxin(update: Update, context: CallbackContext) -> None:
    with open('save_wallet.json', 'r') as dl_file:
        data = json.load(dl_file)
        user = [x for x in data if x['user_id'] == update.message.from_user.id]
        if (len(user) > 0):
            update.message.reply_text(user[0]['mes_user'])
        else:
            update.message.reply_text('Giàu vl ăn xin gì nữa')
    # update.message.reply_text(
    #     'Ủng hộ cha làm bot nghèo 🙇🏻 \nBNB-Bep20: 0x810Caa3fFf0A9C56b22B745dE713d1b305dDbA71\nETH: 0x6067Eb0f98AB2488d8AB66232CeCCdc399c94A0D'
    # )
# endregion

# region Other
def chaosep(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Ơi'
    )


def infoBot(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Em chào anh, nhà em 3 đời làm bot 🤖, hiện tại bot này nhà em có: \n/p - Nhập mã Token để lấy thông tin v1\n/ct - Nhập mã Token để lấy Contract v1\n/p2 - Nhập mã Token để lấy thông tin v2\n/ct2 - Nhập mã Token để lấy Contract v2\n/info - Gọi em ra để dooddeed nè'
    )


def checkGas(update: Update, context: CallbackContext) -> None:
    text_out = dbrun.checkGasEth()
    mesoutbybot = update.message.reply_html(text_out)
    typeChat = mesoutbybot['chat']['type']
    if typeChat == dataConfig['typeGroup']:
        cvTime = int(time.mktime(mesoutbybot.date.timetuple()))
        utils.updateChat(mesoutbybot['message_id'],
                         mesoutbybot['chat']['id'], (cvTime + timeConfig))

        utils.updateChat(update.message.message_id,
                         update.message.chat_id, (cvTime + timeConfig))


def error(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)
# endregion

def main():
    try:
        """Start the bot."""
        updater = Updater(TOKEN, use_context=True)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler("p", getToken))
        dp.add_handler(CommandHandler("cb", getContract))

        dp.add_handler(CommandHandler("pe", getTokenETH))
        dp.add_handler(CommandHandler("ce", getContractETH))

        dp.add_handler(CommandHandler("ab", addTokenBSC))
        dp.add_handler(CommandHandler("ae", addTokenETH))

        dp.add_handler(CommandHandler("info", infoBot))
        dp.add_handler(CommandHandler("anxin", anxin))
        dp.add_handler(CommandHandler("chaosep", chaosep))
        dp.add_handler(CommandHandler("gas", checkGas))

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('setwl', setWallet)],
            states={
                SWL: [MessageHandler(Filters.text, SaveWL)]
            },
            fallbacks=[CommandHandler('cancel', cancel)],
        )
        dp.add_handler(conv_handler)

        # Log error
        dp.add_error_handler(error)

        # Webhook start bot
        updater.start_webhook(listen="0.0.0.0",
                              port=8443,
                              url_path=TOKEN,
                              key='private.key',
                              cert='cert.pem',
                              webhook_url=URL_BOT + TOKEN)
        updater.idle()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
