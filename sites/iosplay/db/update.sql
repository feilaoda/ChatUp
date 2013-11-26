ALTER TABLE `people` DROP INDEX `email`;

ALTER TABLE  `note` ADD  `content_id` INT NULL AFTER  `people_id`;
ALTER TABLE  `pin` ADD  `category` VARCHAR( 100 ) NOT NULL AFTER  `board_id`;
ALTER TABLE  `board` ADD  `people_id` INT NOT NULL ;
ALTER TABLE  `board` ADD  `pins_count` INT NOT NULL AFTER  `people_id`;



ALTER TABLE  `pin` CHANGE  `thumbnail`  `thumb_middle` VARCHAR( 1000 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE  `pin` ADD  `thumb_small` VARCHAR( 1000 ) NOT NULL AFTER  `sort_by`;
ALTER TABLE  `board` CHANGE  `count`  `pins_count` INT( 11 ) NOT NULL;

ALTER TABLE  `read_folder` CHANGE  `sort_by`  `sorting` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE  `board` ADD  `sorting` INT NOT NULL DEFAULT  '0'  , ADD INDEX (  `sorting` );

ALTER TABLE  `movie_site_link` CHANGE  `site_id`  `site_url` VARCHAR( 200 ) NULL DEFAULT NULL;

ALTER TABLE  `movie` CHANGE  `runtime`  `duration` VARCHAR( 50 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE  `movie` ADD  `image_id` INT NOT NULL AFTER  `description`;
ALTER TABLE  `movie` DROP  `thumb_image` , DROP  `front_image` ;
ALTER TABLE  `movie` ADD  `official_site` VARCHAR( 200 ) NULL AFTER  `company`;
ALTER TABLE  `movie` ADD  `updated` DATETIME NOT NULL;

 
-- 2013-04-17 --

ALTER TABLE  `pin` CHANGE  `sort_by`  `sorting` INT( 11 ) NULL DEFAULT NULL;

 

-- 2013-04-20 --
ALTER TABLE  `movie` ADD  `extra_title` VARCHAR( 200 ) NULL AFTER  `title`;
ALTER TABLE  `movie` ADD  `douban_id` INT NULL AFTER  `publish_time` ,
ADD INDEX (  `douban_id` );
 
-- 2013-04-27 --
RENAME TABLE  `keepcd`.`movie_site_link` TO  `keepcd`.`movie_site` ;

-- 2013-05-09 --
ALTER TABLE  `movie` ADD  `resources` INT NOT NULL DEFAULT  '0' AFTER  `publish_time`;
ALTER TABLE  `movie_watch_list` ADD INDEX (`watch`);


-- 2013-05-11 --
ALTER TABLE  `people` CHANGE  `email`  `email` VARCHAR( 200 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL;

ALTER TABLE  `movie_media_link` ADD  `people_id` INT NULL DEFAULT NULL AFTER  `id` ,ADD INDEX (  `people_id` );


RENAME TABLE  `keepcd`.`people_added_link` TO  `keepcd`.`movie_people_added_link` ;
ALTER TABLE  `entity` CHANGE  `label`  `title` VARCHAR( 200 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;

ALTER TABLE  `people_added_link` ADD  `category` VARCHAR( 30 ) NULL AFTER  `people_id` ,
ADD INDEX (  `category` );

ALTER TABLE  `people_added_link` ADD  `definity` VARCHAR( 30 ) NULL AFTER  `category` ,
ADD INDEX (  `definity` );

ALTER TABLE  `media_link` ADD  `hash_value` VARCHAR( 64 ) NULL AFTER  `website`;


ALTER TABLE  `entity` ADD  `salt` VARCHAR( 32 ) NULL DEFAULT NULL AFTER  `statements` ,
ADD INDEX (  `salt` );

ALTER TABLE  `media_link` ADD  `featured` INT NOT NULL DEFAULT  '0' AFTER  `entity_id` ,
ADD INDEX (  `featured` );





ALTER TABLE  `media_link` CHANGE  `definity`  `definition` VARCHAR( 10 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;
ALTER TABLE  `people_added_link` CHANGE  `definity`  `definition` VARCHAR( 30 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;

ALTER TABLE  `movie_image` CHANGE  `cdn_weibo`  `cdn_small` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL

ALTER TABLE movie_image disable KEYS;
ALTER TABLE  `movie_image` ADD  `cdn_small` VARCHAR( 255 ) NULL;
ALTER TABLE  `movie_image` ADD  `cdn_large` VARCHAR( 255 ) NULL;
ALTER TABLE movie_image enable KEYS;


INSERT INTO movie_image_new (id, small, thumb, large, version) (SELECT id, small, thumb, large, version FROM movie_image);
RENAME TABLE movie_image TO movie_image_old, movie_image_new TO movie_image;


ALTER TABLE  `tag` ADD  `type` VARCHAR( 30 ) NULL AFTER  `value`, ADD INDEX (  `type` );
ALTER TABLE  `weibo` CHANGE  `uid`  `uid` VARCHAR( 30 ) NOT NULL;


RENAME TABLE  `bt`.`crawl_douban_movie` TO  `bt`.`crawl_douban_url` ;


ALTER TABLE  `search_movie` ADD  `resource_count` INT NOT NULL DEFAULT  '0',
ADD INDEX (  `resource_count` )


ALTER TABLE  `lang_resource` ADD  `slow_media` VARCHAR( 255 ) NULL AFTER  `media`;
ALTER TABLE  `lang_resource` ENGINE = InnoDB;

ALTER TABLE  `lang_channel_subscribe` ADD  `sorting` INT NULL DEFAULT  '0' AFTER  `channel_id`;


ALTER TABLE `people` ADD `nickname` VARCHAR( 100 ) NULL AFTER `username` ;


ALTER TABLE `crawl_douban_movie` ADD `category` VARCHAR( 100 ) NULL AFTER `url` ;
ALTER TABLE `crawl_imax_im` ADD `category` VARCHAR( 100 ) NULL AFTER `url` ;
ALTER TABLE `crawl_esl_pod` ADD `category` VARCHAR( 100 ) NULL AFTER `url` ;
ALTER TABLE `crawl_voa_news` ADD `category` VARCHAR( 100 ) NULL AFTER `url` ;

ALTER TABLE `lang_resource` ADD `category` VARCHAR( 100 ) NULL AFTER `title` ;
ALTER TABLE `movie_media_link` ADD `salt` VARCHAR( 64 ) NULL AFTER `movie_id` ;


ALTER TABLE  `lang_resource` ADD  `sorting` INT NOT NULL DEFAULT  '0' AFTER  `dl_count` ,
ADD INDEX (  `sorting` );
ALTER TABLE  `lang_cloze` ADD  `title` VARCHAR( 255 ) NULL AFTER  `resource_id`;

ALTER TABLE  `people` ADD  `follow_count` INT NOT NULL DEFAULT  '0' AFTER  `description`;
ALTER TABLE  `people` ADD  `followed_count` INT NOT NULL DEFAULT  '0' ;

ALTER TABLE  `topic` CHANGE  `title`  `title` VARCHAR( 500 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL;


ALTER TABLE  `lang_resource` ADD  `reply_count` INT NOT NULL DEFAULT  '0' AFTER  `resource_url`;
ALTER TABLE  `lang_resource` ADD  `repeat_count` INT NOT NULL DEFAULT  '0' AFTER  `reply_count`;


ALTER TABLE  `topic` ADD  `hidden` INT NULL DEFAULT  '0' AFTER  `impact`

ALTER TABLE  `people` ADD  `pregnancy_type` INT NULL DEFAULT  '0' AFTER  `followed_count`;
ALTER TABLE  `topic_reply` ADD  `status` VARCHAR( 50 ) NULL AFTER  `ups`;


ALTER TABLE  `topic_reply` ADD  `order` INT NULL DEFAULT  '0' AFTER  `content`;

ALTER TABLE  `topic` CHANGE  `hidden`  `hidden` VARCHAR( 10 ) NULL DEFAULT NULL;
ALTER TABLE  `topic_reply` ADD  `hidden` VARCHAR( 1 ) NULL AFTER  `content`;

ALTER TABLE  `people` CHANGE  `edit_username_count`  `status` INT( 11 ) NULL DEFAULT NULL;



ALTER TABLE  `food_note` ADD  `analysed` INT NOT NULL DEFAULT  '0' AFTER  `content_id` ,
ADD INDEX (  `analysed` );


RENAME TABLE  `food` TO   `food_old` ;
RENAME TABLE  `food_ingredient` TO   `food` ;
RENAME TABLE  `food_nutrient` TO   `food_nutrient_cat` ;
RENAME TABLE  `food_ingredient_nutrient` TO   `food_nutrient` ;

INSERT INTO `food_pregnancy`(name) select distinct name from food;

UPDATE `food_pregnancy` a left join food b on a.name = b.name SET  a.food_id=b.id;

ALTER TABLE  `food_unit_item` CHANGE  `ingredient_id`  `food_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE  `food_nutrient` CHANGE  `ingredient_id`  `food_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE  `food_pregnancy` ADD  `sorting` INT NOT NULL DEFAULT  '0' AFTER  `permission`;
ALTER TABLE  `food_pregnancy` ADD  `tips` TEXT NULL AFTER  `sorting`;

ALTER TABLE  `food_pregnancy` ADD  `category` VARCHAR( 50 ) NULL AFTER  `permission` ,
ADD INDEX (  `category` );


UPDATE food_pregnancy a left join food  b on  a.food_id = b.id set a.category = b.category;

ALTER TABLE  `people_setting` ADD  `pregnancy_babycount` INT NULL DEFAULT  '0' AFTER  `stat_date`;




