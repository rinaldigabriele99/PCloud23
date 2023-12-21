import json
import joblib
from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.cloud import firestore
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key
from json import loads
from base64 import b64decode
from google.cloud import pubsub_v1
from flask_mail import Mail, Message
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# si definisce una classe utente, che rappresenta l'utente, username e parametri
class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key

# Configurazione delle impostazioni per l'invio di e-mail usando Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'rinaldi.gabriele1999@gmail.com'
app.config['MAIL_PASSWORD'] = 'ukiatdajbzdebzhi'

# Inizializzazione dell'oggetto Mail
mail = Mail(app)

#da cambiare al momento del deploy
local = True

login = LoginManager(app)
login.login_view = '/static/login.html'

# funzione che serve per creare un utente con i suoi parametri
@login.user_loader
def load_user(username):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document(username).get().to_dict()
    return User(user['username'])


#----------------------------------------------------------------------
#WEBAPP-MAIN
@app.route('/',methods=['GET'])
def main():
    return render_template('index.html', title='Home')

#----------------------------------------------------------------------------------------------
#LOGIN
@app.route('/login', methods=['POST'])
def login_route():
    #return str(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect('/main')
    username = request.values['u']
    password = request.values['p']
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document(username).get()
    if user.exists and user.to_dict()['password'] == password:
        login_user(User(username))
        next_page = request.args.get('next')
        if not next_page:
            next_page = '/main'
        return redirect(next_page)
    return redirect('/static/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    #creazione lista contenente tutti gli amministratori
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    documenti = db.collection('utenti').stream()
    lista_user = []
    for doc in documenti:
        utente = doc.to_dict().get('username')
        lista_user.append(utente)
    if current_user.is_authenticated:
    #if current_user.username in lista_user:
        if request.method == 'GET':
            return redirect('/static/adduser.html')
        else:
            username = request.values['u']
            password = request.values['p']
            email = request.values['e']
            db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
            user = db.collection('utenti').document(username)
            user.set({'username':username, 'password':password, 'email':email})
            return redirect ('/main')
    else:
            return redirect ('/')
    
@app.route('/main', methods=['GET'])
@login_required
def homepageLog():
    return render_template('index-log.html', title='Home')

#-----------------------------------------------------------------------------------------------
#FIRESTORE SENSORE
#visualizzo in formato json i dati che manda il client_sensor presenti sul db firestore
@app.route('/sensors',methods=['GET'])
def sensor_data():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    s = []
    for doc in db.collection('sensors').stream():
        s.append(doc.id)
    return json.dumps(s), 200

#endpoint collegato alla chiamata ajax che manda i dati del db firestore al browser
@app.route('/sensors/all',methods=['GET'])
def sensor_data_firestore():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    data = []
    for doc in db.collection('sensors').stream():
        dict_values = doc.to_dict()
        dict_values['Sensors'] = doc.id
        data.append(dict_values)
    json_data = json.dumps(data, indent = 2)
    return json_data, 200

#aggiungo i valori che ricevo dal sensore in modalità http al db firestore
@app.route('/sensors/<s>', methods=['POST'])
def add_data(s):
    #print(str(request.values))
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


#ricevo i dati dal topic via pubsub e li aggiungo sul db firestore
@app.route('/pubsub/push', methods=['GET'])
def pubsub_push(): 
    '''
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path('progettocloud23', 'pcloud-subscriber')
    subscriber.subscribe(subscription_path, callback=callback)
    #print('ricevuto payload', flush=True)
    #dict = loads(request.data.decode('utf-8'))
    #print(dict, flush=True)
    
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
    '''
    return 'ok', 200 

#visualizzo i dati presenti sul db firestore per ogni riga (s)
@app.route('/sensors/<s>', methods=['GET'])
def get_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        return json.dumps(entity.to_dict()), 200
    else:
        return 'sensor not found', 404
    
#visualizzo i sensori (rilevazioni) fatte e inviate
@app.route('/sensors', methods=['GET'])
def get_data_firestore():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').get()
    #print(json.dumps(entity.to_dict()))
    if entity.exists:
        return json.dumps(entity.to_dict()), 200
    else:
        return 'sensor not found', 404

#-----------------------------------------------------------------------------------------------
#ML MODEL
#ricevo i dati via post dalla form html della web app
@app.route('/process_form', methods=['POST'])
@login_required
def process_form():
    data = request.values
    preprocessed_data = []
    riga = []
    #scorri json e crea una lista preprocessed_data di questo tipo [[..,..,..,..]]
    ordered_keys = list(request.form.keys())
    for chiave in ordered_keys:
        riga.append(float(data[chiave].replace(',', '.')))
    preprocessed_data.append(riga) 
    
    model = joblib.load('modello_regressione.joblib')
    prediction = model.predict(preprocessed_data)
    
    if prediction > 3:
        #creazione lista destinatari (utenti registrati)
        db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
        entity = db.collection('utenti').get()
        listaDestinatari = []
        for riga in entity:
            dati = riga.to_dict()
            listaDestinatari.append(dati['email'])
        
        # Creazione email
        msg = Message('La predizione ha superato il valore soglia', sender='rinaldi.gabriele1999@gmail.com', recipients=listaDestinatari)
        msg.body = f'ATTENZIONE: la predizione ha superato il valore soglia. Predizione ottenuta: {prediction}'
        mail.send(msg)
     
    return render_template('index-log.html', data_prediction = str(prediction))   
    return str(prediction)

#ricevo i dati via post dalla form html della web app e calcolo la predizione col ml_model_facoltativo
@app.route('/process_form_facoltativo', methods=['POST'])
@login_required
def process_form_facoltativo():
    valorereale = request.form.get('valorereale')
    data = request.values
    preprocessed_data = []
    riga = []
    #scorri json e crea una lista preprocessed_data
    ordered_keys = list(request.form.keys())
    for chiave in ordered_keys:
        if chiave == 'valorereale':
            continue
        else:
            riga.append(float(data[chiave].replace(',', '.')))
    preprocessed_data.append(riga)
    
    model = joblib.load('modello_regressione_facoltativo.joblib')
    prediction = model.predict(preprocessed_data)
    
    # Se non è di tipo stringa, convertilo
    if prediction.dtype != np.dtype('str'):
        prediction = prediction.astype(str)
    
    valorereale_num = np.core.defchararray.replace(valorereale, ',', '.')
    prediction_num = np.core.defchararray.replace(prediction, ',', '.')
    mse = (float(valorereale_num) - float(prediction_num))**2
    return render_template('index-log.html', data_prediction_fac = str(prediction), valore_reale = str(valorereale), errore_mse = str(mse))   
    return str(prediction)

#ENDPOINT DA USARE PER PROVE
@app.route('/test', methods=['GET'])
def test():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document('gabriele').get().to_dict()
    
    return str(user['username'])

    
   
#-----------------------------------------------------------------------------------------------
#ESECUZIONE APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)