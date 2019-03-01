import hashlib
import os

def generate_file_md5(rootdir, filename, blocksize=2**20):
    m = hashlib.md5()
    with open(os.path.join(rootdir, filename), "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


temp = generate_file_md5(rootdir='/home/borya/', filename='audio_test.mp3')
print(temp)