# Script to migrate posts
"""
---------------------------------------- TPI table: bb_

CREATE TABLE `bb_attachments_desc` (
  `attach_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `physical_filename` varchar(255) NOT NULL DEFAULT '',
  `real_filename` varchar(255) NOT NULL DEFAULT '',
  `download_count` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `comment` varchar(255) NOT NULL DEFAULT '',
  `extension` varchar(100) NOT NULL DEFAULT '',
  `mimetype` varchar(100) NOT NULL DEFAULT '',
  `filesize` int(20) NOT NULL DEFAULT '0',
  `filetime` int(11) NOT NULL DEFAULT '0',
  `thumbnail` tinyint(1) NOT NULL DEFAULT '0',
  `tracker_status` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`attach_id`),
  KEY `filetime` (`filetime`),
  KEY `filesize` (`filesize`),
  KEY `physical_filename` (`physical_filename`(10))
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

CREATE TABLE `bb_attachments` (
  `attach_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `post_id` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `user_id_1` mediumint(8) NOT NULL DEFAULT '0',
  PRIMARY KEY (`attach_id`,`post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

---------------------------------------- TNT table: Trck_posts

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
) ENGINE=MyISAM AUTO_INCREMENT=15735960 DEFAULT CHARSET=latin1;

---------------------------------------- RULES

CREATE TABLE `bb_attachments` (
  `attach_id` mediumint(8) unsigned NOT NULL DEFAULT '0', new_id
  `post_id` mediumint(8) unsigned NOT NULL DEFAULT '0', pid
  `user_id_1` mediumint(8) NOT NULL DEFAULT '0',  author_id
  PRIMARY KEY (`attach_id`,`post_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


CREATE TABLE `bb_attachments_desc` (
  `attach_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT, new_id
  `physical_filename` varchar(255) NOT NULL DEFAULT '', attach_file (senza .torrent)
  `real_filename` varchar(255) NOT NULL DEFAULT '',  attach_file con .torrent
  `download_count` mediumint(8) unsigned NOT NULL DEFAULT '0', attach_hits o xbt_files.completed
  `comment` varchar(255) NOT NULL DEFAULT '', Trck_topics.description
  `extension` varchar(100) NOT NULL DEFAULT '', "torrent"
  `mimetype` varchar(100) NOT NULL DEFAULT '', "application/x-bittorrent"
  `filesize` int(20) NOT NULL DEFAULT '0', bt_size? (no è la size del file torrent non del file da scaricare)
  `filetime` int(11) NOT NULL DEFAULT '0', mtime (o ctime o last_seed)
  `thumbnail` tinyint(1) NOT NULL DEFAULT '0', 0 
  `tracker_status` tinyint(1) NOT NULL DEFAULT '0', Boh
  PRIMARY KEY (`attach_id`),
  KEY `filetime` (`filetime`),
  KEY `filesize` (`filesize`),
  KEY `physical_filename` (`physical_filename`(10))
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

"""
import json
from pprint import pprint
import logging
import socket
import ipaddress


from TNT.app import app, _i
from TNT.mapper import Map,IMap,MAPPER
from TNT.transform import Transformer
from TNT.func import stringify,new_id


def real_filename(trn, record):
    return stringify(trn,record['attach_file'])

def physical_filename(trn, record):
    return stringify(trn,record['attach_file'][0:-8])

def new_id(trn, record):
    aid = trn.args.id
    value = record['post_id']
    if not hasattr(trn,'new_id'):
        trn.new_id = []
    if value in trn.new_id:
        return trn.new_id.index(value) + aid
    else:
        trn.new_id.append(value)
        return trn.new_id.index(value) + aid

class ATTACHMENT(Transformer):
    DROP = [
        # "bt_info_hash",
    ]
    RULES = {        
        'attach_type': stringify,
        'description': stringify,
        # 'pid': IMap('post'),
        # 'ip_address': ip2int,
        # 'author_name': stringify,
    }
    ADDITIONS = {
        'real_filename': real_filename,
        'physical_filename': physical_filename,
    }
    FIELDS = [
        {'attach_id': '{fid}'},
        {'physical_filename': '{physical_filename}'},
        {'real_filename': '{real_filename}'},
        {'download_count': '{completed}'},
        {'comment': '{description}'},
        {'extension': '"torrent"'},
        {'mimetype': '{attach_type}'},
        {'filesize': '{bt_size}'}, #?!?
        {'filetime': '{mtime}'},
        {'thumbnail': '0'},
        {'tracker_status': '0'},
    ]
    SUB = 'attachment'
    TABLE = 'bb_attachments_desc'
    DB_FIELDS =  ['P.pid AS post_id',
                  'X.fid',
                  'P.attach_file',
                  'X.completed',
                  'T.description',
                  'P.attach_type',
                  'P.bt_size',
                  'P.author_id',
                  'X.mtime', ]
    # [ '*' ]
    DB_ORDER = 'X.fid'
    DB_TABLES = 'Trck_posts P INNER JOIN xbt_files X ON P.pid = X.pid INNER JOIN Trck_topics T ON P.topic_id = T.tid'
    # DB_LIMIT = " LIMIT 100000, 100000"
    #DB_LIMIT = "LIMIT 10000"
    DB_WHERE = "LENGTH(P.attach_file)!=0"
    # PREMAPS = [ ('pid','post',1),]
    # INPUT_MAPS = [ 'post', 'user',  'forum' ]

    def with_db_results(self):
        sql = "INSERT INTO bb_attachments(attach_id, post_id, user_id_1) VALUES "
        records = []
        for result in self.db_results[self.SUB]:
            records.append( "({fid},{post_id},{author_id})".format(**result) )
        return sql + ',\n\t'.join(records) + ";"

def main():
    app('attachment',
        ATTACHMENT )




