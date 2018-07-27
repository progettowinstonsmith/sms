# Script to migrate user_groups
"""
---------------------------------------- TPI table: bb_
CREATE TABLE `bb_forums` (
  `forum_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `cat_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  `forum_name` varchar(150) NOT NULL DEFAULT '',
  `forum_desc` text NOT NULL,
  `forum_status` tinyint(4) NOT NULL DEFAULT '0', 0 sbloccato 1 bloccato - LOOK
  `forum_order` smallint(5) unsigned NOT NULL DEFAULT '1', is position
  `forum_posts` mediumint(8) unsigned NOT NULL DEFAULT '0', is posts
  `forum_topics` mediumint(8) unsigned NOT NULL DEFAULT '0', is topics
  `forum_last_post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `forum_tpl_id` smallint(6) NOT NULL DEFAULT '0',
  `prune_days` smallint(5) unsigned NOT NULL DEFAULT '0',
  `auth_view` tinyint(2) NOT NULL DEFAULT '0',
  `auth_read` tinyint(2) NOT NULL DEFAULT '0',
  `auth_post` tinyint(2) NOT NULL DEFAULT '0',
  `auth_reply` tinyint(2) NOT NULL DEFAULT '0',
  `auth_edit` tinyint(2) NOT NULL DEFAULT '0',
  `auth_delete` tinyint(2) NOT NULL DEFAULT '0',
  `auth_sticky` tinyint(2) NOT NULL DEFAULT '0',
  `auth_announce` tinyint(2) NOT NULL DEFAULT '0',
  `auth_vote` tinyint(2) NOT NULL DEFAULT '0',
  `auth_pollcreate` tinyint(2) NOT NULL DEFAULT '0',
  `auth_attachments` tinyint(2) NOT NULL DEFAULT '0',
  `auth_download` tinyint(2) NOT NULL DEFAULT '0',
  `allow_reg_tracker` tinyint(1) NOT NULL DEFAULT '0',
  `allow_porno_topic` tinyint(1) NOT NULL DEFAULT '0',
  `self_moderated` tinyint(1) NOT NULL DEFAULT '0',
  `forum_parent` smallint(5) unsigned NOT NULL DEFAULT '0',
  `show_on_index` tinyint(1) NOT NULL DEFAULT '1',
  `forum_display_sort` tinyint(1) NOT NULL DEFAULT '0',
  `forum_display_order` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`forum_id`),
  KEY `forums_order` (`forum_order`),
  KEY `cat_id` (`cat_id`),
  KEY `forum_last_post_id` (`forum_last_post_id`),
  KEY `forum_parent` (`forum_parent`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

---------------------------------------- TNT table: Trck_forums
CREATE TABLE `Trck_forums` (
  `id` smallint(5) NOT NULL DEFAULT '0',
  `topics` mediumint(6) DEFAULT NULL,
  `posts` mediumint(6) DEFAULT NULL,
  `last_post` int(10) DEFAULT NULL,
  `last_poster_id` mediumint(8) NOT NULL DEFAULT '0',
  `last_poster_name` varchar(32) DEFAULT NULL,
  `name` varchar(128) NOT NULL DEFAULT '',
  `description` text,
  `position` tinyint(2) DEFAULT NULL,
  `use_ibc` tinyint(1) DEFAULT NULL,
  `use_html` tinyint(1) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `start_perms` varchar(255) NOT NULL DEFAULT '',
  `reply_perms` varchar(255) NOT NULL DEFAULT '',
  `read_perms` varchar(255) NOT NULL DEFAULT '',
  `password` varchar(32) DEFAULT NULL,
  `category` tinyint(2) NOT NULL DEFAULT '0',
  `last_title` varchar(128) DEFAULT NULL,
  `last_id` int(10) DEFAULT NULL,
  `sort_key` varchar(32) DEFAULT NULL,
  `sort_order` varchar(32) DEFAULT NULL,
  `prune` tinyint(3) DEFAULT NULL,
  `show_rules` tinyint(1) DEFAULT NULL,
  `upload_perms` varchar(255) DEFAULT NULL,
  `preview_posts` tinyint(1) DEFAULT NULL,
  `allow_poll` tinyint(1) NOT NULL DEFAULT '1',
  `allow_pollbump` tinyint(1) NOT NULL DEFAULT '0',
  `inc_postcount` tinyint(1) NOT NULL DEFAULT '1',
  `skin_id` int(10) DEFAULT NULL,
  `parent_id` mediumint(5) DEFAULT '-1',
  `subwrap` tinyint(1) DEFAULT '0',
  `sub_can_post` tinyint(1) DEFAULT '1',
  `quick_reply` tinyint(1) DEFAULT '0',
  `redirect_url` varchar(250) DEFAULT '',
  `redirect_on` tinyint(1) NOT NULL DEFAULT '0',
  `redirect_hits` int(10) NOT NULL DEFAULT '0',
  `redirect_loc` varchar(250) DEFAULT '',
  `rules_title` varchar(255) NOT NULL DEFAULT '',
  `rules_text` text NOT NULL,
  `has_mod_posts` tinyint(1) NOT NULL DEFAULT '0',
  `topic_mm_id` varchar(250) NOT NULL DEFAULT '',
  `notify_modq_emails` text,
  PRIMARY KEY (`id`),
  KEY `category` (`category`),
  KEY `id` (`id`),
  KEY `parent` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
---------------------------------------- RULES

OK  `forum_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT is renum(id),
OK  `cat_id` smallint(5) unsigned NOT NULL DEFAULT '0' is renum(category),
OK  `forum_name` varchar(150) NOT NULL DEFAULT '', is name,
OK  `forum_desc` text NOT NULL, is description,
OK  `forum_status` tinyint(4) NOT NULL DEFAULT '0', 0 sbloccato 1 bloccato - LOOK
OK  `forum_order` smallint(5) unsigned NOT NULL DEFAULT '1', is position
OK  `forum_posts` mediumint(8) unsigned NOT NULL DEFAULT '0', is posts
OK  `forum_topics` mediumint(8) unsigned NOT NULL DEFAULT '0', is topics
OK  `forum_last_post_id` mediumint(8) unsigned NOT NULL DEFAULT '0', is last_post
??  `forum_tpl_id` smallint(6) NOT NULL DEFAULT '0',
??  `prune_days` smallint(5) unsigned NOT NULL DEFAULT '0',
??  `auth_view` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_read` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_post` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_reply` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_edit` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_delete` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_sticky` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_announce` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_vote` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_pollcreate` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_attachments` tinyint(2) NOT NULL DEFAULT '0',
??  `auth_download` tinyint(2) NOT NULL DEFAULT '0',
??  `allow_reg_tracker` tinyint(1) NOT NULL DEFAULT '0',
??  `allow_porno_topic` tinyint(1) NOT NULL DEFAULT '0',
??  `self_moderated` tinyint(1) NOT NULL DEFAULT '0',
OK  `forum_parent` smallint(5) unsigned NOT NULL DEFAULT '0', is parent_id
OK  `show_on_index` tinyint(1) NOT NULL DEFAULT '1',
??  `forum_display_sort` tinyint(1) NOT NULL DEFAULT '0',
??  `forum_display_order` tinyint(1) NOT NULL DEFAULT '0',


"""
import argparse
import json
from pprint import pprint
import logging

