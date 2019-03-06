import psycopg2
import psycopg2.extras
from threading import Thread
from flask import Flask
from flask import request, Response
import hashlib
import os
import wget
import smtplib
def send_email(to_addr, body_text):
    server = smtplib.SMTP('smtp.mail.ru', 25)
    server.ehlo()
    server.starttls()
    server.login('test_boston_gene@mail.ru', 'boston2019')
    server.sendmail('test_boston_gene@mail.ru', to_addr, msg=body_text)
    server.quit()

def calculate_hash(filename, email, url, blocksize=128):
    m = hashlib.md5()
    with open(os.path.join(filename), "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    text_for_sent = 'adress file={}, calculated hash md5={}'.format(url, m.hexdigest())
    if email is not None:
        send_email(to_addr=email, body_text=text_for_sent)
    return m.hexdigest()

def download_file_and_calculate_hash(task_id, email, url = 'https://download.sublimetext.com/sublime_text_3_build_3176_x64.tar.bz2'):
    work_name = "/home/borya/md5_hash_calculator/files/file"
    try:
        if os.path.isfile(work_name):
            os.unlink(work_name)
    except Exception as e:
        print(e)

    try:
        filename = wget.download(url)
        update_download(status='TRUE', id = task_id)
    except Exception as e:
        print('error')
    os.rename("/home/borya/md5_hash_calculator/"+filename, work_name)
    md = calculate_hash(filename=work_name, url=url, email=email)
    update_hash(hash=md, url=url, id=task_id)
    return work_name

app = Flask(__name__)
PG_HOST = '127.0.0.1'
PG_DATABASE = 'boston'
PG_USER = 'boston'
PG_PASSWORD = 'boston'

def create_task():
    try:
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('INSERT INTO "maintable" (download, hash_sum, url) VALUES (%s, %s, %s) returning id',
                    ('NULL', 'NULL', 'NULL'))
        conn.commit()
        id = cur.fetchone()['id']
        cur.close()
        conn.close()
        return id
    except Exception as e:
        print(e)
        return False

def update_download(status, id):
    try:
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """UPDATE "maintable" SET "download"='%s' WHERE "id"='%s'""" % (status, id)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def update_hash(hash, url, id):
    try:
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """UPDATE "maintable" SET "hash_sum"='%s', url='%s' WHERE "id"='%s'""" % (hash, url, id)
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_status(id):
    try:
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (PG_HOST, PG_DATABASE, PG_USER, PG_PASSWORD))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """SELECT * FROM "maintable" WHERE "id"='%s'""" % id
        cur.execute(query)
        conn.commit()
        items_list = [c for c in cur]
        ext = items_list[0]
        cur.close()
        conn.close()
        return ext
    except Exception as e:
        print(e)
        return False


@app.route('/submit', methods=['POST'])
def md5_hash():
    if request.method == 'POST':
        email = None
        try:
            email = request.form['email']
        except:
            print('No email')
        try:
            tsk_number = create_task()
            url = request.form['url']
            # file = download_file_and_calculate_hash(url=url, task_id = tsk_number, email=email)
            md = Thread(target=download_file_and_calculate_hash, args=(tsk_number, email, url))
            variavle = md.start()
            return str(tsk_number)
        except Exception as e:
            print(e)
        print('excelent')

@app.route('/check', methods=['GET'])
def check():

    if request.method == 'GET':
        try:
            id = request.args['id']
            tmp = get_status(id)
            if tmp['download'] == 'NULL' or tmp['hash_sum'] == 'NULL' or tmp['url'] == 'NULL':
                return('"status":"running"')
            else:
                tmp='"id":"%s", "md5":"%s", "status":"%s", "url":"%s"'%(tmp['id'],tmp['hash_sum'],tmp['download'],tmp['url'])
                return tmp
        except Exception as e:
            print(e)

        print('excelent')


if __name__ == '__main__':
    app.run(debug=True)