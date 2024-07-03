import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Filters, MessageHandler, Updater

# 定義指令handler，當使用者輸入 /inline 時，發送一條訊息並附上一個inline keyboard
def inline(update, context):
    keyboard = [[InlineKeyboardButton("Google", url="https://www.google.com.tw")],
                [InlineKeyboardButton("Yahoo", url="https://tw.yahoo.com")],
                [InlineKeyboardButton("Bing", url="https://www.bing.com")],
                [InlineKeyboardButton("Quit", callback_data='quit')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="請選擇一個網站：", reply_markup=reply_markup)

# 定義callback query handler，當使用者點擊按鈕時，觸發對應的動作
def button(update, context):
    query = update.callback_query
    if query.data == 'quit':
        query.answer()
        query.edit_message_text(text="您已退出。")
    else:
        query.answer()
        query.edit_message_text(text="您選擇了" + query.data + "。")

# 建立updater和dispatcher
updater = Updater(token='6220870570:AAFeEazKD8HHkshP3tYfGU-YBpPKjU_MviE', use_context=True)
dispatcher = updater.dispatcher

# 加入command handler
dispatcher.add_handler(CommandHandler('inline', inline))

# 加入callback query handler
dispatcher.add_handler(CallbackQueryHandler(button))

# 啟動bot
updater.start_polling()
