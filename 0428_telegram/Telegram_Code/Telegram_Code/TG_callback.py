import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater

# 定義callback function，處理callback query
def button(update, context):
    query = update.callback_query
    if query.data == 'yes':
        query.answer()
        query.edit_message_text(text="您選擇了「是」。")
    elif query.data == 'no':
        query.answer()
        query.edit_message_text(text="您選擇了「否」。")
    elif query.data == 'cancel':
        query.answer()
        query.edit_message_text(text="您已取消操作。")

# 定義指令handler，當使用者輸入 /start 時，發送一條訊息並附上一個inline keyboard
def start(update, context):
    keyboard = [[InlineKeyboardButton("是", callback_data='yes'),
                 InlineKeyboardButton("否", callback_data='no')],
                [InlineKeyboardButton("取消", callback_data='cancel')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="您是否要繼續操作？", reply_markup=reply_markup)

# 建立updater和dispatcher
updater = Updater(token='6220870570:AAFeEazKD8HHkshP3tYfGU-YBpPKjU_MviE', use_context=True)
dispatcher = updater.dispatcher

# 加入command handler
dispatcher.add_handler(CommandHandler('start', start))

# 加入callback query handler
dispatcher.add_handler(CallbackQueryHandler(button))

# 啟動bot
updater.start_polling()
