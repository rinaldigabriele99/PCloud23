from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return render_template('index.html', title='Home')

@app.route('/login',methods=['GET'])
def pippo():
    return render_template('login.html', title='Home')

@app.route('/upload',methods=['POST'])
def upload_data():
    return render_template('login.html', title='Home')



#configurazione firestore - login
db = firestore.Client.from_service_account_json('credentials.json')

coll = 'persone'

# creazione di un entity (document)
entity = db.collection(coll).document('gabrielerinaldi')
entity.set({'nome':'gabriele','cognome':'rinaldi'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)