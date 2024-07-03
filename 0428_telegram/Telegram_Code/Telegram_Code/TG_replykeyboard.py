import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# 定義指令handler，當使用者輸入 /start 時，會顯示reply keyboard
def start(update, context):
    keyboard = [['選項1', '選項2', '選項3']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id, text="請選擇一個選項", reply_markup=reply_markup)

# 定義訊息handler，當使用者點擊reply keyboard的按鈕時，回傳相應的訊息
def echo(update, context):
    text = update.message.text
    if text == '選項1':
        context.bot.send_message(chat_id=update.message.chat_id, text="你選擇了 選項1")
    elif text == '選項2':
        context.bot.send_message(chat_id=update.message.chat_id, text="你選擇了 選項2")
    elif text == '選項3':
        context.bot.send_message(chat_id=update.message.chat_id, text="你選擇了 選項3")

# 建立updater和dispatcher
updater = Updater(token='6220870570:AAFeEazKD8HHkshP3tYfGU-YBpPKjU_MviE', use_context=True)
dispatcher = updater.dispatcher

# 加入command handler
dispatcher.add_handler(CommandHandler('start', start))

# 加入訊息handler
dispatcher.add_handler(MessageHandler(Filters.text, echo))

# 啟動bot
updater.start_polling()


