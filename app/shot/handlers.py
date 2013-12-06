import os
import formencode
import tornado.web
import hashlib
import time
import tempfile
import Image
from tornado.escape import utf8
from tornado.web import URLSpec as url
from tornado.web import UIModule, authenticated
from tornado.options import options
from dojang.app import DojangApp
from dojang.database import db
from dojang.cache import autocache_get, autocache_set
from app.account.lib import UserHandler

from app.account.decorators import require_user
from weibo import APIClient

from app.account.models import People
from .models import Shot

class CreateShotHandler(UserHandler):
    @require_user
    def get(self):
        shot = Shot()
        self.render('shot/create_shot.html', shot=shot)

    @require_user
    def post(self):
        o = Shot()
        token = self.get_argument("token", None)
        expires = self.get_argument("expires", None)
        if self.request.files:
            file = self.request.files['shot'][0]
            people = People.query.get(self.current_user.id)
            if file:
                rawname = file.get('filename')
                dstname = str(int(time.time()))+'.'+rawname.split('.').pop()
                dstname = dstname.lower()
                thbname = "s%s" % (dstname)
                large_thbname = "l%s" % (dstname)
                                
                tf = tempfile.NamedTemporaryFile(delete=False)
                tf.write(file['body'])
                tf.seek(0)
                
                file_path = options.local_upload_path + '/shot/' + thbname
                large_file_path = options.local_upload_path + '/shot/' + large_thbname
                img = Image.open(tf.name)
                img.thumbnail((120,120),resample=1)
                img.save(file_path)
                tf.close()

                try:
                    os.remove(tf.name)
                except Exception, e:
                    pass
                

                small_url = options.local_upload_url + '/shot/' + thbname
                large_url = options.local_upload_url + '/shot/' + large_thbname
                o.small_url = small_url
                o.large_url = large_url


                if token:
                    client = APIClient(app_key=options.weibo_key, app_secret=options.weibo_secret,
                           redirect_uri="http://www.keepcd.com/account/weibo/auth")
                  
                    access_token = token
                    expires_in = expires 
                    client.set_access_token(access_token, expires_in)
                    
                    try:
                        text = "http://www.iosplay.com/shot"
                        f = open(large_url, 'rb')
                        r = client.statuses.upload.post(status=text, pic=f)
                        weibo_small_url = r['bmiddle_pic']
                        weibo_large_url = r['original_pic']
                        o.cdn1 = weibo_large_url
                        f.close() 
                    except Exception, e:
                        pass

            db.session.add(o)
            db.session.commit()

            return self.redirect('/shot')

class ShowAllShotsHandler(UserHandler):
    def get(self):
        shots = Shot.query.filter_by().all()
        self.render('shot/all_shots.html', shots=shots)


app_handlers = [
    url('', ShowAllShotsHandler, name='show-all-shots'),
    url('/new', CreateShotHandler, name='new-shot'),
    # url('/([a-z0-9]+)', ShowShotHandler, name='show-shot'),
 
  

]

app_modules = {
   
}

app = DojangApp('shot', __name__, handlers=app_handlers, ui_modules=app_modules)
