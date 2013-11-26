import os.path
from datetime import datetime
import tempfile
import Image
from tornado.options import options
from dojang.auth.upyun import BaseUpyun


class LocalBackend(object):
    @staticmethod
    def save(body, filename, callback=None):
        file_time = datetime.now().strftime('%Y%m')
        file_dir = options.local_static_path+'/'+file_time
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        path = os.path.join(file_dir, filename)
        
        tf = tempfile.NamedTemporaryFile()
        tf.write(body)
        tf.seek(0)

        img = Image.open(tf.name)
        img.thumbnail((1024,1024),resample=1)
                
        img.save(path)
        tf.close()

        #f = open(path, 'w')
        #f.write(body)
        #f.close()
        if not callback:
            return
        callback(os.path.join(options.local_static_url+'/'+file_time, filename))
        return


class UpyunBackend(object):
    @staticmethod
    def save(body, filename, callback):
        upyun = BaseUpyun(
            options.upyun_bucket, options.upyun_username,
            options.upyun_password
        )
        if 'upyun_static_url' in options:
            upyun.static_url = options.upyun_static_url
        upyun.upload(body, filename, callback)
        return
