# -*- coding: utf-8 -*-
from dojang.app import DojangApp
from dojang.database import db


from app.account.decorators import require_user, apiauth
from app.account.lib import SimpleApiHandler, UserHandler	
from app.lib.filters import markdown

from .models import Wist, WistContent, WistStar


class AllWistsHandler(UserHandler):

    def get(self):
        p = self.get_argument('p', 1)
        limit = 30
        pagination = Wist.query.filter_by(fork_root_id=0).order_by('-id').paginate(p, limit)

        self.render('wist/all_wist.html', pagination=pagination)


class ShowWistHandler(UserHandler):
    def get(self, id):
        wist = Wist.query.filter_by(id=id).first_or_404()
        if wist.content:
            wist_content = wist.content
        else:
            wist_content = WistContent()

        return self.render('wist/show_wist.html', wist=wist, content=wist_content)


class NewWistHandler(UserHandler):
    @require_user
    def get(self):
        wist = Wist()

        self.render('wist/create_wist.html', title="", content="")

    @require_user
    def post(self):
        content = self.get_argument('content', None)
        if not content or content == "":
            self.flash_message('Please fill the required fields', 'error')
            return self.render('wist/create_wist.html', title="", content="")
        wist = Wist()
        wist.people_id = self.current_user.id
        wist.fork_root_id=0
        wist.fork_from_id=0
        wc = WistContent()
        
        wist.tags = self.get_argument('tags', None)
        wist.username = self.current_user.username

        if content:
            content_arr = content.split('\n',1)
            title = content_arr[0]
            wist.title = title.lstrip(' #')
            wc.content = content
            nospace_content = content.lstrip()
            if nospace_content[0] != '#':
                nospace_content = '#'+nospace_content
            wc.content_html = markdown(nospace_content)
            wist.content = wc
        db.session.add(wist)
        db.session.add(wc)
        db.session.commit()

        return self.redirect('/%s/wist/%d' % (wist.username, wist.id))



class EditWistHandler(UserHandler):
    @require_user
    def get(self, id):
        wist = Wist.query.filter_by(id=id).first_or_404()
        self.check_permission(wist)
        wist_content = WistContent.query.filter_by(id=wist.content_id).first()
        content = None
        if wist_content:
            content = wist_content.content
        self.render('wist/edit_wist.html', wist=wist, content=content)

    @require_user
    def post(self, id):
        content = self.get_argument('content', None)
        
        wist = Wist.query.filter_by(id=id).first_or_404()
        wc = WistContent.query.filter_by(id=wist.content_id).first()
        if wc is None:
            wc = WistContent()
            wist.content = wc
        
        if not content:
            self.flash_message('Please fill the required fields', 'error')
            return self.render('wist/edit_wist.html', wist=wist, content=content)


        wist.tags = self.get_argument('tags', None)

        if content:
            content_arr = content.split('\n',1)
            title = content_arr[0]
            wist.title = title.lstrip(' #')
            wc.content = content
            # wc.content_html = markdown(content)
            nospace_content = content.lstrip()
            if nospace_content[0] != '#':
                nospace_content = '#'+nospace_content
            wc.content_html = markdown(nospace_content)
        db.session.add(wist)
        db.session.add(wc)
        db.session.commit()

        return self.redirect('/%s/wist/%d' % (wist.username, wist.id))


