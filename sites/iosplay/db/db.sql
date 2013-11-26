-- phpMyAdmin SQL Dump
-- version 3.4.1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2013 年 09 月 23 日 22:02
-- 服务器版本: 5.1.56
-- PHP 版本: 5.3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- 数据库: `meiban`
--

-- --------------------------------------------------------

--
-- 表的结构 `food`
--

DROP TABLE IF EXISTS `food`;
CREATE TABLE IF NOT EXISTS `food` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `category` varchar(100) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=gbk AUTO_INCREMENT=1167 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_category`
--

DROP TABLE IF EXISTS `food_category`;
CREATE TABLE IF NOT EXISTS `food_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_food_category_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_ingredient`
--

DROP TABLE IF EXISTS `food_ingredient`;
CREATE TABLE IF NOT EXISTS `food_ingredient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `description` mediumtext,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_food_ingredient_category` (`category`)
) ENGINE=InnoDB  DEFAULT CHARSET=gbk AUTO_INCREMENT=1398 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_ingredient_nutrient`
--

DROP TABLE IF EXISTS `food_ingredient_nutrient`;
CREATE TABLE IF NOT EXISTS `food_ingredient_nutrient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ingredient_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `value` varchar(100) DEFAULT NULL,
  `unit` varchar(100) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_food_ingredient_nutrient_ingredient_id` (`ingredient_id`),
  KEY `ix_food_ingredient_nutrient_nutrient` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=gbk AUTO_INCREMENT=100513 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_note`
--

DROP TABLE IF EXISTS `food_note`;
CREATE TABLE IF NOT EXISTS `food_note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `content_id` int(11) DEFAULT NULL,
  `food_time` datetime DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `content_id` (`content_id`),
  KEY `ix_food_note_people_id` (`people_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_note_content`
--

DROP TABLE IF EXISTS `food_note_content`;
CREATE TABLE IF NOT EXISTS `food_note_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `breakfast` text,
  `lunch` text,
  `dinner` text,
  `food` text,
  `format` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_food_note_content_people_id` (`people_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=gbk AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_nutrient`
--

DROP TABLE IF EXISTS `food_nutrient`;
CREATE TABLE IF NOT EXISTS `food_nutrient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=gbk AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_unit`
--

DROP TABLE IF EXISTS `food_unit`;
CREATE TABLE IF NOT EXISTS `food_unit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(500) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_food_unit_unit` (`unit`),
  KEY `ix_food_unit_name` (`name`(383))
) ENGINE=InnoDB  DEFAULT CHARSET=gbk AUTO_INCREMENT=18 ;

-- --------------------------------------------------------

--
-- 表的结构 `food_unit_item`
--

DROP TABLE IF EXISTS `food_unit_item`;
CREATE TABLE IF NOT EXISTS `food_unit_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_id` int(11) DEFAULT NULL,
  `ingredient_id` int(11) DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_food_unit_ingredient_ingredient_id` (`ingredient_id`),
  KEY `ix_food_unit_ingredient_unit_id` (`unit_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=gbk AUTO_INCREMENT=23 ;

-- --------------------------------------------------------

--
-- 表的结构 `group`
--

DROP TABLE IF EXISTS `group`;
CREATE TABLE IF NOT EXISTS `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `description` text,
  `people_id` int(11) NOT NULL,
  `tag` varchar(200) DEFAULT NULL,
  `permission` int(11) DEFAULT '0',
  `status` int(11) DEFAULT '1',
  `avatar` varchar(400) DEFAULT NULL,
  `color` varchar(30) DEFAULT NULL,
  `people_count` int(11) DEFAULT '0',
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_group_title` (`title`),
  KEY `ix_group_status` (`status`),
  KEY `ix_group_people_id` (`people_id`),
  KEY `ix_group_permission` (`permission`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `group_follow`
--

DROP TABLE IF EXISTS `group_follow`;
CREATE TABLE IF NOT EXISTS `group_follow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_group_follow_people_id` (`people_id`),
  KEY `ix_group_follow_group_id` (`group_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `note`
--

DROP TABLE IF EXISTS `note`;
CREATE TABLE IF NOT EXISTS `note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `people_id` int(11) NOT NULL,
  `content_id` int(11) DEFAULT NULL,
  `tag` varchar(200) DEFAULT NULL,
  `permission` int(11) DEFAULT '0',
  `donot_reply` int(11) DEFAULT '1',
  `group_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_note_group_id` (`group_id`),
  KEY `ix_note_title` (`title`),
  KEY `ix_note_people_id` (`people_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- 表的结构 `note_content`
--

DROP TABLE IF EXISTS `note_content`;
CREATE TABLE IF NOT EXISTS `note_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `format` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- 表的结构 `notify`
--

DROP TABLE IF EXISTS `notify`;
CREATE TABLE IF NOT EXISTS `notify` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` int(11) NOT NULL,
  `receiver` int(11) NOT NULL,
  `content` varchar(400) DEFAULT NULL,
  `refer` varchar(600) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `readed` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_notify_receiver` (`receiver`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `people`
--

DROP TABLE IF EXISTS `people`;
CREATE TABLE IF NOT EXISTS `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT '',
  `password` varchar(100) NOT NULL,
  `avatar` varchar(400) DEFAULT NULL,
  `website` varchar(400) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `reputation` int(11) DEFAULT NULL,
  `token` varchar(16) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `edit_username_count` int(11) DEFAULT NULL,
  `description` text,
  `follow_count` int(11) NOT NULL DEFAULT '0',
  `followed_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_people_username` (`username`),
  KEY `ix_people_reputation` (`reputation`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=22 ;

-- --------------------------------------------------------

--
-- 表的结构 `people_added_link`
--

DROP TABLE IF EXISTS `people_added_link`;
CREATE TABLE IF NOT EXISTS `people_added_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_id` int(11) DEFAULT NULL,
  `people_id` int(11) NOT NULL,
  `category` varchar(30) DEFAULT NULL,
  `definition` varchar(30) DEFAULT NULL,
  `link_id` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `title` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_people_added_link_people_id` (`people_id`),
  KEY `ix_people_added_link_entity_id` (`entity_id`),
  KEY `created` (`created`),
  KEY `category` (`category`),
  KEY `definity` (`definition`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

-- --------------------------------------------------------

--
-- 表的结构 `people_follower`
--

DROP TABLE IF EXISTS `people_follower`;
CREATE TABLE IF NOT EXISTS `people_follower` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_people_follower_target_id` (`target_id`),
  KEY `ix_people_follower_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `people_likes_boards`
--

DROP TABLE IF EXISTS `people_likes_boards`;
CREATE TABLE IF NOT EXISTS `people_likes_boards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `boards` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_people_likes_boards_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `social`
--

DROP TABLE IF EXISTS `social`;
CREATE TABLE IF NOT EXISTS `social` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `enabled` varchar(1) DEFAULT NULL,
  `service` varchar(100) DEFAULT NULL,
  `token` text,
  PRIMARY KEY (`id`),
  KEY `ix_social_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `tag`
--

DROP TABLE IF EXISTS `tag`;
CREATE TABLE IF NOT EXISTS `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(250) NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `value` (`value`),
  KEY `ix_tag_value` (`value`),
  KEY `type` (`type`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=62 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic`
--

DROP TABLE IF EXISTS `topic`;
CREATE TABLE IF NOT EXISTS `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `node_id` int(11) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `content` text,
  `format` varchar(100) DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  `hits` int(11) DEFAULT NULL,
  `impact` float DEFAULT '0',
  `up_count` int(11) DEFAULT NULL,
  `ups` text,
  `down_count` int(11) DEFAULT NULL,
  `downs` text,
  `reply_count` int(11) DEFAULT NULL,
  `last_reply_by` int(11) DEFAULT NULL,
  `last_reply_time` datetime DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_people_id` (`people_id`),
  KEY `ix_topic_last_reply_time` (`last_reply_time`),
  KEY `ix_topic_node_id` (`node_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=21 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_log`
--

DROP TABLE IF EXISTS `topic_log`;
CREATE TABLE IF NOT EXISTS `topic_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL,
  `people_id` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_log_topic_id` (`topic_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_node`
--

DROP TABLE IF EXISTS `topic_node`;
CREATE TABLE IF NOT EXISTS `topic_node` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `category` varchar(200) DEFAULT NULL,
  `platform` int(11) NOT NULL DEFAULT '0',
  `avatar` varchar(400) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL,
  `limit_role` int(11) DEFAULT NULL,
  `limit_title` int(11) DEFAULT NULL,
  `limit_voice` int(11) DEFAULT NULL,
  `sorting_by` varchar(50) DEFAULT NULL,
  `topic_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_node_category` (`category`),
  KEY `ix_topic_node_name` (`name`),
  KEY `platform` (`platform`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=13 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_reply`
--

DROP TABLE IF EXISTS `topic_reply`;
CREATE TABLE IF NOT EXISTS `topic_reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) DEFAULT NULL,
  `people_id` int(11) DEFAULT NULL,
  `content` text,
  `up_count` int(11) DEFAULT NULL,
  `ups` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_reply_topic_id` (`topic_id`),
  KEY `ix_topic_reply_people_id` (`people_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=42 ;

-- --------------------------------------------------------

--
-- 表的结构 `topic_vote`
--

DROP TABLE IF EXISTS `topic_vote`;
CREATE TABLE IF NOT EXISTS `topic_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `topic_id` int(11) NOT NULL,
  `value` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `ix_topic_id` (`topic_id`),
  KEY `ix_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `weibo`
--

DROP TABLE IF EXISTS `weibo`;
CREATE TABLE IF NOT EXISTS `weibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `uid` int(11) NOT NULL,
  `domain` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `screen_name` varchar(100) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `avatar_small` varchar(200) DEFAULT NULL,
  `avatar_large` varchar(200) DEFAULT NULL,
  `token` text,
  `session_expires` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_weibo_people_id` (`people_id`),
  KEY `ix_weibo_uid` (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;


DROP TABLE IF EXISTS `food_pregnancy`;
CREATE TABLE IF NOT EXISTS `food_pregnancy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `food_id` int(11) NULL,
  `name` varchar(200) NOT NULL,
  `permission` varchar(50)  NULL,
  `sorting` int(11) NOT NULL,
  `tips` text  NULL,
  `created` datetime  NULL,
  PRIMARY KEY (`id`),
  KEY `food_id` (`food_id`,`permission`),
  KEY `permission` (`permission`),
  KEY `sorting` (`sorting`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;




DROP TABLE IF EXISTS `food_comment`;
CREATE TABLE IF NOT EXISTS `food_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `food_id` int(11) DEFAULT NULL,
  `people_id` int(11) DEFAULT NULL,
  `content` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_food_id` (`food_id`),
  KEY `ix_people_id` (`people_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;


DROP TABLE IF EXISTS `channel`;
CREATE TABLE IF NOT EXISTS `channel` (
  `id` int(11) NOT NULL auto_increment,
  `title` varchar(200) default NULL,
  `isa` varchar(100) default NULL,
  `pic` varchar(255) default NULL,
  `sorting` int(11) default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_channel_title` (`title`),
  KEY `isa` (`isa`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `channel_entity`
--

DROP TABLE IF EXISTS `channel_entry`;
CREATE TABLE IF NOT EXISTS `channel_entry` (
  `id` int(11) NOT NULL auto_increment,
  `channel_id` int(11) default NULL,
  `entry_id` int(11) default NULL,
  `title` varchar(200) default NULL,
  `pic` varchar(255) default NULL,
  `content` Text default NULL,
  `url` varchar(255) default NULL,
  `sorting` int(11) default NULL,
  `created` datetime default NULL,
  PRIMARY KEY  (`id`),
  KEY `ix_title` (`title`),
  KEY `ix_entry_id` (`entry_id`),
  KEY `ix_sorting` (`sorting`),
  KEY `ix_channel_id` (`channel_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `people_setting`;
CREATE TABLE IF NOT EXISTS `people_setting` (
  `id` int(11) NOT NULL auto_increment,
  `people_id` int(11) NOT NULL,
  `stat_type` int(11) NOT NULL default '0',
  `stat_date` datetime default NULL,
  `pregnancy_week` int(11) default NULL,
  `pregnancy_day` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8 AUTO_INCREMENT=1 ;


