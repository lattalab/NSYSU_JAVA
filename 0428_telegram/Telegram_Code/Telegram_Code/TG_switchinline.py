import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, Updater

# 定義inline query handler，處理inline query
def inlinequery(update, context):
    query = update.inline_query.query

    if query:
        # 獲取使用者輸入的搜尋關鍵字
        search_term = query

        # 處理搜尋結果
        search_result = []

        # ... 在此處理搜尋結果 ...

        # 創建 InlineQueryResultArticle 對象，展示搜尋結果
        results = [
            InlineQueryResultArticle(
                id='1',
                title='搜尋結果',
                input_message_content=InputTextMessageContent(search_result),
            ),
        ]

        # 回傳搜尋結果
        update.inline_query.answer(results)
    else:
        # 如果使用者沒有輸入搜尋關鍵字，回傳空結果
        update.inline_query.answer([])

# 建立updater和dispatcher
updater = Updater(token='6220870570:AAFeEazKD8HHkshP3tYfGU-YBpPKjU_MviE', use_context=True)
dispatcher = updater.dispatcher

# 加入inline query handler
dispatcher.add_handler(InlineQueryHandler(inlinequery))

# 啟動bot
updater.start_polling()
