-- MySQL dump 10.13  Distrib 5.6.17, for osx10.7 (x86_64)
--
-- Host: localhost    Database: wecoders
-- ------------------------------------------------------
-- Server version 5.6.17

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
CREATE TABLE `channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) DEFAULT NULL,
  `isa` varchar(50) DEFAULT NULL,
  `pic` varchar(255) DEFAULT NULL,
  `sorting` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_channel_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `channel`
--

--
-- Table structure for table `channel_entry`
--

DROP TABLE IF EXISTS `channel_entry`;
CREATE TABLE `channel_entry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) DEFAULT NULL,
  `entry_id` int(11) DEFAULT NULL,
  `title` varchar(200) DEFAULT NULL,
  `sorting` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `content` text,
  `pic` varchar(255) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_channel_entry_channel_id` (`channel_id`),
  KEY `ix_channel_entry_entry_id` (`entry_id`),
  KEY `ix_channel_entry_sorting` (`sorting`),
  KEY `ix_channel_entry_title` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `notify`
--

DROP TABLE IF EXISTS `notify`;
CREATE TABLE `notify` (
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `people`
--

DROP TABLE IF EXISTS `people`;
CREATE TABLE `people` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `avatar` varchar(400) DEFAULT NULL,
  `website` varchar(400) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `reputation` int(11) DEFAULT NULL,
  `token` varchar(32) DEFAULT NULL,
  `city` varchar(200) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `description` text,
  `follow_count` int(11) DEFAULT NULL,
  `followed_count` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_people_username` (`username`),
  UNIQUE KEY `ix_people_nickname` (`nickname`),
  KEY `ix_people_reputation` (`reputation`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Table structure for table `people_setting`
--

DROP TABLE IF EXISTS `people_setting`;
CREATE TABLE `people_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `github_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_people_setting_people_id` (`people_id`),
  CONSTRAINT `people_setting_ibfk_1` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `social`
--

DROP TABLE IF EXISTS `social`;
CREATE TABLE `social` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `uid` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `enabled` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `service` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `token` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `ix_social_user_id` (`user_id`),
  KEY `ix_social_service` (`service`),
  KEY `ix_social_uid` (`uid`),
  CONSTRAINT `social_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `social`
--

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `node_id` int(11) DEFAULT NULL,
  `title` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `content` text COLLATE utf8_unicode_ci,
  `format` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hits` int(11) DEFAULT NULL,
  `anonymous` int(11) DEFAULT NULL,
  `up_count` int(11) DEFAULT NULL,
  `ups` text COLLATE utf8_unicode_ci,
  `down_count` int(11) DEFAULT NULL,
  `downs` text COLLATE utf8_unicode_ci,
  `reply_count` int(11) DEFAULT NULL,
  `last_reply_time` datetime DEFAULT NULL,
  `last_reply_by` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `content_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_node_id` (`node_id`),
  KEY `ix_topic_people_id` (`people_id`),
  KEY `ix_topic_last_reply_time` (`last_reply_time`),
  CONSTRAINT `topic_ibfk_1` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`),
  CONSTRAINT `topic_ibfk_2` FOREIGN KEY (`node_id`) REFERENCES `topic_node` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `topic`
--


--
-- Table structure for table `topic_content`
--

DROP TABLE IF EXISTS `topic_content`;
CREATE TABLE `topic_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text COLLATE utf8_unicode_ci,
  `content_html` text COLLATE utf8_unicode_ci,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `topic_content`
--

--
-- Table structure for table `topic_log`
--

DROP TABLE IF EXISTS `topic_log`;
CREATE TABLE `topic_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL,
  `people_id` int(11) NOT NULL,
  `event` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_log_topic_id` (`topic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `topic_node`
--

DROP TABLE IF EXISTS `topic_node`;
CREATE TABLE `topic_node` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `title` varchar(200) NOT NULL,
  `category` varchar(200) DEFAULT NULL,
  `anonymous` int(11) DEFAULT NULL,
  `avatar` varchar(400) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL,
  `sorting` varchar(50) DEFAULT NULL,
  `topic_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_node_category` (`category`),
  KEY `ix_topic_node_name` (`name`),
  KEY `ix_topic_node_anonymous` (`anonymous`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `topic_node_follower`
--

DROP TABLE IF EXISTS `topic_node_follower`;
CREATE TABLE `topic_node_follower` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `node_id` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_node_follower_people_id` (`people_id`),
  KEY `ix_topic_node_follower_node_id` (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `topic_reply`
--

DROP TABLE IF EXISTS `topic_reply`;
CREATE TABLE `topic_reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) DEFAULT NULL,
  `people_id` int(11) DEFAULT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `anonymous` int(11) DEFAULT NULL,
  `up_count` int(11) DEFAULT NULL,
  `ups` text,
  `created` datetime DEFAULT NULL,
  `content_html` text,
  PRIMARY KEY (`id`),
  KEY `ix_topic_reply_order` (`order`),
  KEY `ix_topic_reply_topic_id` (`topic_id`),
  KEY `ix_topic_reply_people_id` (`people_id`),
  CONSTRAINT `topic_reply_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`),
  CONSTRAINT `topic_reply_ibfk_2` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `topic_vote`
--

DROP TABLE IF EXISTS `topic_vote`;
CREATE TABLE `topic_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `topic_id` int(11) NOT NULL,
  `value` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_vote_people_id` (`people_id`),
  KEY `ix_topic_vote_topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `weibo`
--

DROP TABLE IF EXISTS `weibo`;
CREATE TABLE `weibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `uid` varchar(30) NOT NULL,
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
  KEY `ix_weibo_uid` (`uid`),
  KEY `ix_weibo_people_id` (`people_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

