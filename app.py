import hashlib
import os
import wget

def md5(url = 'https://download.sublimetext.com/sublime_text_3_build_3176_x64.tar.bz2'):
    def generate_file_md5(filename, blocksize=128):
        m = hashlib.md5()
        with open(os.path.join(filename), "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
        return m.hexdigest()

    work_name = "/home/borya/md5_hash_calculator/files/file"
    try:
        if os.path.isfile(work_name):
            os.unlink(work_name)
    except Exception as e:
        print(e)

    try:
        filename = wget.download(url)
    except:
        print('error')
        os.rename("/home/borya/md5_hash_calculator/"+filename, work_name)
    temp = generate_file_md5(filename=work_name)
    print(temp)