class ForkWistHandler(UserHandler):
    @require_user
    def get(self, id):
        forked_root_wist = None
        wist = Wist.query.filter_by(id=id).first_or_404()
        if self.current_user.id == wist.people_id:
            return self.redirect('/%s/wist/%d' % (wist.username, wist.id))
        if wist.fork_root_id != 0:
            old_wist = Wist.query.filter_by(people_id=self.current_user.id, fork_root_id=wist.fork_root_id).first()
            if old_wist:
                return self.redirect('/%s/wist/%d' % (old_wist.username, old_wist.id))
            forked_root_wist = Wist.query.filter_by(id=wist.fork_root_id).first()
            if forked_root_wist and forked_root_wist.people_id == self.current_user.id:
                return self.redirect('/%s/wist/%d' % (forked_root_wist.username, forked_root_wist.id))

        old_fork_wist = Wist.query.filter_by(people_id=self.current_user.id, fork_root_id=id).first()
        if old_fork_wist:
            return self.redirect('/%s/wist/%d' % (old_fork_wist.username, old_fork_wist.id))
        

        wist_content = WistContent.query.filter_by(id=wist.content_id).first_or_404()
        new_wist = Wist()
        new_wist.people_id = self.current_user.id
        new_wist.username = self.current_user.username
        if wist.fork_root_id == 0:
            new_wist.fork_root_id = wist.id
            forked_root_wist = wist
            

        else:
            new_wist.fork_root_id = wist.fork_root_id

        if forked_root_wist:
            print forked_root_wist.id , forked_root_wist.fork_count, "fork count +1"
            forked_root_wist.fork_count = Wist.fork_count + 1
            db.session.add(forked_root_wist)
        new_wist.fork_from_id = wist.id
        new_wist.fork_from_username = wist.username
        new_wist.title = wist.title
        new_wist.tags = wist.tags

        new_content = WistContent()
        new_content.content = wist_content.content
        new_content.content_html = wist_content.content_html
        new_wist.content = new_content
        wist.fork_count
        db.session.add(new_wist)
        db.session.add(new_content)
        db.session.commit()

        return self.redirect('/%s/wist/%d' % (new_wist.username, new_wist.id))


    def post(self, id):
        wist = Wist.query.filter_by(id=id).first_or_404()
        wc = WistContent.query.filter_by(id=wist.content_id).first_or_404()
        wist.username = self.current_user.username
        content = self.get_argument('content', None)
        wist.tag = self.get_argument('tag', None)

        if content:
            content_arr = content.split('\n',1)
            title = content_arr[0]
            wist.title = content_arr[0]
            wc.content = content
            # wc.content_html = markdown(content)
            nospace_content = content.lstrip()
            if nospace_content[0] != '#':
                nospace_content = '#'+nospace_content
            wc.content_html = markdown(nospace_content)
        db.session.add(wist)
        db.session.add(wc)
        db.session.commit()

        return self.redirect('/%s/wist/%d' % (wist.username, wist.id))


class StarWistHandler(SimpleApiHandler):
    @apiauth
    def post(self, id):
        wist = Wist.query.filter_by(id=id).first()
        count = wist.star_count
        wist_star = WistStar.query.filter_by(wist_id=id, people_id=self.current_user.id).first()
        if wist_star:
            return self.render_json(data={'count':count+1})
        
        wist.star_count = Wist.star_count+1
        wist_star = WistStar()
        wist_star.people_id = self.current_user.id
        wist_star.wist_id = wist.id
        db.session.add(wist_star)
        db.session.add(wist)
        db.session.commit()
        return self.render_json(data={'count':count+1})

class UnstarWistHandler(SimpleApiHandler):
    @apiauth
    def post(self, id):
        wist = Wist.query.filter_by(id=id).first()
        count = wist.star_count
        wist_star = WistStar.query.filter_by(wist_id=id, people_id=self.current_user.id).first()
        if wist_star is None:
            return self.render_json(data={'count':count-1})
        
        wist.star_count = Wist.star_count-1
        if count-1<0:
            count = 0
        db.session.delete(wist_star)
        db.session.add(wist)
        db.session.commit()
        return self.render_json(data={'count':count-1})


app_handlers = [
    ('', AllWistsHandler),
    ('/new', NewWistHandler),
    ('/(\d+)', ShowWistHandler),
    ('/(\d+)/edit', EditWistHandler),
    ('/(\d+)/fork', ForkWistHandler),
    ('/(\d+)/star', StarWistHandler),
    ('/(\d+)/unstar', UnstarWistHandler),
       
]


app_modules = {
    
}

app = DojangApp(
    'wist', __name__, handlers=app_handlers, ui_modules=app_modules
)