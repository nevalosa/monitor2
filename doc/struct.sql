--
-- 表的结构 `info_filesystem`
--

DROP TABLE IF EXISTS `info_filesystem`;
CREATE TABLE IF NOT EXISTS `info_filesystem` (
  `filesystem_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `host_id` int(11) NOT NULL,
  `filesystem_name` varchar(128) DEFAULT NULL COMMENT '文件系统名称',
  `mounted_on` varchar(128) DEFAULT NULL COMMENT '挂载路径',
  `total_size` decimal(20,2) DEFAULT NULL COMMENT '目录大小(MB)',
  `used_size` decimal(20,2) DEFAULT NULL COMMENT '已用大小(MB)',
  `space_used_percent` decimal(5,2) DEFAULT NULL COMMENT 'space已用百分比 示例：78.99',
  `gmt_create` datetime NOT NULL COMMENT '插入时间',
  `gmt_update` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`filesystem_id`),
  KEY `host_id` (`host_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='文件系统磁盘巡检统计表' AUTO_INCREMENT=2 ;