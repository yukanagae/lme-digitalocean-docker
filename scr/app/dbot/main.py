

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import openai
import faiss
import requests
import json
from os.path import join, dirname
import numpy as np
from dotenv import load_dotenv

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#環境変数取得
openai.api_key = os.environ['YOUR_API_KEY']
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

def answer(Question):
     # 文章をベクトル化
    with open('/home/flask/flask_project/about.txt', encoding="utf-8") as f:
        sentences = [s.strip() for s in f.readlines()]
    sentences = [x.replace("\n", " ") for x in sentences]
    embeddings = openai.Embedding.create(input = sentences, model="text-embedding-ada-002")['data']
    # 初期化
    d = 1536
    index = faiss.IndexFlatL2(d) 
    # faissで扱えるようnumpyのarrayに変換
    embeddings = np.array([x["embedding"] for x in embeddings], dtype=np.float32) 
    #FaissのIndexに追加
    index.add(embeddings) 
    # ベクトル化
    query = Question
    query_embedding = np.array([openai.Embedding.create(input = [query], model="text-embedding-ada-002")['data'][0]["embedding"]], dtype=np.float32)
    # ベクトル検索
    k = 1
    D, I = index.search(query_embedding, k)
    result = sentences[I[0][0]]
    print(result)
    asking=(f'あなたは受付の悠美ちゃんです。悠美ちゃんは細やかな気配りを忘れない案内ができる人でわかりやすく答えてくれます。質問に対する心情を読み取って、曖昧な回答は避け、以下の文章を参考にしながら簡潔に質問に回答してください。')
    result = result.replace("\n", " ")
    answer = openai.Completion.create(engine="text-davinci-003", prompt=f"{asking}\n\n{result}\n\nQ: {query}\n", max_tokens=1000)["choices"][0]["text"]
    answer=answer.replace("A:「", " ")
    answer=answer.replace("」", " ")
    kousei = openai.Completion.create(engine="text-davinci-003", prompt=f"次の文章を自然な日本語にしてください。命令形は使わず、なるべく文章を省略せずに修正してください。\n\n{answer}\n", max_tokens=1000)["choices"][0]["text"]
    print("質問")
    print(query)
    print("元文章")
    print(result)
    print("回答")
    print(kousei)
    return kousei

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

def tenso(data):
    webhook_url = 'https://cb.lmes.jp/line/callback/add/42913'
    r = requests.post(webhook_url,data=data,headers={'Content-Type':'application/json','Authorization': 'Bearer ' + YOUR_CHANNEL_SECRET})

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/", methods=['POST'])
def callback2():
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    asking=event.message.text
    res=answer(asking)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(res))
    hdjson=json.loads(str(event))
    ids=event.message.id
    text=event.message.text
    replyToken=hdjson['replyToken']
    userId=hdjson['source']['userId']
    timestamp=hdjson['timestamp']
    webhookEventId=hdjson['webhookEventId']
    data=     {
      "destination": "Ue7d55f860963d788349878ecc0e97231",
      "events": [
        {
          "type": "message",
          "message": {
            "type": "text",
            "id": ids,
            "text": text
          },
          "timestamp": timestamp,
          "source": {
            "type": "user",
            "userId": userId
          },
          "replyToken": replyToken,
          "mode": "active",
          "webhookEventId": webhookEventId,
          "deliveryContext": {
            "isRedelivery": "false"
          }
        }
      ]
    }
 
    #tenso(data)
    print(ids,text,replyToken,userId,timestamp,webhookEventId)
    print(data)


if __name__ == "__main__":
    app.run()
#    port = int(os.getenv("PORT", 5000))
#    app.run(host="0.0.0.0", port=port)