from TNT.app import app
from TNT.mapper import Map,IMap
from TNT.transform import Transformer
from TNT.func import now, stringify

ORDER = {}
LAST_1_LEVEL = [1000,0]
MAX = {}


def forum_order(trn,record):
    global LAST_1_LEVEL
    global ORDER
    id = record['id']
    cat = 0 if record['category'] == 7 else 1
    parent = record['parent_id']
    if (parent is None or parent == -1):
        if parent not in ORDER:
            ORDER[id]=[]
            ORDER[id].append(LAST_1_LEVEL[cat])
            LAST_1_LEVEL[cat] += 100 
        return ORDER[id][0]
    if parent not in ORDER:
        ORDER[parent]=[]
        ORDER[parent].append(LAST_1_LEVEL[cat])
        LAST_1_LEVEL[cat] += 100 
    N = max(ORDER[parent])
    N += 10
    ORDER[parent].append(N)
    return N

class FORUM(Transformer):
    RULES = {
        #'id': 'forum',
        #'parent_id': forum'),
        #'category': IMap('category'),
        'name': stringify,
        'description': stringify,
    }
    ADDITIONS = {
        'forum_order' : forum_order 
    }
    FIELDS = [
        {'forum_id': '{id}'},
        {'cat_id': '{category}'},
        {'forum_name': '{name}'},
        {'forum_desc': '{description}'},
        {'forum_status': '0'},
        {'forum_order': '{forum_order}'},
        {'forum_posts': '{posts}'},
        {'forum_topics': '{topics}'},
        {'forum_last_post_id': '{last_post}'},
        ##
        # ??  `forum_tpl_id` smallint(6) NOT NULL DEFAULT '0',
        # ??  `prune_days` smallint(5) unsigned NOT NULL DEFAULT '0',
        # ??  `auth_view` tinyint(2) NOT NULL DEFAULT '0',
        {'auth_view': '1'}, # ??  `auth_read` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_post` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_reply` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_edit` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_delete` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_sticky` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_announce` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_vote` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_pollcreate` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_attachments` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `auth_download` tinyint(2) NOT NULL DEFAULT '0',
        # ??  `allow_reg_tracker` tinyint(1) NOT NULL DEFAULT '0',
        # ??  `allow_porno_topic` tinyint(1) NOT NULL DEFAULT '0',
        # ??  `self_moderated` tinyint(1) NOT NULL DEFAULT '0',
        {'forum_parent': '{parent_id}'}, # OK  `forum_parent` smallint(5) unsigned NOT NULL DEFAULT '0', is parent_id
        {'show_on_index': '1'},          # OK  `show_on_index` tinyint(1) NOT NULL DEFAULT '1',
        # ??  `forum_display_sort` tinyint(1) NOT NULL DEFAULT '0',
        # ??  `forum_display_order` tinyint(1) NOT NULL DEFAULT '0',
        # {'': '{}'},
    ]
    SUB = 'forum'
    TABLE = 'bb_forums'
    DB_FIELDS = [ '*' ]
    DB_ORDER = 'parent_id'
    DB_TABLES = 'Trck_forums'
    # DB_LIMIT = "LIMIT 100"
    # PREMAPS = [ ('id','forum',10),]


def main():
    app('forum',FORUM)
