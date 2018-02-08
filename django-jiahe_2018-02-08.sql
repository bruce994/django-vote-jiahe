# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: sh-cdb-qenvqae8.sql.tencentcdb.com (MySQL 5.5.45-log)
# Database: django-jiahe
# Generation Time: 2018-02-08 03:30:09 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table vote_ad
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_ad`;

CREATE TABLE `vote_ad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `title` varchar(30) NOT NULL,
  `image` varchar(200) NOT NULL,
  `pub_date` datetime NOT NULL,
  `vid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_ad_vid_id_c2ed5625_fk_vote_vote_id` (`vid_id`),
  CONSTRAINT `vote_ad_vid_id_c2ed5625_fk_vote_vote_id` FOREIGN KEY (`vid_id`) REFERENCES `vote_vote` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_ad` WRITE;
/*!40000 ALTER TABLE `vote_ad` DISABLE KEYS */;

INSERT INTO `vote_ad` (`id`, `mid`, `title`, `image`, `pub_date`, `vid_id`)
VALUES
	(6,1,'广告2','_versions/582a7cdf74b12_medium.png','2018-01-17 11:25:49',1);

/*!40000 ALTER TABLE `vote_ad` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_form
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_form`;

CREATE TABLE `vote_form` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `openid` varchar(200) NOT NULL,
  `username` varchar(30) NOT NULL,
  `tel` varchar(30) NOT NULL,
  `image0` varchar(500) NOT NULL,
  `image1` varchar(500) NOT NULL,
  `image2` varchar(500) NOT NULL,
  `image3` varchar(500) NOT NULL,
  `image4` varchar(500) NOT NULL,
  `info` varchar(1000) NOT NULL,
  `num` int(11) NOT NULL,
  `ticket` int(11) NOT NULL,
  `pub_date` datetime NOT NULL,
  `status` int(11) NOT NULL,
  `vid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_form_openid_6300da3c` (`openid`),
  KEY `vote_form_vid_id_38eb49aa_fk_vote_vote_id` (`vid_id`),
  CONSTRAINT `vote_form_vid_id_38eb49aa_fk_vote_vote_id` FOREIGN KEY (`vid_id`) REFERENCES `vote_vote` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_form` WRITE;
/*!40000 ALTER TABLE `vote_form` DISABLE KEYS */;

INSERT INTO `vote_form` (`id`, `mid`, `openid`, `username`, `tel`, `image0`, `image1`, `image2`, `image3`, `image4`, `info`, `num`, `ticket`, `pub_date`, `status`, `vid_id`)
VALUES
	(78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','测','','images/2018/02/01/WechatIMG77_7d4d1996cd.jpeg','','','','','',1,20,'2018-02-01 09:55:37',0,1);

/*!40000 ALTER TABLE `vote_form` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_gift
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_gift`;

CREATE TABLE `vote_gift` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `title` varchar(30) NOT NULL,
  `ticket` int(11) NOT NULL,
  `price` double NOT NULL,
  `picurl` varchar(500) NOT NULL,
  `attr` int(11) NOT NULL,
  `sort` int(11) NOT NULL,
  `vid_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_gift_vid_id_3121bc9a_fk_vote_vote_id` (`vid_id`),
  CONSTRAINT `vote_gift_vid_id_3121bc9a_fk_vote_vote_id` FOREIGN KEY (`vid_id`) REFERENCES `vote_vote` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_gift` WRITE;
/*!40000 ALTER TABLE `vote_gift` DISABLE KEYS */;

INSERT INTO `vote_gift` (`id`, `mid`, `title`, `ticket`, `price`, `picurl`, `attr`, `sort`, `vid_id`)
VALUES
	(1,1,'5钻',10,0.02,'',0,2,1),
	(2,1,'1钻',5,0.01,'',0,1,1),
	(3,1,'10钻',20,0.05,'',0,3,1),
	(4,1,'自定义',10,0.01,'',1,4,1);

/*!40000 ALTER TABLE `vote_gift` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_ordering
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_ordering`;

