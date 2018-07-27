# Script to migrate user_groups
"""
---------------------------------------- TNT table: Trck_forums

CREATE TABLE `Trck_categories` (
  `id` smallint(5) NOT NULL DEFAULT '0',
  `position` tinyint(3) DEFAULT NULL,
  `state` varchar(10) DEFAULT NULL,
  `name` varchar(128) NOT NULL DEFAULT '',
  `description` text,
  `image` varchar(128) DEFAULT NULL,
  `url` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

---------------------------------------- TPI table: bb_categories

CREATE TABLE `bb_categories` (
  `cat_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `cat_title` varchar(100) NOT NULL DEFAULT '',
  `cat_order` smallint(5) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`cat_id`),
  KEY `cat_order` (`cat_order`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

---------------------------------------- RULES


  `cat_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT, is renum(id)
  `cat_title` varchar(100) NOT NULL DEFAULT '', is name 
  `cat_order` smallint(5) unsigned NOT NULL DEFAULT '0', is position
   description text is description



"""
import argparse
import json
from pprint import pprint

from TNT.app import app
from TNT.mapper import Map,IMap
from TNT.transform import Transformer, now, stringify
from TNT.func import stringify

class CATEGORY(Transformer):
    ALTER = [
        "ALTER TABLE bb_categories ADD COLUMN cat_description varchar(128) NOT NULL DEFAULT '';",
    ]
    RULES = {
        'name': stringify,
        'description': stringify,
    }
    ADDITIONS = {
    }
    FIELDS = [
        {'cat_id': '{id}'},
        {'cat_title': '{name}'},
        {'cat_order': '{position}'},
        {'cat_description': '{description}'},
        # {'': '{}'},
    ]
    SUB = 'categories'
    TABLE = 'bb_categories'
    DB_FIELDS = [ '*' ]
    DB_ORDER = 'id'
    DB_TABLES = 'Trck_categories'
    # DB_LIMIT = "LIMIT 100"
    # PREMAPS = [ ('id','category', 10),]

def main():

    app('category', CATEGORY)
