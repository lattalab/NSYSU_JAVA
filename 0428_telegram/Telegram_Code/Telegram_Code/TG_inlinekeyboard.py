import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

# 定義callback function，當使用者點擊inline keyboard時，執行此function
def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'yes':
        context.bot.send_message(chat_id=query.message.chat_id, text="你選擇了 YES")
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="你選擇了 NO")

# 定義指令handler，當使用者輸入 /start 時，會顯示inline keyboard
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("YES", callback_data='yes'), InlineKeyboardButton("NO", callback_data='no')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="請選擇 YES 或 NO", reply_markup=reply_markup)

# 建立updater和dispatcher
updater = Updater(token='6220870570:AAFeEazKD8HHkshP3tYfGU-YBpPKjU_MviE', use_context=True)
dispatcher = updater.dispatcher

# 加入callback query handler
dispatcher.add_handler(CallbackQueryHandler(button))

# 加入command handler
dispatcher.add_handler(CommandHandler('start', start))

# 啟動bot
updater.start_polling()



