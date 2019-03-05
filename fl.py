import os
from threading import Thread
from flask import Flask
from flask import jsonify, request
from app import calculate_hash, download_file
app = Flask(__name__)

status = {'id':None, 'download':None, 'md_5':None}

@app.route('/submit', methods=['POST'])
def md5_hash():
    if request.method == 'POST':
        email = None
        try:
            email = request.form['email']
        except:
            print('No email')
        try:
            url = request.form['url']
            file = download_file(url=url)
            if os.path.isfile(file):
                status['id'] = 1
                status['download']=True
                # md = calculate_hash(filename=file, url=url, email=email)
                md = Thread(target=calculate_hash, args=(file, url, email))
                variavle = md.start()
                return variavle

        except Exception as e:
            print(e)

        print('excelent')

@app.route('/check', methods=['GET'])
def check():

    if request.method == 'GET':
        try:
            id = request.form['id']
        except:
            print('Error. website address is incorrect')

        print('excelent')


if __name__ == '__main__':
    app.run(debug=True)