# 爬蟲
import requests
from bs4 import BeautifulSoup
# Linebot
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import *
from linebot.exceptions import (
    InvalidSignatureError
)
from flask import Flask, request, abort
from math import *

# 爬臺灣銀行的網頁
response = requests.get(
    "https://rate.bot.com.tw/xrt?Lang=zh-TW")

soup = BeautifulSoup(response.text, "html.parser") # 得到該網頁的html內容

# 定位目標資料的 HTML 元素
table = soup.find("table", class_="table table-striped table-bordered table-condensed table-hover")
rows = table.find_all("tr")


# 迭代每一列資料，取得所需欄位的值
currency = []
cash_buy = []
cash_sell = []
for row in rows:
    columns = row.find_all("td")
    if len(columns) >= 5:
        temp = columns[0].text.strip()[:10].rstrip()
        dollar = (temp.split("(")[1]).split(")")[0]
        currency.append(dollar)  # 貨幣英文簡寫名稱
        cb = columns[1].text.strip()
        if cb != '-':
            cash_buy.append(float(cb))  # 現金買入匯率，賣那一個貨幣需要這麼多台幣
        else:
            cash_buy.append(0.0) # 要是皆為無效值，設為0

        cs =columns[2].text.strip()
        if cs !='-':
            cash_sell.append(float(cs)) # 現金賣出匯率，買那一個貨幣需要這麼多台幣
        else:
            cash_sell.append(0.0) # 要是皆為無效值，設為0
        
# YOUR_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
# YOUR_CHANNEL_SECRET
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
app = Flask(__name__) 

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

import re
@handler.add(MessageEvent, message=TextMessage) # Linebot收到文字訊息時
def rate(event):
    getMess = event.message.text # 紀錄收到的訊息
    if getMess == '/rate': # /rate功能
        reply = "今日台幣對其他貨幣的牌告匯率\n" \
                + "幣別:現金" 
        for i in range(len(currency)):
            oneline = "\n" + currency[i] + ': ' + str(cash_sell[i]) 
            reply += oneline
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
        return
    
    elif '=' in getMess: # 轉換貨幣
        l = getMess.upper().replace(" ","").split("=")
        # 前半段
        # 再分別得到 數字 跟 貨幣
        for char in l[0]:
            if char.isalpha():
                index = l[0].index(char)
                break
        
        v = int(l[0][:index]) # number
        c = l[0][index:] # currency
        
        # case1: 貨幣相同，匯率是1
        if c == l[1]:
            reply = "匯率: 1\n" + str(v) + " " + c
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
        # case2: 台幣轉外幣 (看本行賣出)
        elif c == 'NTD':
            exchange = cash_sell[ (currency.index(l[1])) ]
            reply = "匯率: " + str(exchange) +"\n" \
                    + str(floor(v/exchange)) + " " + l[1]
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
        # case3: 外幣轉台幣 (看本行買入)
        elif l[1] == 'NTD':
            exchange = cash_buy[ (currency.index(c)) ]
            reply = "匯率: " + str(exchange) + "\n" \
                    + str(v*exchange) + " " + l[1]
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
        # case4: 外幣轉外幣 (外幣->台幣->外幣)
        else:
            exchange_to_ntd = cash_buy[ (currency.index(c)) ]
            ntd = v * exchange_to_ntd
            exchange = cash_sell[ (currency.index(l[1])) ]
            result = ntd/exchange
            reply = "匯率: " + str(v/result) + "\n" \
                    + str(result) + " " + l[1]
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
 

# 主程式      
if __name__ == "__main__":
    app.run()
