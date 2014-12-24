--
-- 表的结构 `info_filesystem`
--

drop table `apprec_conf`;
CREATE TABLE `apprec_conf` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `conf_sernum` varchar(32) NOT NULL COMMENT 'conference serial number',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT 'attendance of a conference',
  PRIMARY KEY (`id`),
  KEY `search` (`real_time`,`type`,`conf_sernum`,`num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Real time information of a conference';

drop table `apprec_conf_amount`;
CREATE TABLE `apprec_conf_amount` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT 'Amount of all conference which is in progress',
  PRIMARY KEY (`id`),
  KEY `search` (`real_time`,`type`,`num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Amount of Conference which is in progress';

# Sip的注册用户统计
drop table `apprec_sip_register_num`;
CREATE TABLE `apprec_sip_register_num` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `register_type_id` int(11) NOT NULL DEFAULT '0' COMMENT 'register_type_id: 0(total)',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT 'Amount of sip register',
  PRIMARY KEY (`id`),
  KEY `search` (`real_time`,`type`,`register_type_id`,`num`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='Amount of Sip Register User';

# Web界面的用户统计
drop table `apprec_web_user_num`;
CREATE TABLE `apprec_web_user_num` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'PRIMARY KEY',
  `real_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` int(11) NOT NULL DEFAULT '0' COMMENT 'Collect Type: 0 (normal:real value),2 (day:Average of 24Hours),3 (week:Average of 7days),4 (month:Average of 30Days)',
  `register_user` int(11) NOT NULL DEFAULT '0' COMMENT 'amount of register user',
  `guest_user` int(11) NOT NULL DEFAULT '0' COMMENT 'amount of guest user',
  PRIMARY KEY (`id`),
  KEY `search` (`real_time`,`type`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='Amount of web User';

