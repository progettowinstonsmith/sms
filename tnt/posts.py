# Script to migrate posts
"""
---------------------------------------- TPI table: bb_

CREATE TABLE `bb_posts` (
  `post_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `topic_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `forum_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  `poster_id` mediumint(8) NOT NULL DEFAULT '0',
  `post_time` int(11) NOT NULL DEFAULT '0',
  `poster_ip` varchar(42) NOT NULL DEFAULT '0',
  `poster_rg_id` mediumint(8) NOT NULL DEFAULT '0',
  `attach_rg_sig` tinyint(4) NOT NULL DEFAULT '0',
  `post_username` varchar(25) NOT NULL DEFAULT '',
  `post_edit_time` int(11) NOT NULL DEFAULT '0',
  `post_edit_count` smallint(5) unsigned NOT NULL DEFAULT '0',
  `post_attachment` tinyint(1) NOT NULL DEFAULT '0',
  `user_post` tinyint(1) NOT NULL DEFAULT '1',
  `mc_comment` text NOT NULL,
  `mc_type` tinyint(1) NOT NULL DEFAULT '0',
  `mc_user_id` mediumint(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`post_id`),
  KEY `topic_id` (`topic_id`),
  KEY `poster_id` (`poster_id`),
  KEY `post_time` (`post_time`),
  KEY `forum_id_post_time` (`forum_id`,`post_time`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


---------------------------------------- TNT table: Trck_forums

CREATE TABLE `Trck_posts` (
  `pid` int(10) NOT NULL AUTO_INCREMENT,
  `append_edit` tinyint(1) DEFAULT '0',
  `edit_time` int(10) DEFAULT NULL,
  `author_id` mediumint(8) NOT NULL DEFAULT '0',
  `author_name` varchar(32) DEFAULT NULL,
  `use_sig` tinyint(1) NOT NULL DEFAULT '0',
  `use_emo` tinyint(1) NOT NULL DEFAULT '0',
  `ip_address` varchar(16) NOT NULL DEFAULT '',
  `post_date` int(10) DEFAULT NULL,
  `icon_id` smallint(3) DEFAULT NULL,
  `post` mediumtext,
  `queued` tinyint(1) DEFAULT NULL,
  `topic_id` int(10) NOT NULL DEFAULT '0',
  `forum_id` smallint(5) NOT NULL DEFAULT '0',
  `attach_id` varchar(64) DEFAULT NULL,
  `attach_hits` int(10) DEFAULT NULL,
  `attach_type` varchar(128) DEFAULT NULL,
  `attach_file` varchar(255) DEFAULT NULL,
  `post_title` varchar(255) DEFAULT NULL,
  `new_topic` tinyint(1) DEFAULT '0',
  `edit_name` varchar(255) DEFAULT NULL,
  `bt_info_hash` blob,
  `bt_size` bigint(20) DEFAULT NULL,
  `bt_tracker` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `topic_id` (`topic_id`,`author_id`),
  KEY `author_id` (`author_id`),
  KEY `forum_id` (`forum_id`,`post_date`),
  KEY `InfoHash` (`bt_info_hash`(20)),
  KEY `Category` (`icon_id`),
  KEY `TorrenSize` (`bt_size`),
  KEY `PostDateIndex` (`post_date`),
  KEY `file` (`attach_file`),
  KEY `author` (`author_name`)
) ENGINE=MyISAM AUTO_INCREMENT=15736004 DEFAULT CHARSET=latin1;

---------------------------------------- RULES

  `post_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT, is pid
  `topic_id` mediumint(8) unsigned NOT NULL DEFAULT '0', is topic_id
  `forum_id` smallint(5) unsigned NOT NULL DEFAULT '0', is forum_id
  `poster_id` mediumint(8) NOT NULL DEFAULT '0', is author_id
  `post_time` int(11) NOT NULL DEFAULT '0', is post_date
  `poster_ip` varchar(42) NOT NULL DEFAULT '0', is ip_address
  `poster_rg_id` mediumint(8) NOT NULL DEFAULT '0', 
  `attach_rg_sig` tinyint(4) NOT NULL DEFAULT '0',
  `post_username` varchar(25) NOT NULL DEFAULT '', is author_name
  `post_edit_time` int(11) NOT NULL DEFAULT '0', 
  `post_edit_count` smallint(5) unsigned NOT NULL DEFAULT '0',
  `post_attachment` tinyint(1) NOT NULL DEFAULT '0',
  `user_post` tinyint(1) NOT NULL DEFAULT '1',
  `mc_comment` text NOT NULL,
  `mc_type` tinyint(1) NOT NULL DEFAULT '0',
  `mc_user_id` mediumint(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`post_id`),
  KEY `topic_id` (`topic_id`),
  KEY `poster_id` (`poster_id`),
  KEY `post_time` (`post_time`),
  KEY `forum_id_post_time` (`forum_id`,`post_time`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

"""
import json
from pprint import pprint
import logging
import socket
import ipaddress


from TNT.app import app
from TNT.mapper import Map,IMap,MAPPER
from TNT.transform import Transformer
from TNT.func import now, stringify, ip2int


class POST(Transformer):
    DROP = [
        # "bt_info_hash",
    ]
    RULES = {
        # 'pid': IMap('post'),
        'ip_address': ip2int,
        'author_name': stringify,
    }
    ADDITIONS = {
    }
    FIELDS = [
        {'post_id': '{pid}'},
        {'topic_id': '{topic_id}'},
        {'forum_id': '{forum_id}'},
        {'poster_id': '{author_id}'},
        {'post_time': '{post_date}'},
        {'poster_ip': '{ip_address}'},         # `poster_ip` varchar(42) NOT NULL DEFAULT '0', is ip_address
        # `poster_rg_id` mediumint(8) NOT NULL DEFAULT '0', 
        # `attach_rg_sig` tinyint(4) NOT NULL DEFAULT '0',        
        {'post_username': '{author_name}'},    # `post_username` varchar(25) NOT NULL DEFAULT '', is author_name
        # `post_edit_time` int(11) NOT NULL DEFAULT '0', 
        # `post_edit_count` smallint(5) unsigned NOT NULL DEFAULT '0',
        # `post_attachment` tinyint(1) NOT NULL DEFAULT '0',
        # `user_post` tinyint(1) NOT NULL DEFAULT '1',
        {'user_post': '1'},
        # `mc_comment` text NOT NULL,
        # `mc_type` tinyint(1) NOT NULL DEFAULT '0',
        # `mc_user_id` mediumint(8) NOT NULL DEFAULT '0',

    ]
    SUB = 'post'
    TABLE = 'bb_posts'
    DB_FIELDS =  ['pid',
                  'topic_id',
                  'forum_id',
                  'author_id',
                  'post_date',
                  'ip_address',
                  'author_name',
    ]
    # [ '*' ]
    DB_ORDER = 'pid'
    DB_TABLES = 'Trck_posts'
    # DB_LIMIT = " LIMIT 100000, 100000"
    # DB_LIMIT = "LIMIT 10000"
    # PREMAPS = [ ('pid','post',1),]
    # INPUT_MAPS = [ 'post', 'user',  'forum' ]

def main():
    app('post',POST)



