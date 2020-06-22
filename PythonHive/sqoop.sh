#!/usr/bin/env bash
sqoop import --connect ${secret.rds.huaya.jdbc} \
--query "select * from Mall_Delivery where \$CONDITIONS" \
--split-by Delivery_Id \
--hive-table ods_credits.Mall_Delivery \
--target-dir /user/hive/warehouse/temp_query_result.db/sqoop_Mall_Delivery \
--hive-partition-key dt \
--hive-partition-value ${date} \
--hive-import \
--driver com.microsoft.sqlserver.jdbc.SQLServerDriver \
--boundary-query "SELECT MIN(Delivery_Id), MAX(Delivery_Id) FROM Mall_Delivery" \
--hive-drop-import-delims \
--hive-overwrite


sqoop export  \
--connect ${secret.advert_statistics.jdbc} \
--username ${secret.advert_statistics.account} \
--password ${secret.advert_statistics.password} \
--table tb_ttnews_article_sum \
--columns "account_id,agent_id,cur_date,article_sum" \
--export-dir /user/hive/warehouse/news.db/dwb_news_article_sum/dt=${endate1} \
--input-fields-terminated-by "\001" \
--input-null-string '\\N' \
--input-null-non-string '\\N' \
--update-key cur_date,account_id \
--update-mode allowinsert -- \
--default-character-set=utf-8

