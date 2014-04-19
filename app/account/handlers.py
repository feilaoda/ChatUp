# -*- coding: utf-8 -*-
#!/usr/bin/env python
import Image
import base64
import datetime
import hashlib
import logging
import os
import tempfile
import time

from dojang.app import DojangApp
from dojang.auth.douban import DoubanMixin
from dojang.auth.github import GithubMixin
from dojang.auth.recaptcha import RecaptchaMixin
from dojang.auth.weibo import WeiboMixin
from dojang.cache import autocache_hdel
from dojang.database import db
from dojang.ext import webservice
from dojang.form import FormSchema
from dojang.util import to_md5
import formencode
from tornado.auth import GoogleMixin
from tornado.options import options
from tornado.web import UIModule, HTTPError
from tornado.web import authenticated, asynchronous

from . import validators
from .decorators import require_user
from .lib import UserHandler, get_full_notifies
from .models import People, PeopleSetting, Notify, Weibo


class AccountSignupForm(FormSchema):
    username = formencode.All(validators.Utf8MaxLength(15, messages={"tooLong":u'???????????????15???????????????'}),validators.Utf8MinLength(2, messages={"tooShort":u'???????????????2??????????????????'}),formencode.validators.String(not_empty=True, strip=True, messages={"empty":u"?????????????????????"}))
    

class EmailMixin(object):
    def _create_token(self, user):
        salt = user.create_token(8)
        created = str(int(time.time()))
        hsh = hashlib.sha1(salt + created + user.token).hexdigest()
        token = "%s|%s|%s|%s" % (user.email, salt, created, hsh)
        return base64.b64encode(token)

    def _verify_token(self, token):
        try:
            token = base64.b64decode(token)
        except:
            self.flash_message("Don't be evil", 'error')
            return None
        splits = token.split('|')
        if len(splits) != 4:
            self.flash_message("Don't be evil", 'error')
            return None
        email, salt, created, hsh = splits
        delta = time.time() - int(created)
        if delta < 1:
            self.flash_message("Don't be evil", 'error')
            return None
        if delta > 3600:
            # 1 hour
            self.flash_message('This link is expired, request again', 'warn')
            return None
        user = People.query.get_first(email=email)
        if not user:
            return None
        if hsh == hashlib.sha1(salt + created + user.token).hexdigest():
            return user
        self.flash_message("Don't be evil", 'error')
        return None

    def send_email(self, email, title, content):
        dct = dict(user=email, subject=title, body=content, subtype='html')
        webservice.post('mail/outbox', dct)


class SigninHandler(UserHandler):
    
    def head(self):
        pass

    def get(self):
        # if self.current_user:
        #     self.redirect(self.next_url)
        #     return
        self.render('signin.html')

    def post(self):
        account = self.get_argument('account', None)
        password = self.get_argument('password', None)
        password_md5 = self.get_argument('password_md5', None)
        if not (account and password_md5):
            self.flash_message('Please fill the required fields', 'error')
            self.render('signin.html')
            return
        if '@' in account:
            user = People.query.filter_by(email=account).first()
        else:
            user = People.query.filter_by(username=account).first()

        if user and user.check_password(password_md5):
            self.set_secure_cookie('user', '%s/%s' % (user.id, user.token), domain=options.cookie_domain)
            self.redirect(self.next_url)
            return
        self.flash_message('Invalid account or password', 'error')
        self.render('signin.html')


class GoogleSigninHandler(UserHandler, GoogleMixin):
    @asynchronous
    def get(self):
        if self.current_user:
            self.redirect(self.next_url)
            return
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect(ax_attrs=["email"])

    def _on_auth(self, user):
        if not user:
            self.flash_message('Google signin failed', 'error')
            self.redirect('/')
            return
        email = user["email"].lower()
        user = People.query.filter_by(email=email).first()
        if not user:
            user = People(email)
            user.password = '!'
            #: google account is a valid email
            user.role = 2
            db.session.add(user)
            db.session.commit()
            self.set_secure_cookie('user', '%s/%s' % (user.id, user.token))
            self.redirect('/account/setting')
            return

        self.set_secure_cookie('user', '%s/%s' % (user.id, user.token), domain=options.cookie_domain)
        self.redirect(self.next_url)
        return


