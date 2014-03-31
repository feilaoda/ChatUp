from datetime import datetime
import math

from app.account.models import People
from app.node.models import Node
from dojang.cache import get_cache_list
from tornado.options import options


def get_user_id_list(topics):
    for t in topics:
        yield t.people_id


def get_full_thread(thread):
    users = get_cache_list(People, get_user_id_list([topic]), 'hs:people')
    if thread.people_id in users.keys():
        thread.people = users[topic.people_id]

    return thread

def get_full_threads(threads):
    users = get_cache_list(People, get_user_id_list(threads), 'hs:people')
    user_ids = users.keys()
    for thread in threads:
        if thread.people_id in user_ids:
            thread.people = users[thread.people_id]
            yield thread
