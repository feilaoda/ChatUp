
DROP TABLE IF EXISTS `channel`;
CREATE TABLE IF NOT EXISTS `channel` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(200) default NULL,
  `isa` varchar(50) default NULL,
  `pic` varchar(255) default NULL,
  `sorting` int(11) default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_channel_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `channel_entry`
--

DROP TABLE IF EXISTS `channel_entry`;
CREATE TABLE IF NOT EXISTS `channel_entry` (
  `id` int(11) NOT NULL auto_increment,
  `channel_id` int(11) default NULL,
  `entry_id` int(11) default NULL,
  `title` varchar(200) default NULL,
  `sorting` int(11) default NULL,
  `url` varchar(255) default NULL,
  `content` mediumtext,
  `pic` varchar(255) default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_channel_entry_channel_id` (`channel_id`),
  KEY `ix_channel_entry_title` (`title`),
  KEY `ix_channel_entry_sorting` (`sorting`),
  KEY `ix_channel_entry_entry_id` (`entry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `follow_node`
--

DROP TABLE IF EXISTS `follow_node`;
CREATE TABLE IF NOT EXISTS `follow_node` (
  `id` int(11) NOT NULL auto_increment,
  `people_id` int(11) NOT NULL,
  `node_id` int(11) NOT NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_follow_node_node_id` (`node_id`),
  KEY `ix_follow_node_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `group`
--

DROP TABLE IF EXISTS `group`;
CREATE TABLE IF NOT EXISTS `group` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(200) default NULL,
  `description` mediumtext,
  `people_id` int(11) NOT NULL,
  `tag` varchar(200) default NULL,
  `permission` int(11) default NULL,
  `timeup` int(11) default NULL,
  `status` int(11) default NULL,
  `avatar` varchar(400) default NULL,
  `people_count` int(11) default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_group_status` (`status`),
  KEY `ix_group_permission` (`permission`),
  KEY `ix_group_title` (`title`),
  KEY `ix_group_timeup` (`timeup`),
  KEY `ix_group_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- 表的结构 `group_follow`
--

DROP TABLE IF EXISTS `group_follow`;
CREATE TABLE IF NOT EXISTS `group_follow` (
  `id` int(11) NOT NULL auto_increment,
  `people_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_group_follow_group_id` (`group_id`),
  KEY `ix_group_follow_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `notify`
--

DROP TABLE IF EXISTS `notify`;
CREATE TABLE IF NOT EXISTS `notify` (
  `id` int(11) NOT NULL auto_increment,
  `sender` int(11) NOT NULL,
  `receiver` int(11) NOT NULL,
  `content` varchar(400) default NULL,
  `refer` varchar(600) default NULL,
  `type` varchar(20) default NULL,
  `created` datetime default NULL,
  `readed` varchar(1) default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_notify_receiver` (`receiver`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- 表的结构 `people`
--

DROP TABLE IF EXISTS `people`;
CREATE TABLE IF NOT EXISTS `people` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(100) default NULL,
  `nickname` varchar(100) default NULL,
  `email` varchar(200) default NULL,
  `password` varchar(100) default NULL,
  `avatar` varchar(400) default NULL,
  `website` varchar(400) default NULL,
  `role` int(11) default NULL,
  `reputation` int(11) default NULL,
  `token` varchar(16) default NULL,
  `city` varchar(200) default NULL,
  `status` int(11) default NULL,
  `description` mediumtext,
  `follow_count` int(11) default NULL,
  `followed_count` int(11) default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `ix_people_username` (`username`),
  UNIQUE KEY `ix_people_nickname` (`nickname`),
  KEY `ix_people_reputation` (`reputation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- 表的结构 `people_setting`
--

DROP TABLE IF EXISTS `people_setting`;
CREATE TABLE IF NOT EXISTS `people_setting` (
  `id` int(11) NOT NULL auto_increment,
  `people_id` int(11) NOT NULL,
  `github_name` varchar(200) default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_people_setting_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `social`
--

DROP TABLE IF EXISTS `social`;
CREATE TABLE IF NOT EXISTS `social` (
  `id` int(11) NOT NULL auto_increment,
  `user_id` int(11) NOT NULL,
  `enabled` varchar(1) default NULL,
  `service` varchar(100) default NULL,
  `token` mediumtext,
  PRIMARY KEY  (`id`),
  KEY `ix_social_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic`
--

DROP TABLE IF EXISTS `topic`;
CREATE TABLE IF NOT EXISTS `topic` (
  `id` int(11) NOT NULL auto_increment,
  `people_id` int(11) default NULL,
  `node_id` int(11) default NULL,
  `title` varchar(500) default NULL,
  `content` mediumtext,
  `format` varchar(100) default NULL,
  `status` varchar(50) default NULL,
  `hits` int(11) default NULL,
  `impact` float default NULL,
  `hidden` varchar(1) default NULL,
  `up_count` int(11) default NULL,
  `ups` mediumtext,
  `down_count` int(11) default NULL,
  `downs` mediumtext,
  `reply_count` int(11) default NULL,
  `last_reply_by` int(11) default NULL,
  `last_reply_time` datetime default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_topic_node_id` (`node_id`),
  KEY `ix_topic_people_id` (`people_id`),
  KEY `ix_topic_last_reply_time` (`last_reply_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_log`
--

DROP TABLE IF EXISTS `topic_log`;
CREATE TABLE IF NOT EXISTS `topic_log` (
  `id` int(11) NOT NULL auto_increment,
  `topic_id` int(11) NOT NULL,
  `people_id` int(11) NOT NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_topic_log_topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_node`
--

DROP TABLE IF EXISTS `topic_node`;
CREATE TABLE IF NOT EXISTS `topic_node` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `category` varchar(200) default NULL,
  `platform` int(11) default NULL,
  `avatar` varchar(400) default NULL,
  `description` varchar(1000) default NULL,
  `created` datetime default NULL,
  `last_updated` datetime default NULL,
  `limit_role` int(11) default NULL,
  `limit_title` int(11) default NULL,
  `limit_voice` int(11) default NULL,
  `sorting_by` varchar(50) default NULL,
  `topic_count` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_topic_node_category` (`category`),
  KEY `ix_topic_node_name` (`name`),
  KEY `ix_topic_node_platform` (`platform`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_reply`
--

DROP TABLE IF EXISTS `topic_reply`;
CREATE TABLE IF NOT EXISTS `topic_reply` (
  `id` int(11) NOT NULL auto_increment,
  `topic_id` int(11) default NULL,
  `people_id` int(11) default NULL,
  `content` varchar(2000) default NULL,
  `order` int(11) default NULL,
  `hidden` varchar(1) default NULL,
  `up_count` int(11) default NULL,
  `ups` mediumtext,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_topic_reply_order` (`order`),
  KEY `ix_topic_reply_people_id` (`people_id`),
  KEY `ix_topic_reply_topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_vote`
--

DROP TABLE IF EXISTS `topic_vote`;
CREATE TABLE IF NOT EXISTS `topic_vote` (
  `id` int(11) NOT NULL auto_increment,
  `people_id` int(11) NOT NULL,
  `topic_id` int(11) NOT NULL,
  `value` int(11) default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_topic_vote_people_id` (`people_id`),
  KEY `ix_topic_vote_topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `weibo`
--

DROP TABLE IF EXISTS `weibo`;
CREATE TABLE IF NOT EXISTS `weibo` (
  `id` int(11) NOT NULL auto_increment,
  `people_id` int(11) default NULL,
  `uid` varchar(30) NOT NULL,
  `domain` varchar(100) default NULL,
  `name` varchar(100) default NULL,
  `screen_name` varchar(100) default NULL,
  `province` varchar(100) default NULL,
  `city` varchar(100) default NULL,
  `location` varchar(100) default NULL,
  `avatar_small` varchar(200) default NULL,
  `avatar_large` varchar(200) default NULL,
  `token` mediumtext,
  `session_expires` int(11) default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_weibo_uid` (`uid`),
  KEY `ix_weibo_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;







DROP TABLE IF EXISTS `oh_my`;
CREATE TABLE IF NOT EXISTS `oh_my` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `start` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `duration` int(11) DEFAULT '0',
  `day` varchar(10) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_oh_shit_people_id` (`people_id`),
  KEY `ix_oh_shit_day` (`day`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `push_channel`
--

DROP TABLE IF EXISTS `push_channel`;
CREATE TABLE IF NOT EXISTS `push_channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `description` text,
  `group_id` int(11) DEFAULT NULL,
  `people_id` int(11) NOT NULL,
  `tag` varchar(200) DEFAULT NULL,
  `permission` int(11) DEFAULT NULL,
  `summary` text,
  `token` varchar(64) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_push_channel_permission` (`permission`),
  KEY `ix_push_channel_creator_id` (`people_id`),
  KEY `ix_push_channel_title` (`title`),
  KEY `ix_push_channel_group_id` (`group_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `push_channel_text`
--

DROP TABLE IF EXISTS `push_channel_text`;
CREATE TABLE IF NOT EXISTS `push_channel_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL,
  `content` text,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_push_channel_text_channel_id` (`channel_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `push_group`
--

DROP TABLE IF EXISTS `push_group`;
CREATE TABLE IF NOT EXISTS `push_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `description` text,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_push_group_title` (`title`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `push_text`
--

DROP TABLE IF EXISTS `push_text`;
CREATE TABLE IF NOT EXISTS `push_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `content` text,
  `sync` int(11) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_push_text_sync` (`sync`),
  KEY `ix_push_text_people_id` (`people_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;













