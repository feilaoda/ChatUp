-- phpMyAdmin SQL Dump
-- version 3.4.10.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 16, 2013 at 10:15 AM
-- Server version: 5.0.27
-- PHP Version: 5.2.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `meiban`
--

--
-- Dumping data for table `food_note`
--

INSERT INTO `food_note` (`id`, `people_id`, `content_id`, `note_time`, `created`) VALUES
(1, 20, 1, '2013-09-14 00:00:00', '2013-09-16 05:30:39');

--
-- Dumping data for table `food_note_content`
--

INSERT INTO `food_note_content` (`id`, `people_id`, `breakfast`, `lunch`, `dinner`, `others`, `format`) VALUES
(1, 20, '', '', '', '2小碗绿豆粥\r\n1个鸡蛋\r\n1个玉米\r\n1个石榴\r\n\r\n半碗米饭\r\n一点菜\r\n一个橘子\r\n\r\n一个猕猴桃\r\n一点薯片\r\n一个番茄\r\n\r\n一碗面条', NULL);

--
-- Dumping data for table `food_unit`
--

INSERT INTO `food_unit` (`id`, `name`, `unit`, `created`) VALUES
(1, '鸡蛋', '个', NULL),
(2, '绿豆粥', '小碗', NULL),
(3, '石榴', '个', NULL),
(4, '米饭', '碗', NULL),
(5, '猕猴桃', '个', NULL),
(6, '番茄', '个', '2013-09-16 09:17:00'),
(7, '面条', '碗', '2013-09-16 09:58:25'),
(8, '薯片', '点', '2013-09-16 10:01:25'),
(9, '玉米', '个', '2013-09-16 10:02:53'),
(10, '菜', '点', '2013-09-16 10:03:49');

--
-- Dumping data for table `food_unit_item`
--

INSERT INTO `food_unit_item` (`id`, `unit_id`, `ingredient_id`, `weight`, `created`) VALUES
(1, 1, 517, 50, NULL),
(2, 2, 136, 30, NULL),
(4, 3, 353, 400, NULL),
(5, 4, 1211, 200, NULL),
(9, 2, 32, 40, '2013-09-16 08:48:18'),
(10, 5, 362, 40, '2013-09-16 09:15:16'),
(11, 6, 187, 400, '2013-09-16 09:27:14'),
(12, 7, 71, 200, '2013-09-16 09:59:37'),
(13, 8, 1390, 50, '2013-09-16 10:02:26'),
(14, 9, 26, 200, '2013-09-16 10:03:20'),
(15, 10, 225, 50, '2013-09-16 10:06:51');

--
-- Dumping data for table `people`
--

INSERT INTO `people` (`id`, `username`, `nickname`, `email`, `password`, `avatar`, `website`, `role`, `reputation`, `token`, `created`, `city`, `edit_username_count`, `description`, `follow_count`, `followed_count`) VALUES
(20, 'admin', 'admin', 'admin@example.com', '9nlDCmw4$8ff35735f4ff0eb97c434f6ac610c31874ad8e77', 'http://test.imeiban.com/static/avatar/thb_20_s_1379061970.jpg', NULL, 9, 100, 'nGCGaMWezWDAMwVI', '2013-09-13 02:07:21', NULL, 2, NULL, 0, 0);

--
-- Dumping data for table `topic`
--

