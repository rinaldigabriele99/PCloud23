from flask import Flask,request
from json import loads
from base64 import b64decode

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return 'ok main mio pc'

@app.route('/pubsub/push',methods=['POST'])
def pubsub_push():
    print('ricevuto payload',flush=True)
    dict = loads(request.data.decode('utf-8'))
    print(dict,flush=True)
    #msg = b64decode(dict['message']['data']).decode('utf-8')
    #print(msg)
    return 'ok pubsub', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)