class SignoutHandler(UserHandler):
    def get(self):
        self.clear_cookie('user', domain=options.cookie_domain)
        self.redirect(self.next_url)


class SignoutEverywhereHandler(UserHandler):
    @authenticated
    def get(self):
        user = People.query.get(self.current_user.id)
        user.token = user.create_token(16)
        db.session.add(user)
        db.session.commit()
        self.redirect(self.next_url)







#Signup
#Signup
#Signup

class SignupHandler(UserHandler, RecaptchaMixin, EmailMixin):
    def head(self):
        pass

    def get(self):
        token = self.get_argument('verify', None)
        if token:
            user = self._verify_token(token)
            if user:
                user.role = 2
                db.session.add(user)
                db.session.commit()
                self.flash_message('Your account is activated', 'info')
            self.redirect('/')
            return

        if self.current_user:
            return self.redirect(self.next_url)
        recaptcha = self.recaptcha_render()
        self.render('signup.html', username='', email='', recaptcha=recaptcha)

    @asynchronous
    def post(self):
        if self.current_user and self.get_argument('action') == 'email':
            if self.current_user.role != 1:
                self.flash_message('Your account is activated', 'info')
            else:
                self.send_signup_email(self.current_user)
            self.redirect('/')
            return
        if self.current_user:
            self.redirect(self.next_url)
            return
    
        username = self.get_argument('username', '')
        email = self.get_argument('email', '')
        email = email.lower()
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        
        
        schema = AccountSignupForm(self)
        if not schema.validate():
            self.flash_message('Username is not allowed', 'error')
            recaptcha = self.recaptcha_render()
            self.render('signup.html', username=username, email=email, recaptcha=recaptcha)
            return

        # valid = validators.username(username, min=3, max=20)
        # if not validators.username(username, min=3, max=20):
        #     self.flash_message('Username is not allowed', 'error')
        #     recaptcha = self.recaptcha_render()
        #     self.render('signup.html', username=username, email=email, recaptcha=recaptcha)
        #     return

        if not (password1 and password2):
            self.flash_message('Please fill the required fields', 'error')
            recaptcha = self.recaptcha_render()
            self.render('signup.html', username=username, email=email, recaptcha=recaptcha)
            return

        if password1 != password2:
            self.flash_message("Password doesn't match", 'error')
            recaptcha = self.recaptcha_render()
            self.render('signup.html', username=username, email=email, recaptcha=recaptcha)
            return

        if not validators.email(email):
            self.flash_message('Not a valid email address', 'error')
            recaptcha = self.recaptcha_render()
            self.render('signup.html', username=username, email=email, recaptcha=recaptcha)
            return

        people = People.query.filter_by(username=username).first()
        if people:
            #self.flash_message("This email is already registered", 'warn')
            self.flash_message("The username is already registered", 'error')
            recaptcha = self.recaptcha_render()
            self.render('signup.html', username=username, email=email, recaptcha=recaptcha)
            return

        # self.recaptcha_validate(self._on_validate)
        self._on_validate(response=None)

    def _on_validate(self, response):
        email = self.get_argument('email', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password1', None)
        # if not response:
        #     self.flash_message('Captcha not valid', 'error')
        #     recaptcha = self.recaptcha_render()
        #     self.render('signup.html', username=username, email=email, recaptcha=recaptcha)
        #     return
        user = People(username)
        user.nickname = username
        user.email = email.lower()
        user.password = user.create_password(password)
        db.session.add(user)
        db.session.commit()
        
        self.flash_message('Signup successful', 'success')
        # self.send_signup_email(user)
        self.set_secure_cookie('user', '%s/%s' % (user.id, user.token), domain=options.cookie_domain)
        self.redirect('/')  # account information
        return

    def send_signup_email(self, user):
        token = self._create_token(user)
        url = '%s/account/signup?verify=%s' % \
                (options.siteurl, token)

        template = (
            '<div>Hello <strong>%(email)s</strong></div>'
            '<br /><div>To activate your account, follow'
            '<a href="%(url)s">this link</a>.<div><br />'
            "<div>If you can't click on this link, "
            'copy and paste into your browser with: <br />'
            '%(url)s </div>'
        ) % {'email': user.email, 'url': url}
        self.send_email(user.email, 'Activate your account', template)
        self.flash_message('Please check your inbox', 'info')


class DeleteAccountHandler(UserHandler):
    @authenticated
    def post(self):
        password = self.get_argument('password', None)
        if not password:
            self.flash_message('Please fill the required fields', 'warn')
            #: TODO
            return
        if not self.current_user.check_password(password):
            self.flash_message('Invalid password', 'error')
            #: TODO
            return











class SettingHandler(UserHandler):
    @authenticated
    def get(self):
        setting = PeopleSetting.query.filter_by(people_id=self.current_user.id).first()
        if setting is None:
            setting = PeopleSetting()
        self.render('account/setting.html', setting=setting)

    @authenticated
    def post(self):
        

        website = self.get_argument('website', '')
        if website and not validators.url(website):
            self.flash_message('Website is invalid', 'error')
            self.render('account/setting.html')
            return

        user = People.query.get(self.current_user.id)

        # user.city = self.get_argument('city', '')
        # nickname = self.get_argument('nickname',None)
        # schema = AccountSettingForm(self)
        # if not schema.validate():
        #     self.flash_message('Nickname is invalid', 'error')
        #     self.render("account/setting.html")
        #     return

        # tmp_people = People.query.filter_by(nickname=nickname).first()
        # if tmp_people and tmp_people.id != self.current_user.id:
        #     self.flash_message("The nickname is already registered", 'error')
        #     self.render("account/setting.html")
        #     return


        # if nickname is None:
        #     user.nickname = user.username
        # else:
        #     user.nickname = nickname
        user.description = self.get_argument('description', '')
        user.email = self.get_argument('email', '')
        user.website = website
        db.session.add(user)
        db.session.commit()

        people_setting = PeopleSetting.query.filter_by(people_id=user.id).first()
        if people_setting is None:
            people_setting = PeopleSetting()
            people_setting.people_id = user.id

        stat_type = self.get_argument('stat_type', "0")
        if stat_type == "2":
            people_setting.stat_date = self.get_argument('stat_date')
            twins = self.get_argument('twins', 'no')
            if twins == 'yes':
                people_setting.pregnancy_babycount=2
            else:
                people_setting.pregnancy_babycount=1

        people_setting.stat_type = int(stat_type)
        db.session.add(people_setting)
        db.session.commit()

        self.clear_people_cache(user.id)
        self.flash_message("Save successful", "success")
        self.redirect('/account/setting')


class NotifyHandler(UserHandler):
    @authenticated
    def get(self):
        user = People.query.get(self.current_user.id)
        messages = Notify.query.filter_by(receiver=user.id)\
                .order_by('-id')[:20]
        messages = get_full_notifies(messages)
        self.render('notify.html', messages=messages)

        #: after render, modify user.last_notify
        user.last_notify = datetime.datetime.utcnow()
        db.session.add(user)
        messages = Notify.query.filter_by(readed='n')\
                .filter_by(receiver=self.current_user.id).all()
        for msg in messages:
            msg.readed = 'y'
            db.session.add(msg)

        db.session.commit()

    @authenticated
    def post(self):
        #: mark all as read
        messages = Notify.query.filter_by(readed='n')\
                .filter_by(receiver=self.current_user.id).all()
        for msg in messages:
            msg.readed = 'y'
            db.session.add(msg)

        db.session.commit()
        self.write({'stat': 'ok'})

    @authenticated
    def delete(self):
        #: delete all
        for msg in Notify.query.filter_by(receiver=self.current_user.id):
            db.session.delete(msg)

        db.session.commit()
        self.write({'stat': 'ok'})


class PasswordHandler(UserHandler, EmailMixin):
    """Password

    - GET: 1. form view 2. verify link from email
    - POST: 1. send email to find password. 2. change password
    """
    def get(self):
        token = self.get_argument('verify', None)
        if token and self._verify_token(token):
            self.render('account/password.html', token=token)
            return

        if not self.current_user:
            self.redirect('/account/signin')
            return
        self.render('account/password.html', token=None)

    def post(self):
        action = self.get_argument('action', None)
        if action == 'email':
            self.send_password_email()
            if not self._finished:
                self.redirect('/account/setting')
            return
        password = self.get_argument('password', None)
        if password:
            self.change_password()
            return
        self.find_password()

    def send_password_email(self):
        email = self.get_argument('email', None)
        if self.current_user:
            user = self.current_user
        elif not email:
            self.flash_message("Please fill the required fields", "error")
            self.redirect('/account/signin')
            return
        else:
            user = People.query.get_first(email=email)
            if not user:
                self.flash_message("User does not exists", "error")
                self.redirect('/account/signin')
                return

        token = self._create_token(user)
        url = '%s/account/password?verify=%s' % \
                (options.siteurl, token)

        template = (
            '<div>Hello <strong>%(email)s</strong></div>'
            '<br /><div>Find your password, follow '
            '<a href="%(url)s">this link</a>.<div><br />'
            "<div>If you can't click on this link, "
            'copy and paste into your browser with: <br />'
            '%(url)s </div>'
        ) % {'email': user.email, 'url': url}
        self.flash_message('Please check your inbox', 'info')
        self.send_email(user.email, 'Find your password', template)

    @authenticated
    def change_password(self):
        user = People.query.get_or_404(self.current_user.id)
        password = self.get_argument('password', None)
        # password_md5 = self.get_argument('password_md5', None)
        password_md5 = to_md5(to_md5(password))
        if not user.check_password(password_md5):
            self.flash_message("Invalid old password", "error")
            self.render('account/password.html', token=None)
            return
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        self._change_password(user, password1, password2)

    def find_password(self):
        token = self.get_argument('token', None)
        if not token:
            self.redirect('/account/password')
            return
        user = self._verify_token(token)
        if not user:
            self.redirect('/account/password')
            return
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        self._change_password(user, password1, password2)

    def _change_password(self, user, password1, password2):
        if password1 != password2:
            self.flash_message("Password doesn't match", 'error')
            self.render('account/password.html', token=None)
            return
        user.password = user.create_password(password1)
        user.token = user.create_token(16)
        db.session.add(user)
        db.session.commit()
        self.flash_message('Password changed', 'success')
        self.set_secure_cookie('user', '%s/%s' % (user.id, user.token), domain=options.cookie_domain)
        self.redirect('/account/setting')


class MessageHandler(UserHandler):
    @require_user
    def post(self):
        receiver = self.get_argument('username', None)
        content = self.get_argument('content', None)
        if not (receiver and content):
            self.flash_message('Please fill the required fields', 'error')
        else:
            self.create_notification(receiver, content, '', type='message')
            db.session.commit()

        self.redirect(self.next_url)

class AvatarHandler(UserHandler):
    def check_xsrf_cookie(self):
        pass
    
    @authenticated
    def get(self):

        self.render('account/setting_avatar.html', people=self.current_user)

    @authenticated
    def post(self):
        if self.request.files:
            
            file = self.request.files['avatar'][0]
            people = People.query.get(self.current_user.id)
            
            if file:
                rawname = file.get('filename')
                dstname = str(int(time.time()))+'.'+rawname.split('.').pop()
                dstname = dstname.lower()
                thbname = "thb_%d_s_%s" % (people.id, dstname)
                large_thbname = "thb_%d_l_%s" % (people.id, dstname)
                # write a file
                # src = "./static/upload/src/"+dstname
                # file(src,'w+').write(f['body'])
                
                tf = tempfile.NamedTemporaryFile(delete=False)
                tf.write(file['body'])
                tf.seek(0)
                 
                # create normal file
                # img = Image.open(src)

                avatar_file_path = options.static_avatar_path + '/' + thbname
                large_avatar_file_path = options.static_avatar_path + '/' + large_thbname
                
                img = Image.open(tf.name)

                img.thumbnail((120,120),resample=1)
                
                img.save(avatar_file_path)
                
                #large_img = Image.open(tf.name)
                #large_img.thumbnail((300,300), resample=1)
                #large_img.save(large_avatar_file_path)
                
                tf.close()
                os.remove(tf.name)
                avatar_url = options.static_avatar_url + '/' + thbname
                large_avatar_url = options.static_avatar_url + '/' + large_thbname
                people.avatar = avatar_url
                #people.large_avatar = "/static/avatar/" + large_thbname
                autocache_hdel('hs:people', people.id)
                db.session.add(people)
                db.session.commit()
                
                
                
                return self.redirect('/account/setting')

def _on_saying(xml):
    if not xml:
        raise HTTPError(500, 'Douban saying failed')
    self.write(xml)
    self.finish()

class DoubanAuthHandler(UserHandler, DoubanMixin):
    # @authenticated
    @asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth_callback))
            return
        self.authorize_redirect('http://www.meimashuo.com/account/douban/callback')
 
        

    def _on_auth_callback(self, content):
        if content:
            self.write(content)
            self.finish()
        else:
            self.write("auth failed")
            self.finish()

