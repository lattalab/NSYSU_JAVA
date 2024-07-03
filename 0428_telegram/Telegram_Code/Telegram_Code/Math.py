import telegram
import telegram.ext
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
import csv
from math import factorial

def Select_Command(update: telegram.Update, context: CallbackContext):
    reply_markup = telegram.ReplyKeyboardMarkup([[
        telegram.KeyboardButton('階層計算'),telegram.KeyboardButton('BMI計算')],
        [telegram.KeyboardButton('加總計算'),telegram.KeyboardButton('乘法計算')
    ]], resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="請選擇模式",reply_markup=reply_markup)


def Select(update: telegram.Update, context: CallbackContext):
    mode = update.message.text
    context.user_data['mode'] = mode
    if mode == '階層計算':
        context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入數字(階層計算輸入格式: 10)")
    elif mode == 'BMI計算':
        context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入數字(BMI計算輸入格式: 180,60)")
    elif mode == '加總計算':
        context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入數字(加總計算輸入格式: 1,10)")
    elif mode == '乘法計算':
        context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入數字(乘法計算輸入格式: 5,5)")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入數字(輸入錯誤！)")
        return

def Select_text(update: telegram.Update, context: CallbackContext):
    mode = context.user_data.get('mode')
    text = update.message.text
    if mode == '階層計算':
        result = factorial(int(text))
        Create_Data(text, result, "Factorial")
    elif mode == 'BMI計算':
        text_split = text.split(',')
        result = int(text_split[1]) / (int(text_split[0])/100)**2
        Create_Data(text, result, "BMI")
    elif mode == '加總計算':
        result = 0
        text_split = text.split(',')
        for n in range(int(text_split[0]),int(text_split[1])+1):
            result += n
        Create_Data(text, result, "Sum")
    elif mode == '乘法計算':
        text_split = text.split(',')
        result = int(text_split[0]) * int(text_split[1])
        Create_Data(text, result, "Multiplication ")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="輸入錯誤！")
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


def Create_Data(text, result, file):
    data = []
    data.append(text)
    data.append(result)
    filepath = "./Math_Record/" + file + ".csv"
    with open(filepath, 'a+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


def main():
    updater = telegram.ext.Updater(token="6119764474:AAFWPaxXuUvdVs8u5VIlE9DBmKHhQjazV_Y", use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('math', Select_Command)
    Select_handler = MessageHandler(Filters.text & (~Filters.command), Select_text)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.regex('^(階層計算|BMI計算|加總計算|乘法計算)$'), Select))
    dispatcher.add_handler(Select_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


