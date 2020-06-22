#!/usr/bin/env bash
#!/usr/bash
tablename=dwd_youtui_commerce_page_di
hdfs dfs -mv /user/hive/warehouse/logs.db/${tablename} /user/hive/warehouse/logs.db/${tablename}"_tmp"
hive -e "drop table logs.${tablename}"
hive -e "
create table if not exists  logs.dwd_youtui_commerce_page_di(
    time                  string             comment '系统时间'
    ,youtui_type          bigint             comment 'type'
    ,app_id               bigint             comment '媒体id'
    ,slot_id              string             comment '广告位id'
	,activity_id          bigint             comment '活动id'
	,device_id            string             comment 'device_id'
	,device_type          bigint             comment '设备类型'
	,connection_type      string             comment '网络类型'
	,ip               	  string             comment 'ip'
	,version              string             comment '版本号'
	,channel              string             comment '渠道号'
	,os_type              string             comment '操作系统 '
	,os_version           string             comment '操作系统版本'
	,login_id         	  string             comment '启动id/登录id '
	,user_id              bigint             comment '用户id'
	,advert_id            bigint             comment '广告id'
	,share_way            string             comment '分享途径'
	,cash_amount          bigint             comment '提现金额 单位：分'
	,position_id          bigint             comment '  --内容所在位置id'
	,zfb_account          string             comment '--支付宝账号'
	,is_simulator         string             comment '--is_simulator'
	,sub_type             bigint             comment ' --sub_type'
	,source_cid           bigint             comment '--分享者用户id'
	,content_id           bigint             comment '  --客户端-内容id'
	,phone                string             comment '--手机号'
	,content_type         bigint             comment '--内容类型   1 广告区块,2自由配置区块 ,3活动区块 ,4直投页区块 ,5链接区块'
	,page_source          bigint             comment '0-默认 1-banner页 2-首页列表  3-我的分享页 4-新手引导页  5-互动页面 6-专栏页面 7-趣味活动页面 8-奖励中心页 9-更多 10-H5预览'
	,loading_time	      bigint			 comment '加载时长,毫秒'
	,is_H5				  bigint			 comment '0:否    1:是'
	,page_type				bigint			comment	'不同事件含义不同,详情见cf'
	,tag_type			bigint				comment	'不同事件含义不同,详情见cf'
) comment '友推事件日志'
partitioned by (dt string)
stored as orc;
"
hdfs dfs -mv /user/hive/warehouse/logs.db/${tablename} /user/hive/warehouse/logs.db/${tablename}:"hdh"
hdfs dfs -mv /user/hive/warehouse/logs.db/${tablename}"_tmp" /user/hive/warehouse/logs.db/${tablename}
hive -e "msck REPAIR TABLE logs.${tablename}"
hive -e "alter table logs.${tablename} drop partition(dt='${date}')"


