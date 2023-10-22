from flask import Flask, render_template, request, redirect, url_for, sessions
#from secret import secret_key  #PROBLEMI NELL'INSTALLAZIONE DEL MODULO secret PER LA secret_key

app = Flask(__name__)

usersdb = {
    'marco':'mamei',
    'lorenzob':'buttarelli',
    'gabriele':'rinaldi',
    'andrea':'donati',
    'lorenzof':'ferrari'
}

app.config['SECRET_KEY'] = '12345' #andava messa la secret_key!!!

@app.route('/',methods=['GET'])
#def main():
#    return 'ciao, per favore verifica la tua identità'
def main():
    if 'loggedin' not in session or session["loggedin"]==False:
        return redirect('/static/login.html')
    else:
        return 'Welcome '+session["nome"]
'''
    user = {'username': 'Marco'}
    list = [1,2,3,4,5]
    return render_template('index.html', title='Home', user=user, list=list)
'''

@app.route('/pag2')
def pag2():
    if 'loggedin' not in session or session["loggedin"]==False:
        return redirect('/static/login.html')
    else:
        return 'Welcome 2'+session["nome"]


@app.route('/login', methods=['POST'])
def login():
    return 'ciao, per favore verifica la tua identità'
    username = request.values['u']
    password = request.values['p']
    if username in usersdb and usersdb[username] == password:
        session["loggedin"] = True
        session["nome"] = username
        return redirect('/')
    else:
        return redirect('/static/login.html')

@app.route('/logout')
def logout():
    session["loggedin"] = False
    return redirect('/')

'''
@app.route('/pippo',methods=['GET'])
def pippo():
    #return 'ciao pippo'

    user = {'username': 'Marco'}
    list = [1,2,3,4,5]
    return render_template('index.html', title='Home', user=user, list=list)
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)