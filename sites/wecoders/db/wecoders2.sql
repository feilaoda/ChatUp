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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people`
--

LOCK TABLES `people` WRITE;
/*!40000 ALTER TABLE `people` DISABLE KEYS */;
INSERT INTO `people` VALUES (1,'admin','admin','admin@test.com','SGJVCbEB$0f4310bc5a12f8a33c3f034c82235854f204d0d3',NULL,NULL,9,100,'mImE2ywfBmwoWkzRkZuCtYf6Ge07boxy',NULL,0,NULL,0,0,'2014-06-11 05:49:42'),(2,'test','test','test@test.cm','W18RKbkn$45b0983bc224b2f9f5815c141c2955d38d90715d',NULL,NULL,2,100,'cM5hMmEHkwXvh7EK2hRZLK9betuUW7Y1',NULL,0,NULL,0,0,'2014-06-11 07:10:04'),(3,'jobxx','jobxx','test@job.com','W6d3DtUq$87fbd47c8a9e2a2017dda29bfad010b0ed54ca20',NULL,NULL,2,100,'iPaA5UxTH7gPe9mbXe5g0ja2zeGHEgLF',NULL,0,NULL,0,0,'2014-06-13 03:43:14'),(4,'feilaoda','feilaoda',NULL,'c8g4YZCS',NULL,NULL,2,100,'NfcNuiIV',NULL,0,NULL,0,0,'2014-06-18 11:43:27');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social`
--

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--


--
-- Table structure for table `topic_content`
--

DROP TABLE IF EXISTS `topic_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text COLLATE utf8_unicode_ci,
  `content_html` text COLLATE utf8_unicode_ci,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_content`
--

