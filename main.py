import json
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    #db = firestore.Client() #collego il client col db
    return render_template('index.html', title='Home')

@app.route('/login',methods=['GET'])
def pippo():
    return render_template('login.html', title='Home')


#aggiungo i valori al firestore che ricevo dal sensore
@app.route('/upload/<s>',methods=['POST'])
def add_data(s):
    val = float(request.values['val'])
    db = firestore.Client.from_service_account_json('credentials.json')
    #db = firestore.Client()
    doc_ref = db.collection('sensors').document('s')
    entity = doc_ref.get()
    if 'values' in entity.to_dict(): 
        v = entity.to_dict()['values']
        v.append(val)
        doc_ref.update({'values':v})
    else:
        doc_ref.set({'values':[val]})
    return 'ok', 200

@app.route('/getdata/<s>',methods=['GET'])
def get_data(s):
    db = firestore.Client.from_service_account_json('credentials.json')
    #db = firestore.Client()
    doc_ref = db.collection('sensor').document(s)
    if doc_ref.exists:
        return json.dumps(doc_ref.get().to_dict()['values']), 200
    else:
        return 'sensor not found', 404
    
@app.route('/getgraph/<s>' ,methods=['GET'])
def graph_data(s):
    db = firestore.Client.from_service_account_json('credentials.json')
    #db = firestore.Client()
    doc_ref = db.collection('sensor').document(s)
    if doc_ref.exists:
        d = []
        d.append(['Number', s])
        t = 0
        for x in doc_ref.get().to_dict()['values']:
            d.append([t,x])
            t += 1
        return render_template('graph.html', sensor = s, data = json.dumps(d))
    else:
        return 'sensor not found', 404


#mi restituise il contenuto della collection
@app.route('/fire',methods=['GET'])
def fire():
    db = firestore.Client.from_service_account_json('credentials.json')
    #db = firestore.Client()
    result = ''
    for doc in db.collection('persone').stream():
        result += (f'{doc.id} --> {doc.to_dict()}<br>')
    return result

#configurazione firestore - login (modalita per accedere al db con server in locale)
db = firestore.Client.from_service_account_json('credentials.json')
#configurazione firestore - login (modalita per accedere al db con server in remoto su google)
#db = firestore.Client()

coll = 'persone'

# creazione di un entity (document)
entity = db.collection(coll).document('gabrielerinaldi')
entity.set({'nome':'gabriele','cognome':'rinaldi'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)