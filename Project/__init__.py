from flask import Flask, request, abort
import requests
import json
from Project.Config import *
from uncleengineer import thaistock
app = Flask(__name__)


def GET_BTC_PRICE():
    data = requests.get('https://bx.in.th/api/')
    BTC_PRICE = data.text.split('BTC')[1].split('last_price":')[1].split(',"volume_24hours')[0]
    return BTC_PRICE




@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        number = message.split("\n")
        
        
        for x in number:
            lineNotify(x)
            strUrl = r'https://firebasestorage.googleapis.com/v0/b/image-284ce.appspot.com/o/civil%20registration%2F'+x+r'.png?alt=media&token=1df63c8b-378c-45af-9796-76448ab91c85'
            r = requests.head(strUrl)
            lineNotify(r.status_code)
            
            if( r.status_code <> 404 )
                lineNotify(x)
                notifyPicture(strUrl)
            elif( r.status_code == 404 )
                lineNotify('ไม่พบเบอร์ :'+x)
            
        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!! 11111122666 ' , 200

    else:
        abort(400)

@app.route('/')
def hello():
    return 'hello world book',200

#ข้อความ
def lineNotify(message):
    payload = {'message':message}
    return _lineNotify(payload)

#รูปภาพ
def notifyPicture(url):
    payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
    return _lineNotify(payload)

#ส่งแจ้งเตือน
def _lineNotify(payload,file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    token = 'phv9j1wVnRhB9tOodD7ttLlkt9zYGcQHUI1E4woNjhx'
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)
