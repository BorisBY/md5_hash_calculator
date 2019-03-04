import hashlib
import os
import wget

def generate_file_md5(filename, blocksize=128):
    m = hashlib.md5()
    with open(os.path.join(filename), "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()

url = 'https://cloud.mail.ru/public/Fvwt/4wMN4P2Bc'
work_name = "/home/borya/md5_hash_calculator/files/file"
try:
    if os.path.isfile(work_name):
        os.unlink(work_name)
    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
except Exception as e:
    print(e)

try:
    filename = wget.download(url)
except:
    print('error')

os.rename("/home/borya/md5_hash_calculator/"+filename, work_name)
temp = generate_file_md5(filename=work_name)

print(temp)