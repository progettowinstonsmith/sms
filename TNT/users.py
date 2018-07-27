# Script to migrate user_groups
"""
---------------------------------------- TNT table: Trck_members

CREATE TABLE `Trck_members` (
  `aim_name` varchar(40) DEFAULT NULL,
  `allow_admin_mails` tinyint(1) DEFAULT NULL,
  `auto_track` tinyint(1) DEFAULT '0',
  `avatar_size` varchar(9) DEFAULT NULL,
  `avatar` varchar(128) DEFAULT NULL,
  `bday_day` int(2) DEFAULT NULL,
  `bday_month` int(2) DEFAULT NULL,
  `bday_year` int(4) DEFAULT NULL,
  `coppa_user` tinyint(1) DEFAULT '0',
  `dst_in_use` tinyint(1) DEFAULT '0',
  `email_full` tinyint(1) DEFAULT NULL,
  `email_pm` tinyint(1) DEFAULT NULL,
  `email` varchar(60) NOT NULL DEFAULT '',
  `hide_email` varchar(8) DEFAULT NULL,
  `icq_number` varchar(40) DEFAULT NULL,
  `id` mediumint(8) NOT NULL DEFAULT '0',
  `integ_msg` varchar(250) DEFAULT '',
  `interests` text,
  `ip_address` varchar(16) NOT NULL DEFAULT '',
  `joined` int(10) NOT NULL DEFAULT '0',
  `language` varchar(32) DEFAULT NULL,
  `last_activity` int(10) DEFAULT '0',
  `last_post` int(10) DEFAULT NULL,
  `last_visit` int(10) DEFAULT '0',
  `location` varchar(128) DEFAULT NULL,
  `mgroup` smallint(3) NOT NULL DEFAULT '0',
  `misc` varchar(128) DEFAULT NULL,
  `mod_posts` varchar(100) NOT NULL DEFAULT '0',
  `msg_from_id` mediumint(8) DEFAULT NULL,
  `msg_msg_id` int(10) DEFAULT NULL,
  `msg_total` smallint(5) DEFAULT NULL,
  `msnname` varchar(64) DEFAULT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  `namecrc32` bigint(20) unsigned DEFAULT '0',
  `new_msg` tinyint(2) DEFAULT NULL,
  `org_perm_id` varchar(255) DEFAULT '',
  `org_supmod` tinyint(1) DEFAULT '0',
  `password` varchar(32) NOT NULL DEFAULT '',
  `perms_bitmask` bigint(20) DEFAULT NULL,
  `posts` mediumint(7) DEFAULT '0',
  `pub_rel_invisible` tinyint(1) DEFAULT NULL,
  `restrict_post` varchar(100) NOT NULL DEFAULT '0',
  `show_popup` tinyint(1) DEFAULT NULL,
  `signature` text,
  `skin` smallint(5) DEFAULT NULL,
  `sub_end` int(10) NOT NULL DEFAULT '0',
  `temp_ban` varchar(100) DEFAULT NULL,
  `time_offset` varchar(10) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `vdirs` text,
  `view_avs` tinyint(1) DEFAULT '1',
  `view_img` tinyint(1) DEFAULT '1',
  `view_pop` tinyint(1) DEFAULT '1',
  `view_prefs` varchar(64) DEFAULT '-1&-1',
  `view_sigs` tinyint(1) DEFAULT '1',
  `warn_lastwarn` int(10) NOT NULL DEFAULT '0',
  `warn_level` int(10) DEFAULT NULL,
  `website` varchar(70) DEFAULT NULL,
  `yahoo` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`),
  KEY `mgroup` (`mgroup`),
  KEY `bday_day` (`bday_day`),
  KEY `bday_month` (`bday_month`),
  KEY `MemberLastVisitIndex` (`last_visit`),
  KEY `MemberLastActivIndex` (`last_activity`),
  KEY `iNameCRC32` (`namecrc32`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

---------------------------------------- TPI table: bb_users

CREATE TABLE `bb_users` (
  `user_id` mediumint(8) NOT NULL AUTO_INCREMENT,
  `user_active` tinyint(1) NOT NULL DEFAULT '1',
  `username` varchar(25) NOT NULL DEFAULT '',
  `user_password` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `user_session_time` int(11) NOT NULL DEFAULT '0',
  `user_lastvisit` int(11) NOT NULL DEFAULT '0',
  `user_last_ip` varchar(42) NOT NULL DEFAULT '0',
  `user_regdate` int(11) NOT NULL DEFAULT '0',
  `user_reg_ip` varchar(42) NOT NULL DEFAULT '0',
  `user_level` tinyint(4) NOT NULL DEFAULT '0',
  `user_posts` mediumint(8) unsigned NOT NULL DEFAULT '0',
  `user_timezone` decimal(5,2) NOT NULL DEFAULT '0.00',
  `user_lang` varchar(255) NOT NULL DEFAULT 'ru',
  `user_new_privmsg` smallint(5) unsigned NOT NULL DEFAULT '0',
  `user_unread_privmsg` smallint(5) unsigned NOT NULL DEFAULT '0',
  `user_last_privmsg` int(11) NOT NULL DEFAULT '0',
  `user_opt` int(11) NOT NULL DEFAULT '0',
  `user_rank` int(11) NOT NULL DEFAULT '0',
  `avatar_ext_id` tinyint(4) NOT NULL DEFAULT '0',
  `user_gender` tinyint(1) NOT NULL DEFAULT '0',
  `user_birthday` date NOT NULL DEFAULT '0000-00-00',
  `user_email` varchar(255) NOT NULL DEFAULT '',
  `user_skype` varchar(32) NOT NULL DEFAULT '',
  `user_twitter` varchar(15) NOT NULL DEFAULT '',
  `user_icq` varchar(15) NOT NULL DEFAULT '',
  `user_website` varchar(100) NOT NULL DEFAULT '',
  `user_from` varchar(100) NOT NULL DEFAULT '',
  `user_sig` text NOT NULL,
  `user_occ` varchar(100) NOT NULL DEFAULT '',
  `user_interests` varchar(255) NOT NULL DEFAULT '',
  `user_actkey` varchar(32) NOT NULL DEFAULT '',
  `user_newpasswd` varchar(32) NOT NULL DEFAULT '',
  `autologin_id` varchar(12) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `user_newest_pm_id` mediumint(8) NOT NULL DEFAULT '0',
  `user_points` float(16,2) NOT NULL DEFAULT '0.00',
  `tpl_name` varchar(255) NOT NULL DEFAULT 'default',
  PRIMARY KEY (`user_id`),
  KEY `username` (`username`(10)),
  KEY `user_email` (`user_email`(10)),
  KEY `user_level` (`user_level`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

---------------------------------------- RULES

  `user_id` mediumint(8) NOT NULL AUTO_INCREMENT, is renum(id)
  `user_active` tinyint(1) NOT NULL DEFAULT '1', 
  `username` varchar(25) NOT NULL DEFAULT '', is  name 
  `user_password` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '', is new_passwd
  `user_session_time` int(11) NOT NULL DEFAULT '0',
  `user_lastvisit` int(11) NOT NULL DEFAULT '0', is last_visit
  `user_last_ip` varchar(42) NOT NULL DEFAULT '0', is ip_address
  `user_regdate` int(11) NOT NULL DEFAULT '0',  is joined
  `user_reg_ip` varchar(42) NOT NULL DEFAULT '0', 
  `user_level` tinyint(4) NOT NULL DEFAULT '0',
  `user_posts` mediumint(8) unsigned NOT NULL DEFAULT '0', is posts
  `user_timezone` decimal(5,2) NOT NULL DEFAULT '0.00', 
  `user_lang` varchar(255) NOT NULL DEFAULT 'ru', is language
  `user_new_privmsg` smallint(5) unsigned NOT NULL DEFAULT '0', 
  `user_unread_privmsg` smallint(5) unsigned NOT NULL DEFAULT '0',
  `user_last_privmsg` int(11) NOT NULL DEFAULT '0',
  `user_opt` int(11) NOT NULL DEFAULT '0', 
  `user_rank` int(11) NOT NULL DEFAULT '0',
  `avatar_ext_id` tinyint(4) NOT NULL DEFAULT '0',
  `user_gender` tinyint(1) NOT NULL DEFAULT '0',
  `user_birthday` date NOT NULL DEFAULT '0000-00-00', is bday_*
  `user_email` varchar(255) NOT NULL DEFAULT '', us email
  `user_skype` varchar(32) NOT NULL DEFAULT '', 
  `user_twitter` varchar(15) NOT NULL DEFAULT '',
  `user_icq` varchar(15) NOT NULL DEFAULT '', is icq_number
  `user_website` varchar(100) NOT NULL DEFAULT '', is website
  `user_from` varchar(100) NOT NULL DEFAULT '', 
  `user_sig` text NOT NULL, is signature  
  `user_occ` varchar(100) NOT NULL DEFAULT '', 
  `user_interests` varchar(255) NOT NULL DEFAULT '',
  `user_actkey` varchar(32) NOT NULL DEFAULT '',
  `user_newpasswd` varchar(32) NOT NULL DEFAULT '', 
  `autologin_id` varchar(12) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '',
  `user_newest_pm_id` mediumint(8) NOT NULL DEFAULT '0',
  `user_points` float(16,2) NOT NULL DEFAULT '0.00',
  `tpl_name` varchar(255) NOT NULL DEFAULT 'default',



"""
import json

from TNT.app import app
from TNT.transform import Transformer
from TNT.func import stringify, test_email, new_pwd, birthday

class USER(Transformer):
    RULES = {
        # 'id': 'user',
        'name': stringify,
        'email': test_email,
        'language': stringify,
        'icq_number': stringify,
        'website': stringify,
    }
    ADDITIONS = {
        'pwd' : new_pwd,
        'birthday' : birthday,
    }
    FIELDS = [
        {'user_id': '{id}'},
        {'username': '{name}'},
        {'user_password': '{pwd}'},
        {'user_lastvisit': '{last_visit}'},
        {'user_posts': '{posts}'},
        {'user_lang': '{language}'},
        {'user_birthday': '{birthday}'},
        {'user_email': '{email}'},
        {'user_icq': '{icq_number}'},
        {'user_website': '{website}'},
    ]
    SUB = 'users'
    TABLE = 'bb_users'
    DB_FIELDS = [ '*' ]
    DB_ORDER = 'id'
    DB_TABLES = 'Trck_members'
    # Only Good users
    ID_LABEL = 'id'
    GOOD_ID = json.load(open("/Users/exedre/.tnt/good.map",'r'))

def main():
    app('user',USER)
