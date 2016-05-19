/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50710
Source Host           : localhost:3306
Source Database       : myweb_on_bae

Target Server Type    : MYSQL
Target Server Version : 50710
File Encoding         : 65001

Date: 2016-04-07 14:48:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for weichat_author
-- ----------------------------
DROP TABLE IF EXISTS `weichat_author`;
CREATE TABLE `weichat_author` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(20) NOT NULL,
  `nickname` varchar(16) DEFAULT NULL,
  `author_type` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `weichat_author_author_4582876d_uniq` (`author`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of weichat_author
-- ----------------------------
INSERT INTO `weichat_author` VALUES ('4', 'gh_faabb9a450dd', '新注册公众号', '1');
INSERT INTO `weichat_author` VALUES ('5', 'gh_b46e07012e44', 'hbcw测试号', '4');
INSERT INTO `weichat_author` VALUES ('6', 'gh_d0ea0e87caf8', 'hbcwcontrol', '0');
