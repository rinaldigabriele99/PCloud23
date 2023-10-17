from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return 'ciao gabriele'
'''
    user = {'username': 'Marco'}
    list = [1,2,3,4,5]
    return render_template('index.html', title='Home', user=user, list=list)
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)