# Script to migrate topics
"""

"""
import json
from pprint import pprint
import logging

from TNT.app import app
from TNT.mapper import Map,IMap,MAPPER
from TNT.transform import Transformer
from TNT.func import now, stringify

def topic_state(tnt, x):
    return stringify(tnt,x)

class TOPIC_POSTS(Transformer):
    RULES = {
    }
    ADDITIONS = {
    }
    FIELDS = [
        {'topic_id': '{topic_id}'},
        {'topic_last_post_id': '{topic_last_post_id}'},
        # {'': '{}'},
    ]
    SUB = 'topic'
    TABLE = 'bb_topics'
    DB_SQL = "SELECT P.topic_id, P.pid as topic_last_post_id FROM Trck_topics T, Trck_posts P WHERE P.topic_id = T.tid AND T.last_post = P.post_date AND T.last_poster_id = P.author_id "
    OUT_UPDATE = ( ( ('topic_last_post_id',), 'topic_id' ), )
    WHERE_KIND = 'AND'
    # ORDER BY topic_id, topic_last_post_id

def main():
    app('topic_last_post',TOPIC_POSTS)



