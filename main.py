import json
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from secret import secret_key

# si definisce una classe utente, che rappresenta l'utente, username e parametri
class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
local = True

login = LoginManager(app)
login.login_view = '/static/login.html'

# funzione che serve per creare un utente con i suoi parametri
@login.user_loader
def load_user(username):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    user = db.collection('utenti').document(username).get()
    #if user.exists():
        #return User(username)
    #return None

#----------------------------------------------------------------------
#WEBAPP-MAIN
@app.route('/',methods=['GET'])
def main():
    return render_template('index.html', title='Home')

#----------------------------------------------------------------------------------------------
#LOGIN
@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/main'))
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

#voglio avere un'univca funzione di aggiunta_utenti, con due modalità di accesso
# se acceduta in modalità GET, restituisce la form in cui inserire i dati dell'utente
# che chiamerà lo stesso metodo in modalità POST
# bisogna creare una pagina html di registrazione nuovi utenti 'adduser.html'
@app.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    if current_user.username == 'lorenzo':
        if request.method == 'GET':
            return redirect(url_for('/static/adduser.html'))
        else:
            username = request.values['u']
            password = request.values['p']
            db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
            user = db.collection('utenti').document(username).get()
            user.set({'username':username, 'passowrd':password})
            return 'ok'
    else:
        return redirect ('/')
    
@app.route('/main', methods=['GET'])
@login_required
def homepageLog():
    return render_template('index-log.html', title='Home')
"""
#LOGIN VECCHIO
@app.route('/main', methods=['GET'])
def homepageLog():
    return render_template('index-log.html', title='Home')

@app.route('/login1',methods=['GET'])
def pippo1():
    return render_template('login.html', title='Home')
"""
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

#visualizzo in formato json i dati che manda il client_sensor presenti sul db firestore
@app.route('/sensors/all',methods=['GET'])
def sensor_data_firestore():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    data = {}
    for doc in db.collection('sensors').stream():
        data[doc.id] = doc.to_dict()
    json_data = json.dumps(data, indent = 2)
    return json_data, 200
    #return render_template('index-log.html', json_data = json_data)

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

#visualizzo i dati presenti sul db firestore per ogni riga (s)
@app.route('/sensors/<s>', methods=['GET'])
def get_data(s):
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').document(s).get()
    if entity.exists:
        return json.dumps(entity.to_dict()), 200
    else:
        return 'sensor not found', 404
    
#visualizzo i dati presenti sul db firestore in formato tabellare
@app.route('/sensors', methods=['GET'])
def get_data_firestore():
    db = firestore.Client.from_service_account_json('credentials.json') if local else firestore.Client()
    entity = db.collection('sensors').get()
    #print(json.dumps(entity.to_dict()))
    if entity.exists:
        return json.dumps(entity.to_dict()), 200
    else:
        return 'sensor not found', 404

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
        return render_template('graph.html', sensor=s, data=json.dumps(d))
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