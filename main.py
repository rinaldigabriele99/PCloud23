import json
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)
local = True

@app.route('/',methods=['GET'])
def main():
    return render_template('index.html', title='Home')

#----------------------------------------------------------------------------------------------
#LOGIN
@app.route('/login',methods=['GET'])
def pippo():
    return render_template('index-log.html', title='Home')

@app.route('/login1',methods=['GET'])
def pippo1():
    return render_template('login.html', title='Home')

#-----------------------------------------------------------------------------------------------
#FIRESTORE SENSORE
#visualizzo in formato json i dati che manda il client_sensor
@app.route('/sensors',methods=['GET'])
def sensor_data():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    s = []
    for doc in db.collection('sensors').stream():
        s.append(doc.id)
    return json.dumps(s), 200

#aggiungo i valori che ricevo dal sensore al db firestore
@app.route('/sensors/<s>',methods=['POST'])
def add_data(s):
    #print(str(request.values))
    #return 'ok'
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    chiavi = ['date', '%IronFeed', '%SilicaFeed', 'StarchFlow', 'AminaFlow', 'OrePulpFlow'
              , 'OrePulppH', 'OrePulpDensity', 'FlotationColumn01AirFlow', 'FlotationColumn02AirFlow'
              , 'FlotationColumn03AirFlow', 'FlotationColumn04AirFlow', 'FlotationColumn05AirFlow'
              , 'FlotationColumn06AirFlow', 'FlotationColumn07AirFlow', 'FlotationColumn01Level'
              , 'FlotationColumn02Level', 'FlotationColumn03Level', 'FlotationColumn04Level'
              , 'FlotationColumn05Level', 'FlotationColumn06Level', 'FlotationColumn07Level', '%IronConcentrate'
              , '%SilicaConcentrate']
    for chiave in chiavi:
        entity = db.collection('sensors').document(s)
        entity.set(request.values)
    return 'ok', 200

#visualizzo i dati presenti sul db firestore
@app.route('/sensors/<s>', methods=['GET'])
def get_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        return json.dumps(entity.to_dict()),200
    else:
        return 'sensor not found',404

#visualizzo un grafico dal coi dati presenti sul db firestore
@app.route('/graph/<s>',methods=['GET'])
def graph_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        d = []
        d.append(['Number',s])
        t = 0
        for x in entity.to_dict()['values']:
            d.append([t,x])
            t+=1
        return render_template('graph.html',sensor=s,data=json.dumps(d))
    else:
        return redirect(url_for('static', filename='sensor404.html'))
#-----------------------------------------------------------------------------------------------
#FIRESTORE PERSONE
#mi restituise il contenuto della collection persone
@app.route('/fire',methods=['GET'])
def fire():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    result = ''
    for doc in db.collection('persone').stream():
        result += (f'{doc.id} --> {doc.to_dict()}<br>')
    return result

@app.route('/userlogin',methods=['POST'])
def userlogin():
    return render_template ('index.html')

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