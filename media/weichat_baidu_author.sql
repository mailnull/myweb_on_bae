/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50710
Source Host           : localhost:3306
Source Database       : myweb_on_bae

Target Server Type    : MYSQL
Target Server Version : 50710
File Encoding         : 65001

Date: 2016-04-26 20:44:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for weichat_baidu_author
-- ----------------------------
DROP TABLE IF EXISTS `weichat_baidu_author`;
CREATE TABLE `weichat_baidu_author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(16) NOT NULL,
  `App_ID` int(10) unsigned NOT NULL,
  `API_Key` varchar(30) NOT NULL,
  `Secret_Key` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `App_ID` (`App_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of weichat_baidu_author
-- ----------------------------
INSERT INTO `weichat_baidu_author` VALUES ('1', '18013792913', '7954404', 'moCAj9lb2Vyc1AS1XRmcYlgx', 'd4076ac92eb4a1ac624c9240a86ec98b');
