ALTER TABLE topic_content MODIFY COLUMN content text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL; 

ALTER TABLE topic MODIFY COLUMN title varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL; 

ALTER TABLE topic_reply MODIFY COLUMN content text CHARACTER set utf8 COLLATE utf8_unicode_ci DEFAULT NULL;


另外需要注意的是，当数据库用了 utf8mb4 后，如果用 mysqldump 备份，那么需要在备份时加上 --default-character-set=utf8mb4 参数。
在恢复备份前，需要确保已经输入了 SET CHARSET utf8mb4 这条指令。

ALTER TABLE node ADD COLUMN platform text CHARACTER set utf8 COLLATE utf8_unicode_ci DEFAULT NULL;

