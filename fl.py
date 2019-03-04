from flask import Flask
from flask import jsonify, request
from app import md5
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    type('asd')
    return 'Hello World!'

@app.route('/submit', methods=['POST'])
def asd():

    if request.method == 'POST':
        try:
            url = request.form['url']
            asd = md5(url=url)
        except:
            print('Error. website address is incorrect')
        try:
            email = request.form['email']
        except:
            print('No email')

        print('excelent')

if __name__ == '__main__':
    app.run(debug=True)