# -*- coding: utf-8 -*-


import formencode
from dojang.form import FormSchema
from app.account import validators


class NewTopicForm(FormSchema):
    title = formencode.All(validators.Utf8MaxLength(150, messages={"tooLong":u'标题太长，不能超过150个字'}),validators.Utf8MinLength(5, messages={"tooShort":u'标题太短，不能少于5个字'}),formencode.validators.String(not_empty=True, strip=True, messages={"empty":u"标题不能为空，填点内容吧"}))
