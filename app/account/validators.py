# coding: utf-8
import re
import hashlib
from formencode.validators import FancyValidator
from formencode.api import *

_ = lambda s: s

def regex(pattern, data, flags=0):
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, flags)

    return pattern.match(data)


def email(data):
    pattern = r'^.+@[^.].*\.[a-z]{2,10}$'
    return regex(pattern, data, re.IGNORECASE)


def url(data):
    pattern = (
        r'(?i)^((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
        r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
        r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))$')
    return regex(pattern, data, re.IGNORECASE)




_english_character_re = re.compile(u"^[a-zA-Z0-9]+$")
_chinese_character_re = re.compile(u"^[a-zA-Z0-9\u4e00-\u9fa5]+$")
def username(data, min=2, max=20):
    if data is None:
        return False
    try:
        length = len(data.decode('utf8'))
        if length < min or  length > max:
            return False
    except TypeError:
        return False
    
    m =  _english_character_re.match(data)
    if m is None:
        return False
    return True
   

def nickname(data, min=2, max=20):
    if data is None:
        return False
    try:
        length = len(data.decode('utf8'))
        if length < min or  length > max:
            return False
    except TypeError:
        return False#'Nickname is not allowed'

    
    m =  _chinese_character_re.search(data)
    print m
    if m is None:
        return False#'Nickname is not allowed'
    return True


class Utf8MaxLength(FancyValidator):
    """
    Invalid if the value is longer than `maxLength`.  Uses len(),
    so it can work for strings, lists, or anything with length.

    Examples::

        >>> max5 = MaxLength(5)
        >>> max5.to_python('12345')
        '12345'
        >>> max5.from_python('12345')
        '12345'
        >>> max5.to_python('123456')
        Traceback (most recent call last):
          ...
        Invalid: Enter a value less than 5 characters long
        >>> max5(accept_python=False).from_python('123456')
        Traceback (most recent call last):
          ...
        Invalid: Enter a value less than 5 characters long
        >>> max5.to_python([1, 2, 3])
        [1, 2, 3]
        >>> max5.to_python([1, 2, 3, 4, 5, 6])
        Traceback (most recent call last):
          ...
        Invalid: Enter a value less than 5 characters long
        >>> max5.to_python(5)
        Traceback (most recent call last):
          ...
        Invalid: Invalid value (value with length expected)
    """

    __unpackargs__ = ('maxLength',)

    messages = dict(
        tooLong=_('Enter a value less than %(maxLength)i characters long'),
        invalid=_('Invalid value (value with length expected)'))

    def validate_python(self, value, state):
        try:
            if value and len(value.decode('utf8')) > self.maxLength:
                raise Invalid(
                    self.message('tooLong', state,
                        maxLength=self.maxLength), value, state)
            else:
                return None
        except TypeError:
            raise Invalid(
                self.message('invalid', state), value, state)

class Utf8MinLength(FancyValidator):
    """
    Invalid if the value is longer than `maxLength`.  Uses len(),
    so it can work for strings, lists, or anything with length.

    Examples::

        >>> max5 = MaxLength(5)
        >>> max5.to_python('12345')
        '12345'
        >>> max5.from_python('12345')
        '12345'
        >>> max5.to_python('123456')
        Traceback (most recent call last):
          ...
        Invalid: Enter a value less than 5 characters long
        >>> max5(accept_python=False).from_python('123456')
        Traceback (most recent call last):
          ...
        Invalid: Enter a value less than 5 characters long
        >>> max5.to_python([1, 2, 3])
        [1, 2, 3]
        >>> max5.to_python([1, 2, 3, 4, 5, 6])
        Traceback (most recent call last):
          ...
        Invalid: Enter a value less than 5 characters long
        >>> max5.to_python(5)
        Traceback (most recent call last):
          ...
        Invalid: Invalid value (value with length expected)
    """

    __unpackargs__ = ('minLength',)

    messages = dict(
        tooShort=_('Enter a value less than %(minLength)i characters long'),
        invalid=_('Invalid value (value with length expected)'))

    def validate_python(self, value, state):
        try:
            if value and len(value.decode('utf8')) < self.minLength:
                raise Invalid(
                    self.message('tooShort', state,
                        minLength=self.minLength), value, state)
            else:
                return None
        except TypeError:
            raise Invalid(
                self.message('invalid', state), value, state)


class Utf8String(FancyValidator):
    """
    Converts things to string, but treats empty things as the empty string.

    Also takes a `max` and `min` argument, and the string length must fall
    in that range.

    Also you may give an `encoding` argument, which will encode any unicode
    that is found.  Lists and tuples are joined with `list_joiner`
    (default ``', '``) in ``from_python``.

    ::

        >>> String(min=2).to_python('a')
        Traceback (most recent call last):
            ...
        Invalid: Enter a value 2 characters long or more
        >>> String(max=10).to_python('xxxxxxxxxxx')
        Traceback (most recent call last):
            ...
        Invalid: Enter a value not more than 10 characters long
        >>> String().from_python(None)
        ''
        >>> String().from_python([])
        ''
        >>> String().to_python(None)
        ''
        >>> String(min=3).to_python(None)
        Traceback (most recent call last):
            ...
        Invalid: Please enter a value
        >>> String(min=1).to_python('')
        Traceback (most recent call last):
            ...
        Invalid: Please enter a value

    """

    min = None
    max = None
    not_empty = None
    encoding = None
    list_joiner = ', '

    messages = dict(
        tooLong=_('Enter a value not more than %(max)i characters long'),
        tooShort=_('Enter a value %(min)i characters long or more'))

    def __initargs__(self, new_attrs):
        if self.not_empty is None and self.min:
            self.not_empty = True

    def _to_python(self, value, state):
        raise Invalid(
                self.message('tooLong', state, max=self.max), value, state)
        if value is None:
            value = ''
        elif not isinstance(value, basestring):
            try:
                value = str(value)
            except UnicodeEncodeError:
                value = unicode(value)
        if self.encoding is not None and isinstance(value, unicode):
            value = value.encode(self.encoding)
        return value

    def _from_python(self, value, state):
        if value is None:
            value = ''
        elif not isinstance(value, basestring):
            if isinstance(value, (list, tuple)):
                value = self.list_joiner.join([
                    self._from_python(v, state) for v in value])
            try:
                value = str(value)
            except UnicodeEncodeError:
                value = unicode(value)
        if self.encoding is not None and isinstance(value, unicode):
            value = value.encode(self.encoding)
        if self.strip:
            value = value.strip()
        return value

    def validate_python(self, value, state):
        
        if self.max is None and self.min is None:
            return
        if value is None:
            value = ''
        elif not isinstance(value, basestring):
            try:
                value = str(value)
            except UnicodeEncodeError:
                value = unicode(value)
        if self.max is not None and len(value.decode('utf8')) > self.max:
            raise Invalid(
                self.message('tooLong', state, max=self.max), value, state)
        if self.min is not None and len(value) < self.min:
            raise Invalid(
                self.message('tooShort', state, min=self.min), value, state)

    def empty_value(self, value):
        return ''


        