class DoubanAuthCallbackHandler(UserHandler, DoubanMixin):
    @authenticated
    def get(self):
        print self.request.arguments 
        self.write("douban auth ok" + str(self.request.arguments))

 

class WeiboAuthHandler(UserHandler, WeiboMixin):
    #/account/weibo/auth
    @asynchronous
    def get(self):
        try:
            if self.get_argument("code", False):
                self.get_authenticated_user(
                  redirect_uri=options.site_url + '/account/weibo/callback',
                  client_id=options.weibo_key,
                  client_secret=options.weibo_secret,
                  code=self.get_argument("code"),
                  callback=self.async_callback(self._on_login))
                return
            self.authorize_redirect(redirect_uri=options.site_url + '/account/weibo/auth',
                                client_id=options.weibo_key,
                                extra_params={"response_type": "code"})
        except Exception, err:
            logging.error(str(err))
            self.render("account/weibo_error.html")

    def _on_login(self, user):
        people = None
        print user
        if user:
            uid = user.get('id')
            token = user.get('access_token')
            profile_image = user.get('profile_image_url')
            print "uid", uid
            if uid:
                weibo = Weibo.query.filter_by(uid=uid).first()
                
                if weibo:
                    people = People.query.filter_by(id=weibo.people_id).first()
                    if weibo.token != token:
                        weibo.token = token
                        weibo.profile_image = profile_image
                        db.session.add(weibo)
                        db.session.commit()
                else:
                    weibo = Weibo()
                    weibo.uid = uid
                    weibo.name = user.get('name')
                    weibo.screen_name = user.get('screen_name')
                    weibo.domain = user.get('domain')
                    weibo.avatar_small = user.get('profile_image_url')
                    weibo.avatar_large = user.get('avatar_large')
                    weibo.province = user.get('province')
                    weibo.city = user.get('city')
                    weibo.location = user.get('location')
                    weibo.token = user.get('access_token')
                    weibo.session_expires = user.get('session_expires')


                if people is None:
                    # people = People(People.create_token(8))
                    # people.password = People.create_password(People.create_token(8))
                    # people.token = People.create_token(8)

                    # db.session.add(people)
                    # db.session.commit()
                    # weibo.people_id = people.id
                    print "insert weibo uid", weibo.uid
                    db.session.add(weibo)
                    db.session.commit()
                    print "after weibo uid", weibo.uid

                    self.set_secure_cookie('setting_user', '%s/%s' % (weibo.id, "weibo"), domain=options.cookie_domain)
                    return self.render("account/setting_signup.html", weibo_id=weibo.id, username=weibo.name)
                else:

                    self.set_secure_cookie('user', '%s/%s' % (people.id, people.token), domain=options.cookie_domain)
                    return self.redirect("/")



        self.render("account/weibo_error.html")

    