CREATE TABLE `vote_ordering` (
  `mid` int(11) NOT NULL,
  `id` varchar(16) NOT NULL,
  `vid` int(11) NOT NULL,
  `fid` int(11) NOT NULL,
  `openid` varchar(100) NOT NULL,
  `gift_id` int(11) NOT NULL,
  `num` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `pub_date` datetime NOT NULL,
  `total_fee` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_ordering_openid_c0e04171` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_ordering` WRITE;
/*!40000 ALTER TABLE `vote_ordering` DISABLE KEYS */;

INSERT INTO `vote_ordering` (`mid`, `id`, `vid`, `fid`, `openid`, `gift_id`, `num`, `status`, `pub_date`, `total_fee`)
VALUES
	(1,'0010387116246229',1,78,'oDP855AW1oeJXbDNvcGxddn8D9EA',2,1,0,'2018-02-02 16:34:27',0.01),
	(1,'0233245473076316',1,78,'oDP855FOgTJYNO3gcSJzWFNkKZjA',2,1,0,'2018-02-07 10:31:45',0.01),
	(1,'0300392648747492',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-02-08 09:28:34',0.01),
	(1,'0328900844173987',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-25 22:44:30',0.01),
	(1,'0519888319704893',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-02-07 22:17:24',0.01),
	(1,'0606293515681707',1,78,'undefined',2,1,0,'2018-02-08 11:20:40',0.01),
	(1,'0658688346229474',1,78,'oDP855FOgTJYNO3gcSJzWFNkKZjA',2,1,0,'2018-02-07 10:31:41',0.01),
	(1,'0984343036580906',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 15:55:02',0.01),
	(1,'1340754336026945',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 17:04:27',0.01),
	(1,'1382097088104825',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 15:49:52',0.01),
	(1,'1738157758495141',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 17:05:22',0.01),
	(1,'2703193179136568',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 23:16:55',0.01),
	(1,'3008520787390520',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',4,1000,0,'2018-02-08 09:28:44',10),
	(1,'3123296453254957',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,1,'2018-02-08 11:24:06',0.01),
	(1,'3220196427318013',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-02-07 22:17:27',0.01),
	(1,'3698819013038288',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 15:55:06',0.01),
	(1,'3780222884524936',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-02-02 16:52:44',0.01),
	(1,'4086614454279488',1,78,'undefined',2,1,0,'2018-02-08 11:21:35',0.01),
	(1,'4240754189664817',1,78,'oDP855AW1oeJXbDNvcGxddn8D9EA',2,1,0,'2018-02-02 16:34:29',0.01),
	(1,'4958572100140870',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 15:51:51',0.01),
	(1,'5074756793278095',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 17:02:09',0.01),
	(1,'5286783115508634',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-02-07 20:06:28',0.01),
	(1,'5487325577723086',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 12:23:49',0.01),
	(1,'6299271094926825',1,73,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 15:50:22',0.01),
	(1,'6305539533954689',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,1,'2018-01-26 17:12:40',0.01),
	(1,'6347304031105882',1,78,'oDP855FOgTJYNO3gcSJzWFNkKZjA',2,1,0,'2018-02-07 10:31:48',0.01),
	(1,'6533369938123552',1,71,'oDP855KbsqL4v5casezHScQ4RUHg',1,1,0,'2018-01-26 22:30:42',0.02),
	(1,'7043747532333184',1,78,'undefined',2,1,0,'2018-02-08 11:21:57',0.01),
	(1,'7238870436234367',1,73,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 17:07:43',0.01),
	(1,'7297640373900333',1,74,'oDP855GmRWrmuy--KbyMCcc3i_dI',2,1,0,'2018-01-26 17:14:17',0.01),
	(1,'8387531659209262',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 17:08:37',0.01),
	(1,'8399716663857136',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 12:25:54',0.01),
	(1,'8413500249788554',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',1,1,0,'2018-02-01 09:56:21',0.02),
	(1,'8971447433736684',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,1,'2018-02-08 11:27:02',0.01),
	(1,'9066050910228617',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-02-08 11:23:37',0.01),
	(1,'9475946188368465',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 17:06:05',0.01),
	(1,'9591030087673951',1,74,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 16:56:33',0.01),
	(1,'9712182388038723',1,72,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-01-26 17:10:47',0.01),
	(1,'9928983632971745',1,78,'oDP855KATNsjYw25W8F5Rhqqqb6s',2,1,0,'2018-02-08 00:19:07',0.01);

/*!40000 ALTER TABLE `vote_ordering` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_pay
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_pay`;

CREATE TABLE `vote_pay` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `payment` varchar(20) NOT NULL,
  `transaction_id` varchar(60) NOT NULL,
  `pay_time` varchar(60) NOT NULL,
  `openid` varchar(60) NOT NULL,
  `status` int(11) NOT NULL,
  `total_fee` double NOT NULL,
  `summary` varchar(100) NOT NULL,
  `pub_date` datetime NOT NULL,
  `orderid_id` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_pay_orderid_id_36a41285_fk_vote_ordering_id` (`orderid_id`),
  CONSTRAINT `vote_pay_orderid_id_36a41285_fk_vote_ordering_id` FOREIGN KEY (`orderid_id`) REFERENCES `vote_ordering` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_pay` WRITE;
/*!40000 ALTER TABLE `vote_pay` DISABLE KEYS */;

INSERT INTO `vote_pay` (`id`, `mid`, `payment`, `transaction_id`, `pay_time`, `openid`, `status`, `total_fee`, `summary`, `pub_date`, `orderid_id`)
VALUES
	(1,1,'weixin','4200000052201801261246579368','20180126171247','oDP855KATNsjYw25W8F5Rhqqqb6s',1,0.01,'投票','2018-01-26 17:12:48','6305539533954689'),
	(2,1,'weixin','4200000066201802089294869637','20180208112426','oDP855KATNsjYw25W8F5Rhqqqb6s',1,0.01,'投票','2018-02-08 11:24:26','3123296453254957'),
	(3,1,'weixin','4200000060201802089223401717','20180208112707','oDP855KATNsjYw25W8F5Rhqqqb6s',1,0.01,'投票','2018-02-08 11:27:07','8971447433736684');

/*!40000 ALTER TABLE `vote_pay` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_record
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_record`;

CREATE TABLE `vote_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `fid` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  `openid` varchar(60) NOT NULL,
  `IP` varchar(15) NOT NULL,
  `summary` varchar(100) NOT NULL,
  `is_pay` int(11) NOT NULL,
  `pub_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_record_fid_50a48b3c` (`fid`),
  KEY `vote_record_vid_7a4d4536` (`vid`),
  KEY `vote_record_openid_b14cfe77` (`openid`),
  KEY `vote_record_pub_date_26737d7c` (`pub_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_record` WRITE;
/*!40000 ALTER TABLE `vote_record` DISABLE KEYS */;

INSERT INTO `vote_record` (`id`, `mid`, `fid`, `vid`, `openid`, `IP`, `summary`, `is_pay`, `pub_date`)
VALUES
	(1,1,72,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','171.83.91.13','',0,'2018-01-25 22:43:34'),
	(2,1,72,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','171.83.91.13','',0,'2018-01-25 22:43:36'),
	(3,1,72,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','171.83.91.13','',0,'2018-01-25 22:43:37'),
	(4,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','111.175.199.222','',0,'2018-01-26 16:56:28'),
	(5,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','111.175.199.222','',0,'2018-01-26 16:56:29'),
	(6,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','111.175.199.222','',0,'2018-01-26 16:56:29'),
	(7,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-01-26 17:12:48'),
	(8,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-01-26 17:12:48'),
	(9,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-01-26 17:12:48'),
	(10,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-01-26 17:12:48'),
	(11,1,74,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-01-26 17:12:48'),
	(12,1,71,1,'oDP855KbsqL4v5casezHScQ4RUHg','121.35.101.34','',0,'2018-01-26 22:30:27'),
	(13,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','111.175.199.109','',0,'2018-02-02 16:52:36'),
	(14,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','111.175.199.109','',0,'2018-02-02 16:52:38'),
	(15,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','111.175.199.109','',0,'2018-02-02 16:52:39'),
	(16,1,78,1,'oDP855Gy7t7e3L3X2ji9tW7Z8Z2w','113.5.2.92','',0,'2018-02-03 07:46:27'),
	(17,1,78,1,'undefined','119.98.212.245','',0,'2018-02-08 11:20:03'),
	(18,1,78,1,'undefined','119.98.212.245','',0,'2018-02-08 11:20:04'),
	(19,1,78,1,'undefined','119.98.212.245','',0,'2018-02-08 11:20:05'),
	(20,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.75','',1,'2018-02-08 11:24:26'),
	(21,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.75','',1,'2018-02-08 11:24:26'),
	(22,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.75','',1,'2018-02-08 11:24:26'),
	(23,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.75','',1,'2018-02-08 11:24:26'),
	(24,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.75','',1,'2018-02-08 11:24:26'),
	(25,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','119.98.212.245','',0,'2018-02-08 11:26:15'),
	(26,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','119.98.212.245','',0,'2018-02-08 11:26:17'),
	(27,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','119.98.212.245','',0,'2018-02-08 11:26:18'),
	(28,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-02-08 11:27:07'),
	(29,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-02-08 11:27:07'),
	(30,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-02-08 11:27:07'),
	(31,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-02-08 11:27:07'),
	(32,1,78,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','140.207.54.76','',1,'2018-02-08 11:27:07');

/*!40000 ALTER TABLE `vote_record` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_setting
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_setting`;

CREATE TABLE `vote_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `appId` varchar(30) NOT NULL,
  `appSecret` varchar(80) NOT NULL,
  `mch_id` varchar(20) NOT NULL,
  `merchant_key` varchar(80) NOT NULL,
  `notify_url` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_setting` WRITE;
/*!40000 ALTER TABLE `vote_setting` DISABLE KEYS */;

INSERT INTO `vote_setting` (`id`, `mid`, `appId`, `appSecret`, `mch_id`, `merchant_key`, `notify_url`)
VALUES
	(1,1,'wx13e6c03005b32716','0f6e23d6e20d35794ad80a2ffd81fd47','1487756232','ibpdlEHnPs8eJFhlRqWDs6wPIJFGdhsB','https://jiahe.zz.lanrenmb.com/vote/wxpay_notify/');

/*!40000 ALTER TABLE `vote_setting` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_template
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_template`;

CREATE TABLE `vote_template` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `folder` varchar(30) NOT NULL,
  `picurl` varchar(500) NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_template` WRITE;
/*!40000 ALTER TABLE `vote_template` DISABLE KEYS */;

INSERT INTO `vote_template` (`id`, `title`, `folder`, `picurl`, `status`)
VALUES
	(1,'默认模板','index','images/2018/01/25/WechatIMG77_537df6e9fa.jpeg',1);

/*!40000 ALTER TABLE `vote_template` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_userinfo
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_userinfo`;

CREATE TABLE `vote_userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `openid` varchar(200) NOT NULL,
  `avatarUrl` varchar(500) NOT NULL,
  `city` varchar(20) NOT NULL,
  `country` varchar(20) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `language` varchar(20) NOT NULL,
  `nickName` varchar(20) NOT NULL,
  `province` varchar(20) NOT NULL,
  `pub_date` datetime NOT NULL,
  `login_count` int(11) NOT NULL,
  `login_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_userinfo_mid_a256c085` (`mid`),
  KEY `vote_userinfo_openid_916d5626` (`openid`),
  KEY `vote_userinfo_avatarUrl_d1a374d1` (`avatarUrl`(255))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_userinfo` WRITE;
/*!40000 ALTER TABLE `vote_userinfo` DISABLE KEYS */;

INSERT INTO `vote_userinfo` (`id`, `mid`, `openid`, `avatarUrl`, `city`, `country`, `gender`, `language`, `nickName`, `province`, `pub_date`, `login_count`, `login_date`)
VALUES
	(1,1,'oDP855KATNsjYw25W8F5Rhqqqb6s','https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK89mOkx2ZB3rv9Bj3XiaQy1ubP8KWTep9IWdJTfOsOqoklFoOIgBMOUHAicyfggDicyaUeAoRZs3d7g/0','Wuhan','China','1','zh_CN','A涛哥','Hubei','2018-01-25 22:43:28',8,'2018-02-08 11:22:47'),
	(2,1,'oDP855GmRWrmuy--KbyMCcc3i_dI','https://wx.qlogo.cn/mmopen/vi_32/VXssGw0QDiazGbbL02NAEC5svPYCn7z2X6lG8vSKyCm9jM5kT9BkcTCuKaJFibNXCIkBBwLF7T4eNWKRY8mc4Tcg/0','Wuhan','China','1','zh_CN','仁裕元科技-小胡','Hubei','2018-01-26 17:14:12',1,'2018-01-26 17:14:12'),
	(4,1,'oDP855FOgTJYNO3gcSJzWFNkKZjA','https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83erEo2fvMQywXzPwX1lMDXw8nGicyh47IxVOYPhicls4jgcmZeOe95jpibrXJ4yH3t5bcXmrnKV3kvQsA/0','Ganzhou','China','1','zh_CN','李翔','Jiangxi','2018-01-27 10:50:13',2,'2018-02-04 17:58:06'),
	(6,1,'oDP855MOTHz26yBkKBZnZ9DVO9hA','','','','0','zh_CN','rdgztest_SOCYHR','','2018-02-01 06:24:51',1,'2018-02-01 06:24:51'),
	(7,1,'oDP855AW1oeJXbDNvcGxddn8D9EA','https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83erj09tKwZUH0yzLybVZLufBqEjmLvcvnvZPBmu3zu7w803YerZeESgtG6SFiaKRRNib8LakQdoPKeCQ/0','Ganzhou','China','1','zh_CN','小程序开发·网站建设·企业彩铃','Jiangxi','2018-02-02 16:08:32',1,'2018-02-02 16:08:32'),
	(8,1,'oDP855DTH5e0bgb21AiO25Tv-aCQ','https://wx.qlogo.cn/mmopen/vi_32/cRZxOm30JoGDHXBuiboaOVZ2qr9uyPanSwOawF0mgp8qR7VqV2Uco1VPM9CweF3icsB1IVcfJ5KcMpXVdVr8wLQA/0','','Maldives','1','zh_CN','人生几何','North Nilandhe Atoll','2018-02-02 16:13:17',1,'2018-02-02 16:13:17'),
	(9,1,'oDP855Gy7t7e3L3X2ji9tW7Z8Z2w','https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIUDSvWdgGticaia53H7YfnZ8VwBtkt7DNzEnbic5vAB4mkbgaMBgaR0V2LCGYnJxibFiay027iaWAQoZPQ/0','Yichun','China','1','zh_CN','那…天','Heilongjiang','2018-02-02 17:01:01',1,'2018-02-02 17:01:01'),
	(10,1,'oDP855OGBFAIdofoNVR1VM8EOqZU','https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJibXTeGe1CDCgU3VZs8GGMCdomEDOqJdajcPLZo27IQNEVTzicKiaIIX05R91rTjXGHmPf7McBO13dQ/0','Shenzhen','China','1','zh_CN','Mr_Liang','Guangdong','2018-02-03 23:23:11',1,'2018-02-03 23:23:11'),
	(11,1,'undefined','https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK89mOkx2ZB3rv9Bj3XiaQy1ubP8KWTep9IWdJTfOsOqoklFoOIgBMOUHAicyfggDicyaUeAoRZs3d7g/0','Wuhan','China','1','zh_CN','A涛哥','Hubei','2018-02-07 23:48:31',6,'2018-02-08 11:03:22');

/*!40000 ALTER TABLE `vote_userinfo` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table vote_vote
# ------------------------------------------------------------

DROP TABLE IF EXISTS `vote_vote`;

CREATE TABLE `vote_vote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `title` varchar(30) NOT NULL,
  `message` varchar(100) NOT NULL,
  `image` varchar(200) NOT NULL,
  `view` int(11) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `v_start_date` datetime NOT NULL,
  `v_end_date` datetime NOT NULL,
  `cknums` int(11) NOT NULL,
  `sort_field` varchar(30) NOT NULL,
  `status` int(11) NOT NULL,
  `sign_status` int(11) NOT NULL,
  `sign_repeat` int(11) NOT NULL,
  `sort` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `prize` longtext NOT NULL,
  `pub_date` datetime NOT NULL,
  `template_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vote_vote_template_id_id_9cf7491f_fk_vote_template_id` (`template_id_id`),
  CONSTRAINT `vote_vote_template_id_id_9cf7491f_fk_vote_template_id` FOREIGN KEY (`template_id_id`) REFERENCES `vote_template` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `vote_vote` WRITE;
/*!40000 ALTER TABLE `vote_vote` DISABLE KEYS */;

INSERT INTO `vote_vote` (`id`, `mid`, `title`, `message`, `image`, `view`, `start_date`, `end_date`, `v_start_date`, `v_end_date`, `cknums`, `sort_field`, `status`, `sign_status`, `sign_repeat`, `sort`, `content`, `prize`, `pub_date`, `template_id_id`)
VALUES
	(1,1,'南湾海岛风暴杯投票开始啦','南湾海岛风暴杯投票开始啦','_versions/tmp_1297417425o6zAJs5MfE2_9vkGuEexr_-v8SkId015415309c213e645c0ea5d045e194b_medium.png',80758,'2018-02-01 14:50:00','2019-01-18 14:50:00','2018-01-01 14:50:00','2020-01-12 14:50:00',3,'num',1,1,2,0,'<p><br /> 活动时间：<br /> 2018.02.14&nbsp; 17：00至2018.11.11 &nbsp;19：30；<br /> 本商品礼券的兑换时间：投票成功即可兑换<br /> 活动须知：<br /> 1、兑换地点：幸福&middot;汇邻湾广场三楼服务台（需出示兑换码，方可兑换礼券）<br /> 2、咨询电话：15190743710<br /> 3、礼券使用时间：<br /> 即日起至2016.11.13 &nbsp;20：30<br /> 粉丝可以任意投票。在投票成功后，即可来幸福汇邻湾广场三楼服务台领取兑换券，方可在指定店家享受优惠。<br /> 每人每号仅限参与一次，不可一人多号重复参加；同一好友，每个商品均可帮砍一次。<br /> 中奖用户须马上完成领奖，逾期或领奖时信息填写错误或不完整均视为放弃获奖资格，仅限中奖者本人领奖。<br /> 作弊用户直接取消获奖资格，我们保留追求其责任的权利。<br /> 礼券每天数量有限。<br /> 本活动最终解释权归幸福&middot;汇邻湾广场所有。</p>\r\n<p>&nbsp;</p>','<h1><strong>&nbsp;一等奖：苹果iphone X 一部</strong></h1>\r\n<h1><strong><img src=\"https://jiahe.zz.lanrenmb.com/media/_versions/111_medium.png\" alt=\"\" /></strong></h1>\r\n<h1>&nbsp;</h1>\r\n<h1><strong>二等奖：太阳能空气净化品2台</strong></h1>\r\n<h1><strong>&nbsp;<img src=\"https://jiahe.zz.lanrenmb.com/media/_versions/tmp_1297417425o6zAJs5MfE2_9vkGuEexr_-v8SkI00fd688a6825abd65f0e810b8c63453b_medium.png\" alt=\"\" /></strong></h1>\r\n<h1><strong>三等奖：高端礼盒 10套</strong></h1>\r\n<p><img src=\"https://jiahe.zz.lanrenmb.com/media/_versions/wx20180131-224903%402x_medium.png\" alt=\"\" width=\"300\" height=\"293\" /></p>\r\n<p>&nbsp;</p>\r\n<h1><strong><img src=\"https://jiahe.zz.lanrenmb.com/admin/vote/vote/1/change/_versions/wx20180131-224903%402x_big.png\" alt=\"\" /></strong></h1>','2020-01-12 14:50:35',1);

/*!40000 ALTER TABLE `vote_vote` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
