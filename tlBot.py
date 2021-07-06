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
CERT = '/home/cer/PUBLIC.pem'

bot = Bot(TOKEN)
timeConfig = 60

SWL = range(1)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


# region Get Token BSC
def getToken(update: Update, context: CallbackContext) -> None:
    try:
        # resinsert = dbrun.insertToDb(
        #     update.message.to_json(), 1)  # Insert user/group
        # print(resinsert)

        # Check user/group deactive
        checkUG = dbrun.getUserGroup(update.message.chat_id)
        if checkUG and checkUG['active']:
            token = update.message.text.split(' ')
            if token[1].strip():
                try:
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
                    print(e)
                    dbrun.writeLog('getToken', str(e))

            else:
                update.message.reply_text("Sai câu lệnh")
        else:
            update.message.reply_text("Đóng họ đê!!!!")
    except Exception as e:
        print(e)

def getContract(update: Update, context: CallbackContext) -> None:
    try:
        resinsert = dbrun.insertToDb(
            update.message.to_json(), 1)  # Insert user/group
        print(resinsert)

        # Check user/group deactive
        checkUG = dbrun.getUserGroup(update.message.chat_id)
        if checkUG and checkUG['active']:
            token = update.message.text.split(' ')
            if token[1].strip():
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
        else:
            update.message.reply_text("Đóng họ đê!!!!")
    except Exception as e:
        print(e)
        dbrun.writeLog('getContract', str(e))
# endregion

# region Get Token ETH


def getTokenETH(update: Update, context: CallbackContext) -> None:
    try:
        resinsert = dbrun.insertToDb(
            update.message.to_json(), 1)  # Insert user/group
        print(resinsert)

        # Check user/group deactive
        checkUG = dbrun.getUserGroup(update.message.chat_id)
        if checkUG and checkUG['active']:
            token = update.message.text.split(' ')
            if token[1].strip():
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
            else:
                update.message.reply_text("Sai câu lệnh")
        else:
            update.message.reply_text("Đóng họ đê!!!!")
    except Exception as e:
        print(e)
        dbrun.writeLog('getTokenETH', str(e))


def getContractETH(update: Update, context: CallbackContext) -> None:
    try:
        resinsert = dbrun.insertToDb(
            update.message.to_json(), 1)  # Insert user/group
        print(resinsert)

        # Check user/group deactive
        checkUG = dbrun.getUserGroup(update.message.chat_id)
        if checkUG and checkUG['active']:
            token = update.message.text.split(' ')
            if token[1].strip():
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
        else:
            update.message.reply_text("Đóng họ đê!!!!")
    except Exception as e:
        print(e)
        dbrun.writeLog('getContractETH', str(e))
# endregion

# region Add Token

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
        print(e)
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
        print(e)
        dbrun.writeLog('addTokenETH', str(e))
# endregion

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


def infoBot(update: Update, context: CallbackContext) -> None:
    # Check user/group deactive
    checkUG = dbrun.getUserGroup(update.message.chat_id)
    if checkUG and checkUG['active']:
        update.message.reply_text(
            'Em chào anh, nhà em 3 đời làm bot 🤖, hiện tại bot này nhà em có: \n/p - Nhập mã Token để lấy thông tin Token BSC\n/cb - Nhập mã Token để lấy Contract Token BSC\n/pe - Nhập mã Token để lấy thông tin Token ETH\n/ce - Nhập mã Token để lấy Contract Token ETH\n/info - Gọi em ra để dooddeed nè'
        )
    else:
        update.message.reply_text("Đóng họ đê!!!!")


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
                              port=5000,
                              url_path=TOKEN,
                              webhook_url=f'https://{URL_BOT}/{TOKEN}',
                              cert=CERT)
        updater.idle()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