class WeiboAuthCallbackHandler(UserHandler, DoubanMixin):
    #/account/weibo/callback
    @authenticated
    def get(self):
        print self.request.arguments 
        self.write("douban auth ok" + str(self.request.arguments))



class GithubSignupHandler(UserHandler, GithubMixin):
    @asynchronous
    def get(self):
        logging.info(self.request)
        if self.get_argument("code", None):
            self.get_authenticated_user(
                client_id=options.github_key,
                client_secret= options.github_secret,
                redirect_uri= options.github_redirect_uri,
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_auth)
            )
            return

        if self.get_argument("error", None):
            raise HTTPError(403, self.get_argument("error"))

        self.authorize_redirect(
            client_id = options.github_key,
            client_secret = options.github_secret,
            redirect_uri = options.github_redirect_uri,
        )

    def _on_auth(self, user):
        logging.info(user)
        if not user:
            raise HTTPError(500, "GitHub auth failed")
        uid = user.get('id')
        login = user.get('login')
        if uid:
            github = GitHub.query.filter_by(uid=uid).first()
            
            if github:
                people = People.query.filter_by(id=github.people_id).first()
                if github.token != token:
                    github.token = token
                    github.profile_image = profile_image
                    db.session.add(github)
                    db.session.commit()
            else:
                github = GitHub()
                github.uid = uid
                github.name = user.get('login')
                github.screen_name = user.get('name')
                github.avatar_small = user.get('avatar_url')
                github.avatar_large = user.get('avatar_url')
                github.location = user.get('location')
                github.token = user.get('access_token')
                #github.session_expires = user.get('session_expires')
                if people is None:
                    oldpeple = People.query.filter_by(username=login).first()
                    if oldpeple:
                        #set new username
                        self.set_secure_cookie('setting_user', '%s/%s' % (github.id, "github"), domain=options.cookie_domain)
                        return self.render("account/setting_signup.html", social_id=github.id, username=github.name)



        self.render("account/social_error.html")
        #self.redirect("/signup/github")


