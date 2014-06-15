-- MySQL dump 10.13  Distrib 5.6.17, for osx10.7 (x86_64)
--
-- Host: localhost    Database: wecoders
-- ------------------------------------------------------
-- Server version	5.6.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- create database wecoders CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci';
-- ALTER DATABASE `wecoders` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci';

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel`
--

LOCK TABLES `channel` WRITE;
/*!40000 ALTER TABLE `channel` DISABLE KEYS */;
/*!40000 ALTER TABLE `channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channel_entry`
--

DROP TABLE IF EXISTS `channel_entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel_entry`
--

LOCK TABLES `channel_entry` WRITE;
/*!40000 ALTER TABLE `channel_entry` DISABLE KEYS */;
/*!40000 ALTER TABLE `channel_entry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notify`
--

DROP TABLE IF EXISTS `notify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notify`
--

LOCK TABLES `notify` WRITE;
/*!40000 ALTER TABLE `notify` DISABLE KEYS */;
/*!40000 ALTER TABLE `notify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people`
--

DROP TABLE IF EXISTS `people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people`
--

LOCK TABLES `people` WRITE;
/*!40000 ALTER TABLE `people` DISABLE KEYS */;
INSERT INTO `people` VALUES (1,'admin','admin','admin@test.com','SGJVCbEB$0f4310bc5a12f8a33c3f034c82235854f204d0d3',NULL,NULL,9,100,'mImE2ywfBmwoWkzRkZuCtYf6Ge07boxy',NULL,0,NULL,0,0,'2014-06-11 05:49:42');
/*!40000 ALTER TABLE `people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people_setting`
--

DROP TABLE IF EXISTS `people_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `github_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_people_setting_people_id` (`people_id`),
  CONSTRAINT `people_setting_ibfk_1` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people_setting`
--

LOCK TABLES `people_setting` WRITE;
/*!40000 ALTER TABLE `people_setting` DISABLE KEYS */;
/*!40000 ALTER TABLE `people_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social`
--

DROP TABLE IF EXISTS `social`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `enabled` varchar(1) DEFAULT NULL,
  `service` varchar(100) DEFAULT NULL,
  `token` text,
  PRIMARY KEY (`id`),
  KEY `ix_social_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social`
--

LOCK TABLES `social` WRITE;
/*!40000 ALTER TABLE `social` DISABLE KEYS */;
/*!40000 ALTER TABLE `social` ENABLE KEYS */;
UNLOCK TABLES;



DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) DEFAULT NULL,
  `node_id` int(11) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `content_id` int(11) DEFAULT NULL,
  `format` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `hits` int(11) DEFAULT NULL,
  `anonymous` int(11) DEFAULT NULL,
  `up_count` int(11) DEFAULT NULL,
  `ups` text,
  `down_count` int(11) DEFAULT NULL,
  `downs` text,
  `reply_count` int(11) DEFAULT NULL,
  `last_reply_time` datetime DEFAULT NULL,
  `last_reply_by` int(11) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_node_id` (`node_id`),
  KEY `ix_topic_people_id` (`people_id`),
  KEY `ix_topic_last_reply_time` (`last_reply_time`),
  CONSTRAINT `topic_ibfk_1` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`),
  CONSTRAINT `topic_ibfk_2` FOREIGN KEY (`node_id`) REFERENCES `topic_node` (`id`)
);

--
-- Table structure for table `topic_log`
--

DROP TABLE IF EXISTS `topic_log`;

CREATE TABLE `topic_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL,
  `people_id` int(11) NOT NULL,
  `event` text DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_log_topic_id` (`topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `topic_log`
--

LOCK TABLES `topic_log` WRITE;
/*!40000 ALTER TABLE `topic_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `topic_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_node`
--

DROP TABLE IF EXISTS `topic_node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_node`
--

LOCK TABLES `topic_node` WRITE;
/*!40000 ALTER TABLE `topic_node` DISABLE KEYS */;
INSERT INTO `topic_node` VALUES (1,'swift','Swift','life',0,NULL,'lieft','2014-06-11 05:54:23','2014-06-11 05:54:23','-id',0);
/*!40000 ALTER TABLE `topic_node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_node_follower`
--

DROP TABLE IF EXISTS `topic_node_follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic_node_follower` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `people_id` int(11) NOT NULL,
  `node_id` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_node_follower_people_id` (`people_id`),
  KEY `ix_topic_node_follower_node_id` (`node_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_node_follower`
--

LOCK TABLES `topic_node_follower` WRITE;
/*!40000 ALTER TABLE `topic_node_follower` DISABLE KEYS */;
/*!40000 ALTER TABLE `topic_node_follower` ENABLE KEYS */;
UNLOCK TABLES;



DROP TABLE IF EXISTS `topic_reply`;
CREATE TABLE `topic_reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) DEFAULT NULL,
  `people_id` int(11) DEFAULT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `content_html` text DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `anonymous` int(11) DEFAULT NULL,
  `up_count` int(11) DEFAULT NULL,
  `ups` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_reply_order` (`order`),
  KEY `ix_topic_reply_topic_id` (`topic_id`),
  KEY `ix_topic_reply_people_id` (`people_id`),
  CONSTRAINT `topic_reply_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`),
  CONSTRAINT `topic_reply_ibfk_2` FOREIGN KEY (`people_id`) REFERENCES `people` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `topic_vote`
--

DROP TABLE IF EXISTS `topic_vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_vote`
--

LOCK TABLES `topic_vote` WRITE;
/*!40000 ALTER TABLE `topic_vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `topic_vote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weibo`
--

DROP TABLE IF EXISTS `weibo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weibo`
--

LOCK TABLES `weibo` WRITE;
/*!40000 ALTER TABLE `weibo` DISABLE KEYS */;
/*!40000 ALTER TABLE `weibo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-06-11 14:12:51
