/*
Navicat MySQL Data Transfer

Source Server         : 192.168.126.8
Source Server Version : 50621
Source Host           : 192.168.126.8:3306
Source Database       : monitor

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2015-01-06 16:37:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for apprec_conf
-- ----------------------------
DROP TABLE IF EXISTS `apprec_conf`;
CREATE TABLE `apprec_conf` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `conf_sernum` varchar(32) NOT NULL COMMENT 'conference serial number',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT 'attendance of a conference',
  PRIMARY KEY (`id`),
  UNIQUE KEY `search` (`real_time`,`type`,`conf_sernum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Real time information of a conference';

-- ----------------------------
-- Table structure for apprec_conf_daily_num
-- ----------------------------
DROP TABLE IF EXISTS `apprec_conf_daily_num`;
CREATE TABLE `apprec_conf_daily_num` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '2' COMMENT 'Collect Type: 2 (day:Total of one day)',
  `conf_num` int(11) NOT NULL DEFAULT '0' COMMENT 'Total number of daliy conference',
  `conf_effective_num` int(11) NOT NULL DEFAULT '0' COMMENT 'Total number of daliy effective conference which means duration is more than 10mins',
  PRIMARY KEY (`id`),
  UNIQUE KEY `search` (`real_time`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='num of daliy conference';

-- ----------------------------
-- Table structure for apprec_conf_num
-- ----------------------------
DROP TABLE IF EXISTS `apprec_conf_num`;
CREATE TABLE `apprec_conf_num` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `conf_sernum` varchar(32) NOT NULL COMMENT 'conference serial number',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT 'attendance of a conference',
  PRIMARY KEY (`id`),
  UNIQUE KEY `search` (`real_time`,`type`,`conf_sernum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Real time information of a conference';

-- ----------------------------
-- Table structure for apprec_conf_sip_num
-- ----------------------------
DROP TABLE IF EXISTS `apprec_conf_sip_num`;
CREATE TABLE `apprec_conf_sip_num` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT 'Amount of all conference which is in progress',
  PRIMARY KEY (`id`),
  UNIQUE KEY `search` (`real_time`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Amount of Conference which is in progress';

-- ----------------------------
-- Table structure for apprec_file_daily_num
-- ----------------------------
DROP TABLE IF EXISTS `apprec_file_daily_num`;
CREATE TABLE `apprec_file_daily_num` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '2' COMMENT 'Collect Type: 2 (day:Total of one day)',
  `file_conf_num` int(11) NOT NULL DEFAULT '0' COMMENT 'Total number of daliy created files',
  `file_video_num` int(11) NOT NULL DEFAULT '0' COMMENT 'Total number of daliy created video files',
  PRIMARY KEY (`id`),
  KEY `search` (`real_time`,`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='num of daliy conference';

-- ----------------------------
-- Table structure for apprec_user
-- ----------------------------
DROP TABLE IF EXISTS `apprec_user`;
CREATE TABLE `apprec_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `app_group_id` int(11) NOT NULL DEFAULT '0',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `register_user` int(11) NOT NULL DEFAULT '0' COMMENT 'amount of register user',
  `guest_user` int(11) NOT NULL DEFAULT '0' COMMENT 'amount of guest user',
  `sip_online_user` int(11) NOT NULL DEFAULT '0' COMMENT 'amount of sip server user',
  `web_online_user` int(11) NOT NULL DEFAULT '0' COMMENT 'amount of web server user(Redis Web Token)',
  `pc_online_user` int(11) NOT NULL DEFAULT '0' COMMENT 'amount of pc client user(Redis PC Token)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `search` (`real_time`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='Amount of web User';

-- ----------------------------
-- Table structure for apprec_user_statistics
-- ----------------------------
DROP TABLE IF EXISTS `apprec_user_statistics`;
CREATE TABLE `apprec_user_statistics` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `app_group_id` int(11) NOT NULL DEFAULT '0',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(2) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 2 (day:Last 24Hours),3 (week:Last 7days),4 (month:Last of 30Days)',
  `'max_sip` int(11) NOT NULL DEFAULT '0',
  `'min_sip` int(11) NOT NULL DEFAULT '0',
  `'max_web` int(11) NOT NULL DEFAULT '0',
  `'min_web` int(11) NOT NULL DEFAULT '0',
  `'max_pc` int(11) NOT NULL DEFAULT '0',
  `'min_pc` int(11) NOT NULL DEFAULT '0' COMMENT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `search` (`real_time`,`type`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='Amount of web User';

-- ----------------------------
-- Table structure for info_host
-- ----------------------------
DROP TABLE IF EXISTS `info_host`;
CREATE TABLE `info_host` (
  `host_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `host_ip` varchar(16) NOT NULL,
  `region` varchar(255) DEFAULT NULL COMMENT '所在区域',
  `host_name` varchar(80) DEFAULT NULL COMMENT '主机名',
  `racuser` varchar(10) DEFAULT 'root' COMMENT 'Remote Access Control User',
  `racpasswd` varchar(256) DEFAULT '123456' COMMENT 'racå¸å·å¯†ç ',
  `racip` varchar(15) DEFAULT NULL,
  `racport` int(11) DEFAULT '0',
  `os_type` varchar(128) DEFAULT NULL COMMENT 'linux|aix|hp-ux',
  `kernel` varchar(128) DEFAULT NULL COMMENT 'é€šè¿‡ã€uname -rã€‘èŽ·å–',
  `distribute_id` varchar(128) DEFAULT NULL COMMENT 'è®°å½•æ“ä½œç³»ç»Ÿçš„å‘è¡Œç‰ˆæœ¬',
  `physical_mem` mediumint(11) DEFAULT NULL COMMENT 'å•ä½mb',
  `swap_size` mediumint(11) DEFAULT NULL COMMENT 'å•ä½mb',
  `cpu_model_name` varchar(128) DEFAULT NULL COMMENT 'cpuåŽ‚å•†ä¿¡æ¯',
  `cpu_ghz` decimal(20,2) DEFAULT '0.00' COMMENT 'ä¸»é¢‘',
  `cpu_num` smallint(6) DEFAULT NULL COMMENT 'cpuæ•°é‡ã€é€»è¾‘ã€‘',
  `status` varchar(8) NOT NULL DEFAULT 'online' COMMENT 'offline|online',
  `last_hours` bigint(8) DEFAULT '0' COMMENT 'åœ¨çº¿æ—¶é•¿,å•ä½ç§’',
  `offline_time` timestamp NULL DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `online_time` timestamp NULL DEFAULT NULL,
  `ssh_port` int(10) DEFAULT NULL COMMENT 'sshå»ºç«‹çš„ç«¯å£ï¼Œé»˜è®¤ä¸º22',
  `gmt_create` timestamp NULL DEFAULT NULL,
  `gmt_update` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'æ›´æ–°æ—¶é—´',
  PRIMARY KEY (`host_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