# class GithubSignupHandler(UserHandler):
    
#     def get(self):
#         return self.render("account/signup_github.html")
    



class SettingRenameGithubHandler(UserHandler):
    def post(self, id):
        setting_user = self.get_secure_cookie("setting_user")
        if not setting_user:
            return self.render_error(403)
        try:
            account_id, token = setting_user.split('/')
            account_id = int(account_id)
        except:
            self.clear_cookie("setting_user")
            # return self.render("account/social_error.html")
            return render_error(404)
        id = int(id)
        if account_id != id:
            return self.render_error(403)


        username = self.get_argument('username', None)
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        if not username:
            self.flash_message('Please fill the required fields', 'error')
            self.render("account/signup_github.html", social_id=id, username=username)
            return
      

        if not validators.username(username):
            self.flash_message('Username is invalid', 'error')
            self.render("account/signup_github.html", social_id=id, username=username)
            return

        tmp_people = People.query.filter_by(username=username).first()
        if tmp_people:
            self.flash_message("The username is already registered", 'error')
            self.render("account/signup_github.html", social_id=id, username=username)
            return

        github = GitHub.query.filter_by(id=id).first_or_404()
        people = People(People.create_token(8))
        people.username = username
        people.nickname = username
        people.password = None
        people.token = People.create_token(8)
        people.email = github.email
        db.session.add(people)
        db.session.commit()
        
        github.people_id = people.id
        db.session.add(github)
        db.session.commit()


        self.flash_message("Setting account successful", 'success')
        self.set_secure_cookie('user', '%s/%s' % (people.id, people.token), domain=options.cookie_domain)
        self.clear_cookie("setting_user")
        self.redirect('/')


