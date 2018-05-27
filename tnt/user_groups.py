# Script to migrate user_groups
"""
---------------------------------------- TNT table: Trck_groups

CREATE TABLE `Trck_groups` (
  `g_id` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `g_view_board` tinyint(1) DEFAULT NULL,
  `g_mem_info` tinyint(1) DEFAULT NULL,
  `g_other_topics` tinyint(1) DEFAULT NULL,
  `g_use_search` tinyint(1) DEFAULT NULL,
  `g_email_friend` tinyint(1) DEFAULT NULL,
  `g_invite_friend` tinyint(1) DEFAULT NULL,
  `g_edit_profile` tinyint(1) DEFAULT NULL,
  `g_post_new_topics` tinyint(1) DEFAULT NULL,
  `g_reply_own_topics` tinyint(1) DEFAULT NULL,
  `g_reply_other_topics` tinyint(1) DEFAULT NULL,
  `g_edit_posts` tinyint(1) DEFAULT NULL,
  `g_delete_own_posts` tinyint(1) DEFAULT NULL,
  `g_open_close_posts` tinyint(1) DEFAULT NULL,
  `g_delete_own_topics` tinyint(1) DEFAULT NULL,
  `g_post_polls` tinyint(1) DEFAULT NULL,
  `g_vote_polls` tinyint(1) DEFAULT NULL,
  `g_use_pm` tinyint(1) DEFAULT NULL,
  `g_is_supmod` tinyint(1) DEFAULT NULL,
  `g_access_cp` tinyint(1) DEFAULT NULL,
  `g_title` varchar(32) NOT NULL DEFAULT '',
  `g_can_remove` tinyint(1) DEFAULT NULL,
  `g_append_edit` tinyint(1) DEFAULT NULL,
  `g_access_offline` tinyint(1) DEFAULT NULL,
  `g_avoid_q` tinyint(1) DEFAULT NULL,
  `g_avoid_flood` tinyint(1) DEFAULT NULL,
  `g_icon` varchar(64) DEFAULT NULL,
  `g_attach_max` bigint(20) DEFAULT NULL,
  `g_avatar_upload` tinyint(1) DEFAULT '0',
  `g_calendar_post` tinyint(1) DEFAULT '0',
  `prefix` varchar(250) DEFAULT NULL,
  `suffix` varchar(250) DEFAULT NULL,
  `g_max_messages` int(5) DEFAULT '50',
  `g_max_mass_pm` int(5) DEFAULT '0',
  `g_search_flood` mediumint(6) DEFAULT '20',
  `g_edit_cutoff` int(10) DEFAULT '0',
  `g_promotion` varchar(10) DEFAULT '-1&-1',
  `g_hide_from_list` tinyint(1) DEFAULT '0',
  `g_post_closed` tinyint(1) DEFAULT '0',
  `g_perm_id` varchar(255) NOT NULL DEFAULT '',
  `g_photo_max_vars` varchar(200) DEFAULT '',
  `g_dohtml` tinyint(1) NOT NULL DEFAULT '0',
  `g_edit_topic` tinyint(1) NOT NULL DEFAULT '0',
  `g_email_limit` varchar(15) NOT NULL DEFAULT '10:15',
  PRIMARY KEY (`g_id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;

---------------------------------------- TPI table: bb_groups

CREATE TABLE `bb_groups` (
  `group_id` mediumint(8) NOT NULL AUTO_INCREMENT,
  `avatar_ext_id` int(15) NOT NULL DEFAULT '0',
  `group_time` int(11) NOT NULL DEFAULT '0',
  `mod_time` int(11) NOT NULL DEFAULT '0',
  `group_type` tinyint(4) NOT NULL DEFAULT '1',    (0, aperto; 1, chiuso; 2, nascosto)
  `release_group` tinyint(4) NOT NULL DEFAULT '0', (0 no, 1 si)
  `group_name` varchar(40) NOT NULL DEFAULT '', 
  `group_description` text NOT NULL,
  `group_signature` text NOT NULL,
  `group_moderator` mediumint(8) NOT NULL DEFAULT '0',
  `group_single_user` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`group_id`),
  KEY `group_single_user` (`group_single_user`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


---------------------------------------- RULES

  `group_id` mediumint(8) NOT NULL AUTO_INCREMENT is renum<--`g_id` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `avatar_ext_id` int(15) NOT NULL DEFAULT '0' is '0',
  `group_time` int(11) NOT NULL DEFAULT '0' is now,
  `mod_time` int(11) NOT NULL DEFAULT '0' is now,
  `group_type` tinyint(4) NOT NULL DEFAULT '1' is 2, (to open manually)
  `release_group` tinyint(4) NOT NULL DEFAULT '0' is 1 (to disable manually)
  `group_name` varchar(40) NOT NULL DEFAULT '' is `g_title` varchar(32) NOT NULL DEFAULT '',
  `group_description` text NOT NULL is '',
  `group_signature` text NOT NULL is '', 
  `group_moderator` mediumint(8) NOT NULL DEFAULT '0',
  `group_single_user` tinyint(1) NOT NULL DEFAULT '1',


"""
from datetime import date
import time

from TNT import TNTdb

def now_to_epoch():
    return int(time.mktime(time.gmtime()))

def to_epoch(indate, format='%Y-%m-%d'):
    return int(time.mktime(time.strptime(indate, pattern)))

def from_epoch(epoch):
    pass

class Renumberer:
    LAST_ID = 1
    MAP = {}

    def __call__(self,num):
        if num not in self.MAP:
            self.MAP[num]=self.LAST_ID
            self.LAST_ID += 1
        return self.MAP[num]

def test_renumberer():
    import random
    from pprint import pprint 
    arange = list(range(0,100))
    random.shuffle(arange)
    renums = map(Renumberer(), arange)
    pprint(list(zip(arange, renums)))



class Transformer:
    RULES = {}
    ADDITIONS = {}

    def __init__(self,table):
        self.table = table
        self.data = []
        
    def record(self, info):
        record = info
        for rkey, rfunc in self.RULES.items():
            value = info[rkey]
            if rkey in info:
                value = rfunc(value)
            record[rkey] = value 
        for rkey, rfunc in self.ADDITIONS.items():
            record[rkey] = rfunc(record)
        return record

    def insert(self):
        return "INSERT INTO {table}({fields}) VALUES".format(table=self.table,values=self.FIELDS)
        
    def values(self, info):
        info = self.record(info)
        values = "({values})".format(values=self.VALUES)
        values = values.vformat(info)
        return values

    def transform(self):  
        insert = self.insert()
        values = []
        for info in self.data:
            values.append(self.values(info))
        return insert + "\n\t".join(values)
        
    def load(self, jsonfile):
        self.data = json.load(jsonfile)
        
def stringify(x):
    return "'"+x+"'"

def now(x):
    return now_to_epoch()
    
class USER_GROUP(Transformer):
    RULES = {
        'group_id': Renumberer(),
        'group_title': stringify,

    }
    ADDITIONS = {
        'group_time': now,
        'mod_time': now,
        'group_type': lambda x: 2,
        'release_group': lambda x: 1,
        'group_description': lambda x: '',
        'group_signature': lambda x: '',        
    }
    FIELDS = 'group_id,group_time,mod_time,group_type,release_group,group_name,group_description,group_signature'
    VALUES = '{g_id},{group_time},{mod_time},{group_type},{release_group},{g_title},{group_description},{group_signature}'


def main():
    print("User_groups migration")
