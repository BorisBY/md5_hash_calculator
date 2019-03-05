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
    send_email(to_addr=email, body_text=text_for_sent)
    return m.hexdigest()

def download_file(url = 'https://download.sublimetext.com/sublime_text_3_build_3176_x64.tar.bz2'):
    work_name = "/home/borya/md5_hash_calculator/files/file"
    try:
        if os.path.isfile(work_name):
            os.unlink(work_name)
    except Exception as e:
        print(e)

    try:
        filename = wget.download(url)
    except Exception as e:
        print('error')

    os.rename("/home/borya/md5_hash_calculator/"+filename, work_name)
    return work_name