class SettingSignupHandler(UserHandler):
    

    def post(self, id):
        setting_user = self.get_secure_cookie("setting_user")
        if not setting_user:
            return self.render_error(403)
        try:
            account_id, token = setting_user.split('/')
            account_id = int(account_id)
        except:
            self.clear_cookie("setting_user")
            return self.render("account/weibo_error.html")
            # return render_error(403)
        id = int(id)
        if account_id != id:
            return self.render_error(403)


        username = self.get_argument('username', None)
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)
        if not username or not (password1 and password2) :
            self.flash_message('Please fill the required fields', 'error')
            self.render("account/setting_signup.html", weibo_id=id, username=username)
            return
        if password1 != password2 :
            self.flash_message("Password doesn't match", 'error')
            self.render("account/setting_signup.html", weibo_id=id, username=username)
            return

        if not validators.username(username):
            self.flash_message('Username is invalid', 'error')
            self.render("account/setting_signup.html", weibo_id=id, username=username)
            return

        tmp_people = People.query.filter_by(username=username).first()
        if tmp_people:
            self.flash_message("The username is already registered", 'error')
            self.render("account/setting_signup.html", weibo_id=id, username=username)
            return

        people = People(People.create_token(8))
        people.username = username
        people.nickname = username
        people.password = People.create_password(password1)
        people.token = People.create_token(8)

        db.session.add(people)
        db.session.commit()

        weibo = Weibo.query.filter_by(id=id).first_or_404()
        weibo.people_id = people.id
        db.session.add(weibo)
        db.session.commit()


        self.flash_message("Setting account successful", 'success')
        self.set_secure_cookie('user', '%s/%s' % (people.id, people.token), domain=options.cookie_domain)
        self.clear_cookie("setting_user")
        self.redirect('/')