INSERT INTO `topic` (`id`, `people_id`, `node_id`, `title`, `content`, `format`, `status`, `hits`, `impact`, `up_count`, `ups`, `down_count`, `downs`, `reply_count`, `last_reply_by`, `last_reply_time`, `created`) VALUES
(11, 20, 6, 'test', 'wom                   \r\n罕见的复古太阳镜，材质细节很考究，性价比太高了，这个眼睛的做工和包装可以和大牌...', 'html', NULL, 1, 0, 0, NULL, 0, NULL, 0, NULL, '2013-09-13 02:17:37', '2013-09-13 02:17:37'),
(12, 20, 6, '<a href="/topic">{{_("community")}}</a><span></span> »', '', 'html', NULL, 1, 0, 0, NULL, 0, NULL, 0, NULL, '2013-09-13 02:23:39', '2013-09-13 02:23:39'),
(13, 20, 6, '期里面尝试过C++、C#、Lua、Basic、Php、Javascript、Flex。 //@灵感之源:技术发展快，跟不上潮流要被淘汰啊', 'lessc --compress static/stylesheets/movie.less >> \r\n$(STATIC)/assets/css/application.min.css', 'html', NULL, 1, 0, 0, NULL, 0, NULL, 2, 20, '2013-09-13 03:45:51', '2013-09-13 02:23:47'),
(14, 20, 6, '与2有着本质的区别，……哥哥就是老衲看透红尘……傻：有些人明知道你是在玩Ta，于是就陪你一块玩，因为Ta也想玩你一把，玩到最后都成了大家的笑柄，相互诋毁；2：你明明是在玩Ta，可Ta就是看不出来，还陪你一起哭，一起笑，一起闯祸，一起患难……玩到最后你们会相互感觉欠对方太多，你后悔自己做的太过火，Ta却悔恨 ok', '昨天Russia to Limit Snowden''s Speech   [VOA慢速英语] (24人听过)\r\n2013-09-11Rising Temperatures Could Mean More Wildfires   [VOA慢速英语] (32人听过)\r\n2013-09-10The Growing Threat From Extremist Groups   [VOA慢速英语] (37人听过)\r\n2013-09-09Free Education for Poor Kenyan Girls   [VOA慢速英语] (21人听过)\r\n2013-09-08Understanding Corporate Structure   [ESL Podcast] (31人听过)\r\n2013-09-08Forty Years of Harmony: China and the Philadelphia Orchestra   [VOA慢速英语] (32人听过)\r\n2013-09-08The City of Brotherly Love, and Beantown   [VOA慢速英语] (22人听过)\r\n2013-09-07Are Smarthphones Ruining the Concert Experience?   [VOA慢速英语] (31人听过)\r\n2013-09-07US Senate Committee Approves Use of Force in Syria   [VOA慢速英语] (31人听过)\r\n2013-09-06Needy Kids In Virginia Get Supplied for School   [VOA慢速英语] (21人听过)\r\n2013-09-06US Lawmakers Prepare for Budget Debate Over Health Care Law   [VOA慢速英语] (22人听过)\r\n2013-09-05Being Tidy and Messy   [ESL Podcast] (26人听过)\r\n2013-09-05Andrew Jackson and the Election of 1828 - The Making of a Nation No.', 'html', NULL, 1, 0, 0, NULL, 0, NULL, 0, NULL, '2013-09-13 03:46:27', '2013-09-13 03:46:27'),
(15, 20, 7, '期里面尝试过C++、C#、Lua、Basic、Php、Javascript、Flex。 //@灵感之源:技术发展快，跟不上潮流要被淘汰啊', '', 'html', NULL, 1, 0, 0, NULL, 0, NULL, 0, NULL, '2013-09-13 03:57:39', '2013-09-13 03:57:39');

--
-- Dumping data for table `topic_log`
--

INSERT INTO `topic_log` (`id`, `topic_id`, `people_id`, `created`) VALUES
(5, 13, 20, '2013-09-13 03:45:23'),
(6, 13, 20, '2013-09-13 03:45:30'),
(7, 13, 20, '2013-09-13 03:45:35'),
(8, 13, 20, '2013-09-13 03:45:41'),
(9, 14, 20, '2013-09-13 07:09:51');

--
-- Dumping data for table `topic_node`
--

INSERT INTO `topic_node` (`id`, `name`, `title`, `category`, `platform`, `avatar`, `description`, `created`, `last_updated`, `limit_role`, `limit_title`, `limit_voice`, `sorting_by`, `topic_count`) VALUES
(6, 'pregnancy1w', '孕期第1周', 'health', 0, NULL, '孕期第1周', '2013-09-13 02:15:35', '2013-09-13 03:46:27', 0, 0, 0, '-id', 4),
(7, 'pregnancy2w', '孕期第2周', 'health', 0, NULL, '孕期第2周', '2013-09-13 03:57:30', '2013-09-13 03:57:39', 0, 0, 0, '-id', 1);

--
-- Dumping data for table `topic_reply`
--

INSERT INTO `topic_reply` (`id`, `topic_id`, `people_id`, `content`, `up_count`, `ups`, `created`) VALUES
(36, 13, 20, 'lessc --compress static/stylesheets/movie.less >> $(STATIC)/assets/css/application.min.css', 0, NULL, '2013-09-13 03:44:33'),
(37, 13, 20, '与2有着本质的区别，……哥哥就是老衲看透红尘……傻：有些人明知道你是在玩Ta，于是就陪你一块玩，因为Ta也想玩你一把，玩到最后都成了大家的笑柄，相互诋毁；2：你明明是在玩Ta，可Ta就是看不出来，还陪你一起哭，一起笑，一起闯祸，一起患难……玩到最后你们会相互感觉欠对方太多，你后悔自己做的太过火，Ta却悔恨', 0, NULL, '2013-09-13 03:45:51');
