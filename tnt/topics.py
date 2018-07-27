# Script to migrate topics
"""
---------------------------------------- TPI table: bb_

CREATE TABLE `bb_topics` (
  `topic_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `forum_id` smallint(8) unsigned NOT NULL DEFAULT '0',
  `topic_title` varchar(250) NOT NULL DEFAULT '',
  `topic_poster` mediumint(8) NOT NULL DEFAULT '0',
  `topic_time` int(11) NOT NULL DEFAULT '0',
  `topic_views` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `topic_replies` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `topic_status` tinyint(3) NOT NULL DEFAULT '0',
  `topic_vote` tinyint(1) NOT NULL DEFAULT '0',
  `topic_type` tinyint(3) NOT NULL DEFAULT '0',
  `topic_first_post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `topic_last_post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `topic_moved_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `topic_attachment` tinyint(1) NOT NULL DEFAULT '0',
  `topic_dl_type` tinyint(1) NOT NULL DEFAULT '0',
  `topic_last_post_time` int(11) NOT NULL DEFAULT '0',
  `topic_show_first_post` tinyint(1) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`topic_id`),
  KEY `forum_id` (`forum_id`),
  KEY `topic_last_post_id` (`topic_last_post_id`),
  KEY `topic_last_post_time` (`topic_last_post_time`),
  FULLTEXT KEY `topic_title` (`topic_title`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

---------------------------------------- TNT table: Trck_forums

CREATE TABLE `Trck_topics` (
R  `tid` int(10) NOT NULL AUTO_INCREMENT,
*  `title` varchar(250) NOT NULL DEFAULT '',
>  `description` varchar(250) DEFAULT NULL,
R  `state` varchar(8) DEFAULT NULL,
*  `posts` int(10) DEFAULT NULL,
R  `starter_id` mediumint(8) NOT NULL DEFAULT '0',
*  `start_date` int(10) DEFAULT NULL,
  `last_poster_id` mediumint(8) NOT NULL DEFAULT '0',
R  `last_post` int(10) DEFAULT NULL,
  `icon_id` tinyint(2) DEFAULT NULL,
X `starter_name` varchar(32) DEFAULT NULL,
X  `last_poster_name` varchar(32) DEFAULT NULL,
  `poll_state` varchar(8) DEFAULT NULL,
  `last_vote` int(10) DEFAULT NULL,
* `views` int(10) DEFAULT NULL,
R  `forum_id` smallint(5) NOT NULL DEFAULT '0',
  `approved` tinyint(1) DEFAULT NULL,
X  `author_mode` tinyint(1) DEFAULT NULL,
X  `pinned` tinyint(1) DEFAULT NULL,
  `moved_to` varchar(64) DEFAULT NULL,
X  `rating` text,
X  `total_votes` int(5) NOT NULL DEFAULT '0',
  `bt_info_hash` blob,
  PRIMARY KEY (`tid`),
  KEY `last_post` (`last_post`),
  KEY `forum_id` (`forum_id`,`approved`,`pinned`),
  KEY `f_info_hash` (`bt_info_hash`(20)),
  KEY `TopicCategory` (`icon_id`),
  KEY `TopicLastPost` (`last_poster_id`),
  KEY `descritpion` (`description`),
  KEY `approved` (`approved`),
  KEY `pinned` (`pinned`),
  FULLTEXT KEY `title` (`title`)
) ENGINE=MyISAM AUTO_INCREMENT=589473 DEFAULT CHARSET=latin1;

---------------------------------------- RULES

OK  `topic_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT, is renum(tid)
OK  `forum_id` smallint(8) unsigned NOT NULL DEFAULT '0', is renum(forum_id)
OK  `topic_title` varchar(250) NOT NULL DEFAULT '', is title
OK  `topic_poster` mediumint(8) NOT NULL DEFAULT '0',  is starter_id
OK  `topic_time` int(11) NOT NULL DEFAULT '0', is start_date
OK  `topic_views` mediumint(8) unsigned NOT NULL DEFAULT '0',  is views
OK  `topic_replies` mediumint(8) unsigned NOT NULL DEFAULT '0', is posts
??  `topic_status` tinyint(3) NOT NULL DEFAULT '0', is X(state)
??  `topic_vote` tinyint(1) NOT NULL DEFAULT '0', X
??  `topic_type` tinyint(3) NOT NULL DEFAULT '0', ?
??  `topic_first_post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
??  `topic_last_post_id` mediumint(8) unsigned NOT NULL DEFAULT '0', 
??  `topic_moved_id` mediumint(8) unsigned NOT NULL DEFAULT '0', from moved_to
??  `topic_attachment` tinyint(1) NOT NULL DEFAULT '0', ?
??  `topic_dl_type` tinyint(1) NOT NULL DEFAULT '0', ?
OK  `topic_last_post_time` int(11) NOT NULL DEFAULT '0', last_post
??  `topic_show_first_post` tinyint(1) unsigned NOT NULL DEFAULT '0', ?

ADD INTO FILES

?? bb_attachments_desc
    topic_id, comment

"""
import json
from pprint import pprint
import logging

from TNT.app import app
from TNT.mapper import Map,IMap,MAPPER
from TNT.transform import Transformer
from TNT.func import now, stringify, not_null

def topic_state(tnt, x):
    return stringify(tnt,x)

class TOPIC(Transformer):
    DROP = [
        # o"bt_info_hash",
    ]
    RULES = {
        'title': stringify,
        'description': stringify,
        'state': topic_state,
        'moved_to': not_null,
    }
    ADDITIONS = {
    }
    FIELDS = [
        {'topic_id': '{tid}'},
        {'forum_id': '{forum_id}'},
        {'topic_title': '{title}'},
        {'topic_poster': '{starter_id}' },
        {'topic_time': '{start_date}' },
        {'topic_views': '{views}'},
        {'topic_replies': '{posts}'},
        {'topic_status': '{state}'},
        # {'': '{}'},
        # {'': '{}'},
        {'topic_moved_id': '{moved_to}'},
        #
        {'topic_last_post_time': '{last_post}'},
        # {'': '{}'},
    ]
    SUB = 'topic'
    TABLE = 'bb_topics'
    DB_FIELDS =  ['approved',
                  'author_mode',
                  # 'bt_info_hash',
                  'description',
                  'forum_id',
                  'icon_id',
                  'last_post',
                  'last_poster_id',
                  'last_poster_name',
                  'last_vote',
                  'moved_to',
                  'pinned',
                  'poll_state',
                  'posts',
                  'rating',
                  'start_date',
                  'starter_id',
                  'starter_name',
                  'state',
                  'tid',
                  'title',
                  'total_votes',
                  'views',]
    DB_ORDER = 'tid'
    DB_TABLES = 'Trck_topics'



def main():
    app('topic',TOPIC)