LOCK TABLES `topic_content` WRITE;
/*!40000 ALTER TABLE `topic_content` DISABLE KEYS */;
INSERT INTO `topic_content` VALUES (2,'sdddok',NULL,'2014-06-15 00:09:03'),(3,'<app.topic.models.TopicContent object at 0x1038fee50>',NULL,'2014-06-15 00:13:43'),(4,'',NULL,'2014-06-15 02:39:14'),(5,'ReplyReplyReplyReplyReply\r\nd\r\ndd\r\nhello',NULL,'2014-06-15 02:40:42'),(6,'个人简介\r\n\r\n李浩，腾讯云高级工程师，对海量接入、高可靠服务架构、数据一致性等方面有丰富经验，目前专注于为腾讯游戏云厂商提供高品质的产品和服务。',NULL,'2014-06-15 13:34:07'),(7,'test',NULL,'2014-06-17 01:53:41'),(8,'一直处在神坛顶端的linode vps打破了10几年来的规矩，将最低套餐由20美元一个月降低到最低套餐每个月10美元起步，具体配置为：1G内存（XEN），1核（E5-',NULL,'2014-06-17 01:54:13'),(9,'',NULL,'2014-06-17 01:54:22'),(10,'',NULL,'2014-06-17 01:54:30'),(11,'',NULL,'2014-06-17 01:54:39'),(12,'',NULL,'2014-06-17 01:56:47'),(13,'',NULL,'2014-06-17 02:01:46'),(14,'',NULL,'2014-06-17 02:01:54'),(15,'',NULL,'2014-06-17 02:02:00'),(16,'',NULL,'2014-06-17 02:02:06'),(17,'',NULL,'2014-06-17 02:02:12'),(18,'',NULL,'2014-06-17 02:02:18'),(23,'',NULL,'2014-06-17 02:18:09'),(24,'',NULL,'2014-06-17 02:19:27'),(25,'topic = Topic()\r\n重磅消息:linode-$10/月/1g内存/24gSSD/2T流量/送10美元\r\n2014年6月16日 | 作者: admin | 分类: 优惠码 |	 标签: linode, linode vps, linode优惠码	 | 19条评论\r\n一直处在神坛顶端的linode vps打破了10几年来的规矩，将最低套餐由20美元一个月降低到最低套餐每个月10美元起步，具体配置为：1G内存（XEN），1核（E5-2680V2）,24G SSD,2T流量，有美国达拉斯、纽约、亚特兰大、弗里蒙特\\英国伦敦\\日本东京这几个数据中心。大家知道digitalocean 和 vultr等类似的后起之秀开始逐渐蚕食这个市场，linode迫不得已已经进行了多次升级，这次的10美元套餐着实让我吃了一惊。如果你不知道linode的话围观下我以前的文章：linode vps 介绍   linode vps购买教程   Linode VPS测评/新版SSD盘/E5-2680V2   围观官方：www.linode.com\r\n\r\nLinode官方送10美元，优惠码：LINODE10  围观官方：www.linode.com',NULL,'2014-06-17 02:23:00');
/*!40000 ALTER TABLE `topic_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic_log`
--

DROP TABLE IF EXISTS `topic_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topic_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL,
  `people_id` int(11) NOT NULL,
  `event` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_topic_log_topic_id` (`topic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_log`
--

LOCK TABLES `topic_log` WRITE;
/*!40000 ALTER TABLE `topic_log` DISABLE KEYS */;
INSERT INTO `topic_log` VALUES (5,10,3,'edit topic: [如何修改UIPageViewController的点的颜色？,<app.topic.models.TopicContent object at 0x1038fee50>]','2014-06-15 02:44:55'),(6,12,3,'edit topic: [iOS开源资源汇集网站,ReplyReplyReplyReplyReply\r\nd\r\ndd]','2014-06-15 02:46:56'),(7,12,3,'edit topic: [iOS开源资源汇集网站,ReplyReplyReplyReplyReply\r\nd\r\ndd\r\nhello]','2014-06-15 02:47:03'),(8,13,1,'edit topic: [测试中文支持,个人简介\r\n\r\n李浩，腾讯云高级工程师，对海量接入、高可靠服务架构、数据一致性等方面有丰富经验，目前专注于为腾讯游戏云厂商提供高品质的产品和服务。]','2014-06-15 13:34:23');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_node`
--

LOCK TABLES `topic_node` WRITE;
/*!40000 ALTER TABLE `topic_node` DISABLE KEYS */;
INSERT INTO `topic_node` VALUES (1,'swift','Swift','life',0,NULL,'lieft','2014-06-11 05:54:23','2014-06-11 07:19:11','-id',2),(2,'ios','iOS开源资源汇集网站','dev',0,NULL,'phpMyAdmin','2014-06-11 06:33:05','2014-06-15 02:40:42','-id',3),(3,'fuli','福利','娱乐',1,'','','2014-06-11 07:20:18','2014-06-13 03:43:25','-id',1),(4,'fulitwo','fuli2','',1,NULL,'','2014-06-11 07:25:10','2014-06-17 02:23:00','-id',23);
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

--
-- Table structure for table `topic_reply`
--

DROP TABLE IF EXISTS `topic_reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic_reply`
--

LOCK TABLES `topic_reply` WRITE;
/*!40000 ALTER TABLE `topic_reply` DISABLE KEYS */;
INSERT INTO `topic_reply` VALUES (18,10,3,'Anonymous','nnn',1,0,0,NULL,'2014-06-15 00:35:21',NULL),(19,9,3,'Anonymous','class=\"badge\"class=\"badge\"class=\"badge\"class=\"badge\"',1,0,0,NULL,'2014-06-15 00:37:50',NULL),(20,11,3,'Anonymous','Reply',1,0,0,NULL,'2014-06-15 02:39:54',NULL),(21,10,3,'Anonymous','Back To Top',2,0,0,NULL,'2014-06-15 02:41:52',NULL),(22,10,3,'Anonymous','Back To TopBack To TopBack To Top',3,0,0,NULL,'2014-06-15 02:41:55',NULL),(23,14,2,'Anonymous','test',1,0,0,NULL,'2014-06-17 01:53:44',NULL);
/*!40000 ALTER TABLE `topic_reply` ENABLE KEYS */;
UNLOCK TABLES;

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

-- Dump completed on 2014-06-19  9:33:23
