import math
from datetime import datetime
from tornado.options import options
from dojang.cache import get_cache_list
from app.account.models import People

#from .models import Node


def get_user_id_list(topics):
    for t in topics:
        yield t.people_id
        if t.last_reply_by:
            yield t.last_reply_by
def get_full_topic(topic):
    users = get_cache_list(People, get_user_id_list([topic]), 'hs:people')
    if topic.people_id in users.keys():
        topic.people = users[topic.people_id]

    return topic

def get_full_topics(topics):
    users = get_cache_list(People, get_user_id_list(topics), 'hs:people')
    user_ids = users.keys()
    for topic in topics:
        if topic.people_id in user_ids:
            topic.people = users[topic.people_id]
            # if topic.last_reply_by:
            #     topic.last_replyer = users[topic.last_reply_by]
            # else:
            #     topic.last_replyer = None
            yield topic

# def get_all_topics(topics):
#     users = get_cache_list(People, get_user_id_list(topics), 'hs:people')
#     nodes = get_cache_list(Node, (t.node_id for t in topics), 'sp:node')
#     user_ids = users.keys()
#     node_ids = nodes.keys()

#     for topic in topics:
#         if topic.people_id in user_ids and topic.node_id in node_ids:
#             topic.people = users[topic.people_id]
#             if topic.last_reply_by:
#                 topic.last_replyer = users[topic.last_reply_by]
#             else:
#                 topic.last_replyer = None
#             topic.node = nodes[topic.node_id]
#             yield topic

def get_replier_id_list(replies):
    if replies is None or len(replies) == 0:
        return []
    ids = []
    for r in replies:
        #yield r.people_id
        ids.append(r.people_id)
    return ids

def get_full_replies(replies):
    users = get_cache_list(People, get_replier_id_list(replies), 'hs:people')
    user_ids = users.keys()
    for reply in replies:
        if reply.people_id in user_ids:
            reply.people = users[reply.people_id]
            yield reply


def reply_impact_for_topic(topic, reputation):
    if reputation < 2:
        return 0
    factor = int(options.reply_factor_for_topic)
    time_factor = int(options.reply_time_factor)
    time = datetime.utcnow() - topic.created
    factor += time.days * time_factor
    return factor * int(math.log(reputation))


def up_impact_for_topic(reputation):
    if reputation < 2:
        return 0
    factor = int(options.up_factor_for_topic)
    return factor * int(math.log(reputation))


def down_impact_for_topic(reputation):
    if reputation < 2:
        return 0
    factor = int(options.down_factor_for_topic)
    return factor * int(math.log(reputation))


def up_impact_for_user(reputation):
    if reputation < 2:
        return 0
    factor = int(options.up_factor_for_user)
    impact = factor * int(math.log(reputation))
    return min(impact, int(options.up_max_for_user))


def down_impact_for_user(reputation):
    if reputation < 2:
        return 0
    factor = int(options.down_factor_for_user)
    impact = factor * int(math.log(reputation))
    return min(impact, int(options.down_max_for_user))


def accept_reply_impact_for_user(reputation):
    if reputation < 2:
        return 0
    factor = int(options.accept_reply_factor_for_user)
    impact = factor * int(math.log(reputation))
    return min(impact, int(options.vote_max_for_user))
