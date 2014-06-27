# Makefile for project June

.PHONY: clean-pyc clean-build docs

# Variables for June
CONFIG = settings.py
PROJSERVER = iosplay.com:/home/feilaoda/www/static
STATIC = ../static
HOME = ..

# Development
server:
	app/run.py --settings=$(CONFIG)


database:
	app/tools.py --settings=$(CONFIG) createdb


admin:
	app/tools.py --settings=$(CONFIG) createuser

# Common Task
clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {rm} +
	find . -name '*~' -exec rm -f {} +

# Sphinx Documentation
docs:
	$(MAKE) -C docs html


# Deployment
upload:
	rsync -av --del --exclude=*.pyc june/_static/* $(PROJSERVER)


# static, required livereload
install_static: install_image install_js install_css

install_js:
	livereload lib_js
	livereload editor_js
	livereload site_js
	livereload topic_js

install_css:
	livereload site_css

install_image:
	if [ ! -d $(STATIC)/img ]; then mkdir -p $(STATIC)/img; fi
	cp -r assets/img/* $(STATIC)/img/


# Git
github:
	git push origin develop


static: css  static_image js


css2:
	if [ ! -d $(STATIC)/assets/v2/css ]; then mkdir -p $(STATIC)/assets/v2/css; fi
	#lessc --compress $(HOME)/vendor/stylesheets/bootstrap/bootstrap.less > $(STATIC)/assets/v2/css/vendor.min.css
	lessc --compress $(HOME)/static/stylesheets/base.less > $(STATIC)/assets/v2/css/application.min.css
	lessc --compress $(HOME)/static/stylesheets/box.less >> $(STATIC)/assets/v2/css/application.min.css
	lessc --compress $(HOME)/static/stylesheets/topic.less >> $(STATIC)/assets/v2/css/application.min.css
	lessc --compress $(HOME)/static/stylesheets/blog.less >> $(STATIC)/assets/v2/css/application.min.css
	lessc --compress $(HOME)/static/stylesheets/shot.less >> $(STATIC)/assets/v2/css/application.min.css
	lessc --compress $(HOME)/static/stylesheets/footer.less >> $(STATIC)/assets/v2/css/application.min.css
	lessc --compress $(HOME)/static/stylesheets/front.less >> $(STATIC)/assets/v2/css/application.min.css

	lessc --compress $(HOME)/static/stylesheets/mobile.less > $(STATIC)/assets/v2/css/mobile.min.css
	lessc --compress $(HOME)/static/stylesheets/admin.less > $(STATIC)/assets/v2/css/admin.min.css


css:
	if [ ! -d $(STATIC)/assets/css ]; then mkdir -p $(STATIC)/assets/css; fi
	lessc --compress $(HOME)/app/vendor/stylesheets/bootstrap-3.1.0/less/bootstrap.less > $(STATIC)/assets/css/v3/vendor.min.css
	lessc --compress $(HOME)/static/stylesheets/application.less > $(STATIC)/assets/css/v3/application.min.css
	cssshrink $(STATIC)/assets/css/v3/vendor.min.css > $(STATIC)/assets/css/v3/application.css
	cssshrink $(STATIC)/assets/css/v3/application.min.css >> $(STATIC)/assets/css/v3/application.css
	cssshrink $(STATIC)/assets/css/v3/application.css > $(STATIC)/assets/css/v3/stylesheets.min.css
	#cat $(HOME)/vendor/waterfall/css/reset.css > $(STATIC)/assets/css/waterfall.min.css
	#cat $(HOME)/vendor/waterfall/css/main.css >> $(STATIC)/assets/css/waterfall.min.css
	#cat $(HOME)/vendor/waterfall/css/woo.css >> $(STATIC)/assets/css/waterfall.min.css
	#cat $(HOME)/vendor/waterfall/css/gotop.css >> $(STATIC)/assets/css/waterfall.min.css
	#cat $(HOME)/vendor/waterfall/css/pagine.css >> $(STATIC)/assets/css/waterfall.min.css
	#cat $(HOME)/vendor/waterfall/css/resize.css >> $(STATIC)/assets/css/waterfall.min.css


	lessc --compress $(HOME)/static/stylesheets/mobile.less > $(STATIC)/assets/css/mobile.min.css
	lessc --compress $(HOME)/static/stylesheets/admin.less > $(STATIC)/assets/css/admin.min.css


static_image:
	if [ ! -d $(STATIC)/assets/img ]; then mkdir -p $(STATIC)/assets/img; fi
	cp -r assets/img/* $(STATIC)/img/

js: libjs



libjs:
	if [ ! -d $(STATIC)/assets/js ]; then mkdir -p $(STATIC)/assets/js; fi

	uglifyjs $(HOME)/app/vendor/javascripts/jquery/jquery.min.js > $(STATIC)/assets/js/vendor.min.js
#uglifyjs -nc $(HOME)/vendor/javascripts/jquery/jquery.ui.min.js > $(STATIC)/assets/js/jquery.ui.min.js

#uglifyjs -nc $(HOME)/vendor/javascripts/bootstrap/bootstrap-dropdown.js >> $(STATIC)/assets/js/vendor.min.js
#uglifyjs -nc $(HOME)/vendor/javascripts/bootstrap/bootstrap-modal.js >> $(STATIC)/assets/js/vendor.min.js
#uglifyjs -nc $(HOME)/vendor/javascripts/bootstrap/bootstrap-tab.js >> $(STATIC)/assets/js/vendor.min.js
#uglifyjs -nc $(HOME)/vendor/javascripts/bootstrap/bootstrap-datepicker.js >> $(STATIC)/assets/js/vendor.min.js

#uglifyjs -nc $(HOME)/static/javascripts/base.js > $(STATIC)/assets/js/application.min.js
# uglifyjs -nc $(HOME)/static/javascripts/pin.js >> $(STATIC)/assets/js/application.min.js
# uglifyjs -nc $(HOME)/static/javascripts/movie.js >> $(STATIC)/assets/js/application.min.js
# uglifyjs -nc $(HOME)/static/javascripts/english.js >> $(STATIC)/assets/js/application.min.js
# uglifyjs -nc $(HOME)/vendor/waterfall/js/browser.js > $(STATIC)/assets/js/waterfall.min.js
# uglifyjs -nc $(HOME)/vendor/waterfall/js/history.js >> $(STATIC)/assets/js/waterfall.min.js
# uglifyjs -nc $(HOME)/vendor/waterfall/js/template.min.js >> $(STATIC)/assets/js/waterfall.min.js
# uglifyjs -nc $(HOME)/vendor/waterfall/js/tabswitch.js >> $(STATIC)/assets/js/waterfall.min.js
# uglifyjs -nc $(HOME)/vendor/waterfall/js/woo.js >> $(STATIC)/assets/js/waterfall.min.js
# uglifyjs -nc $(HOME)/vendor/waterfall/js/masnunit.js >> $(STATIC)/assets/js/waterfall.min.js

# uglifyjs -nc $(HOME)/static/javascripts/yepnope.js > $(STATIC)/assets/js/finance.min.js
# uglifyjs -nc $(HOME)/static/javascripts/flotr2/flotr2.min.js >> $(STATIC)/assets/js/finance.min.js
# uglifyjs -nc $(HOME)/static/javascripts/flotr2/js/plugins/handles.js >> $(STATIC)/assets/js/finance.min.js
# uglifyjs -nc $(HOME)/static/javascripts/bonzo/bonzo.min.js >> $(STATIC)/assets/js/finance.min.js
# uglifyjs -nc $(HOME)/static/javascripts/envision.min.js >> $(STATIC)/assets/js/finance.min.js
# uglifyjs -nc $(HOME)/static/javascripts/soundmanager2.min.js >> $(STATIC)/assets/js/finance.min.js
# uglifyjs -nc $(HOME)/static/javascripts/bitfinance.js >> $(STATIC)/assets/js/finance.min.js
# uglifyjs -nc $(HOME)/static/javascripts/financechart.js >> $(STATIC)/assets/js/finance.min.js

# uglifyjs -nc $(HOME)/static/javascripts/socket.io.js > $(STATIC)/assets/js/socket.io.min.js

# uglifyjs -nc $(HOME)/static/javascripts/topic.js >> $(STATIC)/assets/js/topic.min.js




editorjs:
	if [ ! -d $(STATIC)/js ]; then mkdir -p $(STATIC)/js; fi
	#uglifyjs -nc assets/js/marked.js > $(STATIC)/js/editor.js
	#uglifyjs -nc assets/js/editor.js >> $(STATIC)/js/editor.js
	uglifyjs -nc assets/js/post-editor.js >> $(STATIC)/js/editor.js

topicjs:
	if [ ! -d $(STATIC)/js ]; then mkdir -p $(STATIC)/js; fi
	uglifyjs -nc $(STATIC)/assets/js/jquery.caret.js > $(STATIC)/js/topic.js
	uglifyjs -nc $(STATIC)/assets/js/jquery.atwho.js >> $(STATIC)/js/topic.js
	uglifyjs -nc $(STATIC)/assets/js/topic.js >> $(STATIC)/js/topic.js
	uglifyjs -nc $(STATIC)/assets/js/post-editor.js >> $(STATIC)/js/topic.js

sitejs:
	if [ ! -d $(STATIC)/js ]; then mkdir -p $(STATIC)/js; fi
	uglifyjs -nc $(STATIC)/assets/js/site.js > $(STATIC)/js/site.js


adminjs:
	if [ ! -d $(STATIC)/js ]; then mkdir -p $(STATIC)/js; fi
	uglifyjs -nc $(STATIC)/assets/js/jquery.ui.core.js > $(STATIC)/js/admin.js
	uglifyjs -nc $(STATIC)/assets/js/jquery.ui.widget.js >> $(STATIC)/js/admin.js
	uglifyjs -nc $(STATIC)/assets/js/jquery.ui.mouse.js >> $(STATIC)/js/admin.js
	uglifyjs -nc $(STATIC)/assets/js/jquery.ui.sortable.js >> $(STATIC)/js/admin.js
