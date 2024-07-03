import telegram
import openai
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
import csv

def translate_Command(update: telegram.Update, context: CallbackContext):
    reply_markup = telegram.ReplyKeyboardMarkup([[
        telegram.KeyboardButton('英翻簡中'),
        telegram.KeyboardButton('英翻繁中')
    ], [
        telegram.KeyboardButton('繁中翻英'),
        telegram.KeyboardButton('簡中翻英')
    ]], resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="請選擇翻譯模式",reply_markup=reply_markup)


def translate(update: telegram.Update, context: CallbackContext):
    mode = update.message.text
    context.user_data['mode'] = mode
    context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入欲翻譯之文字")


def translate_text(update: telegram.Update, context: CallbackContext):
    mode = context.user_data.get('mode')
    text = update.message.text
    if mode == '英翻簡中':
        GPT_Input_Text = text+"，翻译中国简体字 不要解释"
        result = GPT_Translate(GPT_Input_Text)
        Create_Data(text, result, "English_to_Chinese(Simplified)")
    elif mode == '英翻繁中':
        GPT_Input_Text = text+"英文翻譯中文，繁體中文，不要解釋"
        result = GPT_Translate(GPT_Input_Text)
        Create_Data(text, result, "English_to_Chinese(Traditional)")
    elif mode == '繁中翻英':
        GPT_Input_Text = text+"，中文翻譯英文，不要解釋"
        result = GPT_Translate(GPT_Input_Text)
        Create_Data(text, result, "Chinese(Traditional)_to_English")
    elif mode == '簡中翻英':
        GPT_Input_Text = text+"，简体字翻译英文，不要解释"
        result = GPT_Translate(GPT_Input_Text)
        Create_Data(text, result, "Chinese(Simplified)_to_English")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="翻譯模式錯誤！")
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def GPT_Translate(input_Text):
    openai.api_key = "" # api key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input_Text,
        temperature=0.5,
        max_tokens=50,
        top_p=0.75,
        n=1,
    )
    return response.choices[0].text.strip()

def Create_Data(text, result, file):
    data = []
    data.append(text)
    data.append(result)
    filepath = "./GPT_Record/" + file + ".csv"
    with open(filepath, 'a+', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


def main():
    updater = telegram.ext.Updater(token='', use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('translate', translate_Command)
    translate_handler = MessageHandler(Filters.text & (~Filters.command), translate_text)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.regex('^(英翻簡中|英翻繁中|繁中翻英|簡中翻英)$'), translate))
    dispatcher.add_handler(translate_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
