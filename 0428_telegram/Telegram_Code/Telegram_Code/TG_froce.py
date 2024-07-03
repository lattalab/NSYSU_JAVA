import telegram
from telegram import ForceReply
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# 定義指令handler，當使用者輸入 /reply 時，發送一條訊息並要求使用者回覆
def reply(update, context):
    reply_markup = ForceReply()
    context.bot.send_message(chat_id=update.message.chat_id, text="請回覆一則訊息：", reply_markup=reply_markup)

# 定義訊息handler，當使用者回覆訊息時，bot會回傳相應的訊息
def echo(update, context):
    text = update.message.text
    context.bot.send_message(chat_id=update.message.chat_id, text="你回覆了：" + text)

# 建立updater和dispatcher
updater = Updater(token='6220870570:AAFeEazKD8HHkshP3tYfGU-YBpPKjU_MviE', use_context=True)
dispatcher = updater.dispatcher

# 加入command handler
dispatcher.add_handler(CommandHandler('reply', reply))

# 加入訊息handler
dispatcher.add_handler(MessageHandler(Filters.reply, echo))

# 啟動bot
updater.start_polling()