app_handlers = [
    ('/signup', SignupHandler),
    ('/signup/github', GithubSignupHandler),
    ('/callback/github', GithubSignupHandler),
    ('/rename/github/(\d+)', SettingRenameGithubHandler),

    ('/signin', SigninHandler),
    ('/signin/google', GoogleSigninHandler),
    ('/signout', SignoutHandler),
    ('/setting', SettingHandler),
    ('/setting/avatar', AvatarHandler),
    ('/setting/signup/(\d+)', SettingSignupHandler),

    ('/signout/everywhere', SignoutEverywhereHandler),
    ('/delete', DeleteAccountHandler),
    ('/notify', NotifyHandler),
    ('/password', PasswordHandler),
    ('/message', MessageHandler),
    # ('/douban/auth', DoubanAuthHandler),
    # ('/douban/callback', DoubanAuthCallbackHandler),
    # ('/weibo/auth', WeiboAuthHandler),
    # ('/weibo/callback', WeiboAuthCallbackHandler),

]


class RecentPeoplesModule(UIModule):
    def render(self):
        users = People.query.order_by('-id').limit(12)
        return self.render_string('module/people_cell.html', users=users)

class UserModule(UIModule):
    """UserModule

    This module contains topic and reply count,
    in this case, it is located in topic app
    """
    def render(self, user_id):
        user = People.query.get_first(id=user_id)
        if not user:
            return ''

        return self.render_string('module/user.html', user=user)

class ProfileHeaderModule(UIModule):
    
    def render(self, people):
        if not people:
            return ''
       
        return self.render_string('module/profile_header.html', people=people)

class ProfileSidebarModule(UIModule):
    def render(self, people):
        if not people:
            return ''
        if people == self.current_user:
            people.is_master = True
        else:
            people.is_master = False

        return self.render_string('module/profile_sidebar.html', people=people)

class SigninSidebarModule(UIModule):
    def render(self):
        return self.render_string('module/signin_sidebar.html')


class TemplateModule(UIModule):
    def render(self, tmpl_file, **kargs):
        return self.render_string(tmpl, **kargs)

app_modules = {
    'RecentPeoples': RecentPeoplesModule,
    'User': UserModule,
    'ProfileHeader': ProfileHeaderModule,
    'ProfileSidebar': ProfileSidebarModule, 
    'Template': TemplateModule,
    'SigninSidebar': SigninSidebarModule
}

app = DojangApp('account', __name__, handlers=app_handlers, ui_modules=app_modules)


