/*
Navicat MySQL Data Transfer

Source Server         : DEV
Source Server Version : 50711
Source Host           : 127.0.0.1:3306
Source Database       : quey

Target Server Type    : MYSQL
Target Server Version : 50711
File Encoding         : 65001

Date: 2016-06-01 09:09:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admins
-- ----------------------------
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eno` varchar(128) DEFAULT NULL,
  `reg_time` datetime DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `eno` (`eno`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admins
-- ----------------------------
INSERT INTO `admins` VALUES ('1', '20122212880', '2016-05-10 03:06:49', 'pbkdf2:sha1:1000$fJNVEl1K$cc2969cbb29e2cc18a433692fa55a217fb1b2fef');

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('e785358a9443');

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of categories
-- ----------------------------
INSERT INTO `categories` VALUES ('2', '会议');
INSERT INTO `categories` VALUES ('7', '公益');
INSERT INTO `categories` VALUES ('12', '其它');
INSERT INTO `categories` VALUES ('4', '展览');
INSERT INTO `categories` VALUES ('3', '演出');
INSERT INTO `categories` VALUES ('6', '社团');
INSERT INTO `categories` VALUES ('1', '讲座');
INSERT INTO `categories` VALUES ('5', '运动');

-- ----------------------------
-- Table structure for certifications
-- ----------------------------
DROP TABLE IF EXISTS `certifications`;
CREATE TABLE `certifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ucode` varchar(40) DEFAULT NULL,
  `certi_date` date DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `agent_id` varchar(20) DEFAULT NULL,
  `inputer_id` int(11) DEFAULT NULL,
  `body` varchar(128) DEFAULT NULL,
  `function` text,
  `description` text,
  `website` varchar(128) DEFAULT NULL,
  `address` text,
  `phone` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ucode` (`ucode`),
  UNIQUE KEY `ix_certifications_body` (`body`),
  KEY `inputer_id` (`inputer_id`),
  CONSTRAINT `certifications_ibfk_1` FOREIGN KEY (`inputer_id`) REFERENCES `admins` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of certifications
-- ----------------------------
INSERT INTO `certifications` VALUES ('1', 'b261ec1b-dac5-42e4-8a6e-3a8272135dd6', '2016-05-10', '2018-05-10', '370602197010133719', '1', '鲁东大学', '大专、本科、研究生学历教育，继续教育，专业培训，学术交流', '省重点建设高校', 'http://www.ldu.edu.cn/', '山东省烟台市芝罘区红旗中路186号', '0535—6672723');
INSERT INTO `certifications` VALUES ('2', '680d658b-ee88-4d0a-86b7-13f6babe5b4b', '2016-05-20', '2020-05-19', '440308196705083421', '1', '深圳大学', '学术，教育，公益，事业单位', '“特区大学”、“特色大学”', 'http://www.szu.edu.cn/2014/', '广东省深圳市深圳大学科技楼808', '(0755) 26536114 ');
INSERT INTO `certifications` VALUES ('3', '24609a3d-7617-43aa-bc2e-0c5191bcf1c9', '2016-05-20', '2017-05-20', '370523197804289842', '1', '山东大学', '学术，教育，培训', '国家首批重点建设的“211工程”和“985工程”大学，教育部直属重点综合性大学', 'http://www.sdu.edu.cn/', '山东省济南市山大南路27号', '（86）-531-88565657');

-- ----------------------------
-- Table structure for discussions
-- ----------------------------
DROP TABLE IF EXISTS `discussions`;
CREATE TABLE `discussions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author_id` int(11) DEFAULT NULL,
  `topic_id` int(11) DEFAULT NULL,
  `content` text,
  `post_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `topic_id` (`topic_id`),
  KEY `ix_discussions_post_time` (`post_time`),
  CONSTRAINT `discussions_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `discussions_ibfk_2` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of discussions
-- ----------------------------
INSERT INTO `discussions` VALUES ('1', '4', '1', '“我要这天，再遮不住我眼，我要这地，再埋不了我心，要这众生，都明白我意，要那诸佛，都烟消云散！”', '2016-05-14 15:48:53');
INSERT INTO `discussions` VALUES ('2', '2', '1', '猪八戒和孙悟空虽然都神通广大，但在命运面前终究是软弱无力的小人物。顶天立地的美猴王实际上仍然是那个充满惊恐的小猴子，而决心与命运抗争的天逢若非紧急也终究不肯以猪的面目见阿月。神仙尚且如此，何况吾辈生来渺小的小人物呢？随着年纪的增长，少年时素怀的“愿乘长风破万里浪”的豪情壮志早已经烟消云散，只剩下一个行尸走肉的家伙还在苟延残喘。自己何尝不是一只因为知道自己身份而在午夜对月痛哭的猪啊！但他们最终战胜了命运，而我呢？', '2016-05-14 16:14:34');
INSERT INTO `discussions` VALUES ('3', '4', '1', '楼上说得对。', '2016-05-20 07:03:47');
INSERT INTO `discussions` VALUES ('5', '4', '1', '比《大话西游》更适合小资MM们看的言情版西游记。', '2016-05-20 08:50:05');
INSERT INTO `discussions` VALUES ('6', '4', '1', '如来盯着唐僧看着……霎那间佛光普照……漫天的花瓣飞舞…… 唐僧微笑着对如来说：“干你娘……”。', '2016-05-20 08:50:19');
INSERT INTO `discussions` VALUES ('7', '4', '1', '经书只是一个水月镜花的信仰，取到了也未必能普度众生。', '2016-05-20 08:50:31');
INSERT INTO `discussions` VALUES ('8', '4', '1', '也许因为心情浮躁', '2016-05-20 08:50:43');
INSERT INTO `discussions` VALUES ('9', '4', '1', '还是几个月前，突然看到豆瓣上冒出了新版的悟空传，短信中学挚友说你还记得悟空传吗？她马上回过来一句“我要这天，再遮不住我眼，要这地，再埋不了我心，要这众生，都明白我意，要那诸佛，都烟消云散！”竟愣住了。六年了，再次看到它仍让人震撼。 最近几天又莫名总是想起第一句，总是记不全四句。记忆中的影像是高中被戏称为鸽子笼的宿舍。那年高三，我坐在上铺的床上，趁着别人都休息偷偷拿出悟空传来看。', '2016-05-20 08:50:55');
INSERT INTO `discussions` VALUES ('10', '4', '1', '还是几个月前，突然看到豆瓣上冒出了新版的悟空传，短信中学挚友说你还记得悟空传吗？她马上回过来一句“我要这天，再遮不住我眼，要这地，再埋不了我心，要这众生，都明白我意，要那诸佛，都烟消云散！”竟愣住了。六年了，再次看到它仍让人震撼。 最近几天又莫名总是想起第一句，总是记不全四句。记忆中的影像是高中被戏称为鸽子笼的宿舍。那年高三，我坐在上铺的床上，趁着别人都休息偷偷拿出悟空传来看。', '2016-05-20 08:51:06');
INSERT INTO `discussions` VALUES ('11', '4', '1', '还是几个月前，突然看到豆瓣上冒出了新版的悟空传，短信中学挚友说你还记得悟空传吗？她马上回过来一句“我要这天，再遮不住我眼，要这地，再埋不了我心，要这众生，都明白我意，要那诸佛，都烟消云散！”竟愣住了。六年了，再次看到它仍让人震撼。 最近几天又莫名总是想起第一句，总是记不全四句。记忆中的影像是高中被戏称为鸽子笼的宿舍。那年高三，我坐在上铺的床上，趁着别人都休息偷偷拿出悟空传来看。', '2016-05-20 08:51:09');
INSERT INTO `discussions` VALUES ('12', '4', '1', '还是几个月前，突然看到豆瓣上冒出了新版的悟空传，短信中学挚友说你还记得悟空传吗？。六年了，再次看到它仍让人震撼。 最近几天又莫名总是想起第一句，总是记不全四句。记忆中的影像是高中被戏称为鸽子笼的宿舍。那年高三，我坐在上铺的床上，趁着别人都休息偷偷拿出悟空传来看。', '2016-05-20 08:51:21');
INSERT INTO `discussions` VALUES ('13', '4', '1', '那年高三，我坐在上铺的床上，趁着别人都休息偷偷拿出悟空传来看。', '2016-05-20 08:51:30');
INSERT INTO `discussions` VALUES ('14', '4', '1', '在豆瓣上看到对《悟空传》的评论，想到了高中时一口气看完今何在的这部小说的情景。“我要这天，再遮不住我眼；要这地，再埋不了我心；要这众生，都明白我意；要那诸佛，都烟消云散！”当时颇有些激情燃烧的味道，现在看来，青春期特有的冲动。就像今何在为《悟空传》的再版写了这么一段题记。“从写作这个故事到现在，五年过去了。当年为这个故事而欢笑愤怒悲伤的情绪，已经难以回忆。', '2016-05-20 08:54:24');
INSERT INTO `discussions` VALUES ('15', '2', '1', '连番刺激使我的精神往更精神的方向发展了。', '2016-05-20 09:08:34');
INSERT INTO `discussions` VALUES ('16', '2', '1', '我这个人总是过时的厉害，看过时的书，做过时的事情，尊重过时的信仰。 常常满心欢喜的拿些过时的书宝贝起来。', '2016-05-20 09:09:42');
INSERT INTO `discussions` VALUES ('17', '2', '3', '“虽然是很早以前的书，但是在现在的背景下阅读也完全不过时，值得学习和反思的地方反而更有现实性。”', '2016-05-20 09:11:23');
INSERT INTO `discussions` VALUES ('18', '2', '2', '自顶！', '2016-05-20 10:23:07');
INSERT INTO `discussions` VALUES ('20', '2', '2', '时间是怎样爬上了我的眼珠，只有我自己最清楚。爱是一道光，如此闪亮；闪亮，让你眼睛更明亮。世上无难事，只要肯放弃。', '2016-05-20 11:20:24');
INSERT INTO `discussions` VALUES ('21', '2', '1', '你们在说什么？', '2016-05-21 00:02:31');
INSERT INTO `discussions` VALUES ('22', '2', '5', '世上无难事，只要肯放弃……23333333333333333', '2016-05-21 00:10:54');
INSERT INTO `discussions` VALUES ('23', '2', '6', '没人鸟我。我觉得会反弹，但是赢勇士也不容易！', '2016-05-21 01:04:05');

-- ----------------------------
-- Table structure for events
-- ----------------------------
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `poster_url` varchar(128) DEFAULT NULL,
  `detail` text,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `new_time` date DEFAULT NULL,
  `sponsor_id` int(11) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `address` varchar(256) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `sponsor_id` (`sponsor_id`),
  KEY `ix_events_end_time` (`end_time`),
  KEY `ix_events_new_time` (`new_time`),
  KEY `ix_events_start_time` (`start_time`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `events_ibfk_2` FOREIGN KEY (`sponsor_id`) REFERENCES `institutions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of events
-- ----------------------------
INSERT INTO `events` VALUES ('1', '1', null, '我校信息与电气工程学院将于本周六开始举行毕业生答辩。望各位将要参加答辩的毕业生，认真准备，\r\n\r\n争取取得好成绩。具体的日程安排请随时跟踪学院官网：http://www.xinke.ldu.edu.cn/。', '2016-05-21 08:00:00', '2016-05-22 17:30:00', '2016-05-16', '1', '信电学院毕业答辩', '山东省烟台市芝罘区世回尧街道鲁东大学逸夫实验楼', '37.5198', '121.354');
INSERT INTO `events` VALUES ('2', '6', 'http://127.0.0.1:5000/uploads/posters/sdfsgdfgd.png', '520这个日子表白的人肯定大于结婚的人，那些宅男又羞涩，又没经验该如何表白呢？\r\n鲁东大学心理健康社团将在五月十二日举办“大声说出你的爱”的活动，赶快行动吧！', '2016-05-20 07:20:00', '2016-05-20 22:00:00', '2016-05-19', '1', '5月20日——大声说出爱', '山东省烟台市芝罘区世回尧街道鲁东大学第五餐厅前面空地', '37.5248', '121.359');
INSERT INTO `events` VALUES ('3', '6', 'http://127.0.0.1:5000/uploads/posters/20160520075202737.jpg', '本次文化节的主题是“饺子文化大碰撞”，中外学生同台竞技，共同体验饺子文化。活动内容分包饺子体验、饺子文化互动和包饺子比赛三大板块。国际学生们在专业厨师和中国学生志愿者的指导协助下，围在桌前学习和体验包水饺。饺子文化互动板块分为中国饺子文化知识问答和国外饺子文化展示两项。活动现场，国际学生踊跃回答抽取的问题，从一来一去的题目问答中，学生们对中国饺子文化有了更多的了解。随后，来自埃及、俄罗斯、蒙古的学生分别以实物和图片的形式向大家介绍了本国的饺子文化，在场的学生切身感受到了世界饺子文化的碰撞与交融。包饺子比赛是最为激烈而紧张的部分，比赛分为个人挑战赛、中外学生2对2 pk小组赛和包饺子5人小组赛。', '2016-05-23 09:30:00', '2016-05-23 12:30:00', '2016-05-21', '2', '国际事务部举办国际学生公寓饺子文化节', '山东省济南市历城区山东大学公寓2号楼大厅', '36.7126', '117.094');
INSERT INTO `events` VALUES ('4', '1', null, '毕业答辩', '2016-05-10 10:25:00', '2016-05-18 14:25:00', '2016-05-21', '1', '答辩', '山东省济南市天桥区天桥东街街道天桥教工幼儿园29号', '36.6753', '117.001');

-- ----------------------------
-- Table structure for follows
-- ----------------------------
DROP TABLE IF EXISTS `follows`;
CREATE TABLE `follows` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `follow_time` datetime DEFAULT NULL,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`),
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of follows
-- ----------------------------
INSERT INTO `follows` VALUES ('1', '1', '2016-05-12 11:17:16');
INSERT INTO `follows` VALUES ('2', '1', '2016-05-12 11:30:34');
INSERT INTO `follows` VALUES ('2', '2', '2016-05-12 11:28:34');
INSERT INTO `follows` VALUES ('3', '3', '2016-05-12 11:33:33');
INSERT INTO `follows` VALUES ('4', '2', '2016-05-12 11:37:43');
INSERT INTO `follows` VALUES ('4', '4', '2016-05-12 11:35:59');
INSERT INTO `follows` VALUES ('5', '5', '2016-05-21 01:28:55');

-- ----------------------------
-- Table structure for groups
-- ----------------------------
DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(24) DEFAULT NULL,
  `icon_url` varchar(128) DEFAULT NULL,
  `intro` text,
  `birthday` date DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_groups_birthday` (`birthday`),
  KEY `ix_groups_name` (`name`),
  KEY `groups_ibfk_1` (`owner_id`),
  CONSTRAINT `groups_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of groups
-- ----------------------------
INSERT INTO `groups` VALUES ('1', '雀跃动漫组——地球上最爱动漫的一群人', 'http://127.0.0.1:5000/uploads/icons/20160504191406.png', '为什么，为什么，为什么！为什么执着于动漫，因为动漫是我们的信仰，是我的一切快乐的来源。坚持动漫就是我的王道！！！', '2016-05-12', '1');
INSERT INTO `groups` VALUES ('2', '朝阳公园东七门儿', 'http://127.0.0.1:5000/uploads/icons/9k_1.jpg', '《奇葩说》幕后制作团队米未传媒，马东议长创立并亲自带队，座落朝阳公园东七门儿。除奇葩说一手动态，还有“超独家”幕后猛料；7*24实时互动，奇葩面对面跟你撕*；限量珍藏，你想都不敢想的奇葩福利尽在“七门儿”里。', '2016-05-12', '3');
INSERT INTO `groups` VALUES ('3', '鲁东大学读书会', 'http://127.0.0.1:5000/uploads/icons/20160514194624.png', '“一个人只拥有此生是不够的，他还应该拥有诗意的世界”——王小波。从读书中给自己的心灵开辟一片乌托邦吧。', '2016-05-14', '4');
INSERT INTO `groups` VALUES ('4', '雷霆迷', 'http://127.0.0.1:5000/uploads/icons/thunder.png', '俄克拉何马雷霆（Oklahoma City Thunder）是世界上最伟大的球队！', '2016-05-21', '2');

-- ----------------------------
-- Table structure for institutions
-- ----------------------------
DROP TABLE IF EXISTS `institutions`;
CREATE TABLE `institutions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `certi_id` int(11) DEFAULT NULL,
  `uurl` varchar(64) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `logo_url` varchar(128) DEFAULT NULL,
  `poster_url` varchar(128) DEFAULT NULL,
  `intro` text,
  `password_hash` varchar(128) DEFAULT NULL,
  `enroll_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `certi_id` (`certi_id`),
  UNIQUE KEY `ix_institutions_uurl` (`uurl`),
  KEY `ix_institutions_enroll_date` (`enroll_date`),
  CONSTRAINT `institutions_ibfk_1` FOREIGN KEY (`certi_id`) REFERENCES `certifications` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of institutions
-- ----------------------------
INSERT INTO `institutions` VALUES ('1', '1', 'ldu', '鲁东大学', 'http://127.0.0.1:5000/uploads/logos/logoldu_1.png', 'http://127.0.0.1:5000/uploads/posters/ldu-screen.jpg', '鲁东大学唯一官方账号。学校坐落在“中国最佳魅力城市”——烟台，是一所以文理工为主体、多学科协调发展的省重点建设高校。2012年，成为首批“山东省应用型人才培养特色名校”、服务国家特殊需求博士人才培养项目单位。2014年，获批教育学博士后科研流动站。原文化部部长、著名作家王蒙评价鲁东大学“人杰校灵”。', 'pbkdf2:sha1:1000$WhMwXwch$ebfb604d711bfc5651326f6961b5f433989f9b04', '2016-05-10');
INSERT INTO `institutions` VALUES ('2', '3', 'sdu', 'sdu', null, null, null, 'pbkdf2:sha1:1000$0hbgfMS6$56be9acfbb5e2b37a272ff84e24050a5abea3a7a', '2016-05-20');

-- ----------------------------
-- Table structure for joins
-- ----------------------------
DROP TABLE IF EXISTS `joins`;
CREATE TABLE `joins` (
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `join_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`group_id`),
  KEY `group_id` (`group_id`),
  CONSTRAINT `joins_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
  CONSTRAINT `joins_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of joins
-- ----------------------------
INSERT INTO `joins` VALUES ('1', '1', '2016-05-12 11:26:54');
INSERT INTO `joins` VALUES ('2', '1', '2016-05-14 16:26:18');
INSERT INTO `joins` VALUES ('2', '3', '2016-05-14 16:14:17');
INSERT INTO `joins` VALUES ('2', '4', '2016-05-21 01:01:11');
INSERT INTO `joins` VALUES ('3', '2', '2016-05-12 11:35:02');
INSERT INTO `joins` VALUES ('4', '3', '2016-05-14 11:48:36');

-- ----------------------------
-- Table structure for marks
-- ----------------------------
DROP TABLE IF EXISTS `marks`;
CREATE TABLE `marks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) DEFAULT NULL,
  `url` varchar(128) DEFAULT NULL,
  `mark_time` datetime DEFAULT NULL,
  `marker_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `marker_id` (`marker_id`),
  KEY `ix_marks_mark_time` (`mark_time`),
  KEY `ix_marks_url` (`url`),
  CONSTRAINT `marks_ibfk_1` FOREIGN KEY (`marker_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of marks
-- ----------------------------
INSERT INTO `marks` VALUES ('1', '雀跃动漫组——地球上最爱动漫的一群人 - 小组 | 雀跃', 'http://127.0.0.1:5000/group/1', '2016-05-12 11:43:15', '4');
INSERT INTO `marks` VALUES ('2', '信电学院毕业答辩 | 雀跃', 'http://127.0.0.1:5000/event/1', '2016-05-18 14:38:08', '4');
INSERT INTO `marks` VALUES ('3', ' 看完《悟空传》，三观颠覆了 - 小组话题 | 雀跃', 'http://127.0.0.1:5000/group/3/topic/1', '2016-05-20 09:20:20', '2');
INSERT INTO `marks` VALUES ('4', ' 《C++从入门到放弃》在读 - 小组话题 | 雀跃', 'http://127.0.0.1:5000/group/3/topic/5', '2016-05-21 00:11:09', '2');

-- ----------------------------
-- Table structure for notifications
-- ----------------------------
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `post_time` datetime DEFAULT NULL,
  `publisher_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `publisher_id` (`publisher_id`),
  KEY `ix_notifications_post_time` (`post_time`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`publisher_id`) REFERENCES `institutions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of notifications
-- ----------------------------
INSERT INTO `notifications` VALUES ('1', '#信电学院#针对毕业生的毕业论文（设计）工作，在5.09~5.13各位四年级的学生需要上交论文正文电子稿（不含封皮、开题报告、结题报告、目录）。在此之前，望各位学生认真撰写论文，并与导师沟通，学习论文的撰写方法，把论文写好。望导师耐心指导学生的写作，并督促学生的撰写进度。', '2016-05-10 03:23:10', '1');
INSERT INTO `notifications` VALUES ('2', '昨日上午，我校2016年田径运动会在北区田径场隆重开幕。', '2016-05-13 00:45:22', '1');
INSERT INTO `notifications` VALUES ('3', '为了全方位的加强对大学生心理健康教育，提高大学生适应环境、管理自我、人际交往等各方面的能力，“缤纷校园，爱在鲁大”主题活动计划于5月24日上午在文化广场举行。心理健康节活动内容共分为speak it out、时光快递、漂流瓶、爱的抱抱四个板块，游戏种类形式多样、参与性强，奖品丰厚。每位同学均可积极参加。', '2016-05-19 19:26:05', '1');
INSERT INTO `notifications` VALUES ('4', 'Hello, world !', '2016-05-20 16:46:41', '2');
INSERT INTO `notifications` VALUES ('5', '5月17日，上海海洋大学党委副书记、副校长汪歙萍一行来山东大学访问交流，并就相关工作进行座谈。山大党委副书记仝兴华会见来访客人。', '2016-05-21 03:28:15', '2');

-- ----------------------------
-- Table structure for participates
-- ----------------------------
DROP TABLE IF EXISTS `participates`;
CREATE TABLE `participates` (
  `user_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `partici_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`event_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `participates_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`),
  CONSTRAINT `participates_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of participates
-- ----------------------------
INSERT INTO `participates` VALUES ('2', '2', '2016-05-20 12:52:36');
INSERT INTO `participates` VALUES ('2', '3', '2016-05-21 11:27:53');
INSERT INTO `participates` VALUES ('4', '1', '2016-05-18 13:10:29');

-- ----------------------------
-- Table structure for topics
-- ----------------------------
DROP TABLE IF EXISTS `topics`;
CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `title` varchar(128) DEFAULT NULL,
  `post_time` datetime DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  KEY `ix_topics_post_time` (`post_time`),
  KEY `topics_ibfk_1` (`author_id`),
  KEY `topics_ibfk_2` (`group_id`),
  CONSTRAINT `topics_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `topics_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of topics
-- ----------------------------
INSERT INTO `topics` VALUES ('1', '3', '4', '看完《悟空传》，三观颠覆了', '2016-05-14 11:59:58', '作者今何在以一个全新的视角看《西游记》，在他的笔下，强大者逃脱不了被奴役，康庄大道实际是早已设定好的绝路……一个很绝望的故事。');
INSERT INTO `topics` VALUES ('2', '1', '2', '征一个妹子，一起去杭州国际动漫节', '2016-05-14 16:29:20', '本人91年女生，4月27到5月2号的杭州国际动漫节，有妹子愿意同行么？');
INSERT INTO `topics` VALUES ('3', '3', '2', '《菊与刀》是一本好书吗？', '2016-05-20 09:10:48', '1944年，作者受美国政府所托，完成一项旨在认清日本民族的课题，并以之为二战后改造日本国家的指导。此书即该项目成果。在本书中，作者在简单叙述日本近代史的基础上，挖掘日本人矛盾性格的根源，并详细阐释日本人的“恩债”“人情”“义理”“忠孝”等理念，以及其他一些如幼儿抚养等生活习惯。尤为重要的是，作者在本书中提出了“耻感文化”和“罪感文化”这两个在后世引发巨大反响的概念。本书不愧为文化人类学模范。\r\n真是上面说的这样吗？');
INSERT INTO `topics` VALUES ('5', '3', '2', '《C++从入门到放弃》在读', '2016-05-21 00:04:16', '我最近在读《C++从入门到放弃》，感觉很不错。推荐给大家哦。');
INSERT INTO `topics` VALUES ('6', '4', '2', '下一回比赛，雷霆反弹还是继续摆烂？', '2016-05-21 01:03:12', '勇士在甲骨文球馆没有再让雷霆“以下犯上”的希望和念想继续得逞。他们只用了三节就让这一场比赛早早的失去了悬念。最终勇士以118-91的酣畅淋漓的大胜赢回了比赛，从而将大比分扳成1-1，结束了主场的前两战。下一战，你们觉得雷霆反弹还是继续摆烂？');
INSERT INTO `topics` VALUES ('7', '4', '2', '答辩', '2016-05-21 11:28:55', '大年');

-- ----------------------------
-- Table structure for tracks
-- ----------------------------
DROP TABLE IF EXISTS `tracks`;
CREATE TABLE `tracks` (
  `user_id` int(11) NOT NULL,
  `insti_id` int(11) NOT NULL,
  `track_time` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`,`insti_id`),
  KEY `insti_id` (`insti_id`),
  CONSTRAINT `tracks_ibfk_1` FOREIGN KEY (`insti_id`) REFERENCES `institutions` (`id`),
  CONSTRAINT `tracks_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tracks
-- ----------------------------
INSERT INTO `tracks` VALUES ('2', '1', '2016-05-20 22:16:40');
INSERT INTO `tracks` VALUES ('2', '2', '2016-05-21 03:49:38');

-- ----------------------------
-- Table structure for twitters
-- ----------------------------
DROP TABLE IF EXISTS `twitters`;
CREATE TABLE `twitters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `post_time` datetime DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `ix_twitters_post_time` (`post_time`),
  CONSTRAINT `twitters_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of twitters
-- ----------------------------
INSERT INTO `twitters` VALUES ('1', '感觉错过了沈从文。为什么所有中学语文教材推荐的都是《边城》呢，多无聊，尤其对一个看着TVB职场剧长大的城市独生女。看他其他一些小说，才知道希腊小庙里供着什么。', '2016-05-12 11:19:44', '1');
INSERT INTO `twitters` VALUES ('2', '商场通往负一层的楼梯上架了一个长长的滑梯 我敏捷地跟在小朋友后头滑了下去 非常开心。', '2016-05-12 11:24:25', '1');
INSERT INTO `twitters` VALUES ('3', '那种后来说，遇见了对的人就改变了想法的人，拜托，你之前就不是什么不婚主义者，不过是搪塞备胎们的借口。说多了，自己都以为是真的了。', '2016-05-12 11:32:21', '2');
INSERT INTO `twitters` VALUES ('4', '清炒土豆丝，不用醋，不用辣，也很好吃。', '2016-05-12 11:35:26', '3');
INSERT INTO `twitters` VALUES ('5', '饭否，生日快乐', '2016-05-12 11:42:44', '4');
INSERT INTO `twitters` VALUES ('6', '三楼这个露台设计的好尴尬 既挡了风景又没啥用 难道是给我们蹦迪吗？', '2016-05-14 11:44:36', '4');
INSERT INTO `twitters` VALUES ('7', '一只名叫犬山柴男的霓虹柴犬成为霓虹SBK社新闻的主播，播报新闻时啥都不做，只需要在镜头面前一本正经的卖萌卖脸。。。炒鸡萌。。。', '2016-05-14 15:59:35', '2');
INSERT INTO `twitters` VALUES ('8', '如果真的有穿越，我想去看看80年代的大学校园。我戴硕大的白色围巾，念大家都不懂的诗歌，然后女生们哭成一团，男孩私下写一个字条留在板凳上。周末去老乡会组织的舞会，穿洗烂了的背心，配初版的布尔迪尔。我喜欢谁，就在他经常去的图书馆的那个位置，留一封信，而他30年后才拆开。', '2016-05-14 16:18:52', '2');
INSERT INTO `twitters` VALUES ('9', '今天立夏，是夏天的开始。 夏天的开始，好像最先想到的是从浅绿变成深绿色的枝条与叶子。 好像是为了抵抗接下来的炎热时光一样，一种逐渐强壮的、稳定的绿色。 飞机总是会飞过天空。', '2016-05-18 13:11:11', '4');
INSERT INTO `twitters` VALUES ('10', '东山，还能看见这般景象：小船咿呀，芦苇飘摇，凉风轻荡，夕阳中，鸥鹭忘机。满船载着丰收之悦，透出的都是当地的质朴，有山有水，四处果香。这个场景跟《橘子红了》里面好像。帮东山陆巷古村落的怀德堂主人推广一下枇杷。正宗的白沙枇杷，30一斤。', '2016-05-19 22:27:48', '4');
INSERT INTO `twitters` VALUES ('11', '别人的朋友圈广告是卡地亚，我的朋友圈广告是口香糖。我穷的只买到起口香糖的事情连腾讯都知道了？', '2016-05-20 11:12:51', '2');
INSERT INTO `twitters` VALUES ('12', '本来觉得所谓什么富养挺无聊的，碰到某些位 ，感觉富养的理论也不是全无是处，别长大之后这么没见过世面的样子，让人笑话。', '2016-05-20 11:13:24', '2');
INSERT INTO `twitters` VALUES ('13', '“孩子”是个神话，并且这个神话已经规训了我们的眼睛，没有它，我们看不见任何现实中的孩子，有了它，我们所见的孩子与现实无限地偏离。', '2016-05-21 01:27:45', '1');
INSERT INTO `twitters` VALUES ('14', '昨天看了一篇文章，说吃多少都非常瘦的人基础代谢过于快，死得也会很早。我吓坏了，那我得活多长时间啊想都不敢想。', '2016-05-21 01:28:00', '1');
INSERT INTO `twitters` VALUES ('15', '北京时间凌晨一点三十七，我还在敲代码。厉害如我，没有几个。', '2016-05-21 01:38:38', '2');
INSERT INTO `twitters` VALUES ('16', 'PPT没做，答辩马上开始。', '2016-05-21 03:06:38', '2');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) DEFAULT NULL,
  `name` varchar(24) NOT NULL,
  `avatar_url` varchar(128) DEFAULT NULL,
  `portrait_url` varchar(128) DEFAULT NULL,
  `reg_date` date DEFAULT NULL,
  `intro` text,
  `signature` varchar(30) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `ix_users_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', 'jinsailun@jsl.com', '金赛纶', 'http://127.0.0.1:5000/uploads/avatars/20160427155035.png', '/static/images/portrait_default.png', '2016-05-12', '金赛纶，2000年7月31日出生，韩国儿童演员。金赛纶2009年凭借电影《旅行者》出道，2010年她与元斌一起出演了电影《大叔》并获得广泛关注，由于该电影的成功，金赛纶在2010年获得各大电影节的青睐，获得了新人演技奖的头衔。2011年金赛纶出演MBC周末剧《你能听见我的心吗？》，这是她首次参与电视剧的演出。2012年在MBC电视剧《女王的教师》展现了出色的演技，她与裴斗娜近期拍摄中的电影《道希》2014年5月上映。2014年主演的电视剧《high school love on》于7月份播出。', '我就是我，是颜色不一样的烟火。', '0', 'pbkdf2:sha1:1000$XIYYBomj$b554573a7ad2e91b11b83d37292a95680fcf31a7');
INSERT INTO `users` VALUES ('2', 'songzhongji@szj.com', '宋仲基', 'http://127.0.0.1:5000/uploads/avatars/20160427151600.png', 'http://127.0.0.1:5000/uploads/portraits/12968965832672.jpg', '2016-05-12', '宋仲基，1985年9月19日出生于韩国大田广域市，韩国演员、主持人。2008年出演电影《霜花店》进入演艺圈，之后在电视剧、电影、综艺主持多方发展。2009年在音乐节目Music Bank中担任主持，后在艺能节目《Running man》中担任固定嘉宾（E01——E41）。2010年出演电视剧《成均馆绯闻》具龙河一角，获得KBS演技大赏最佳人气奖。2011年在电视剧《树大根深》中饰演青年世宗，获得SBS演技大赏PD奖[1] 。2012年接拍KBS水木剧《善良的男人》，在KBS演技大赏中获得最佳男演员奖、网络人气奖及最佳情侣奖 。同年主演的电影《狼族少年》上映，正片票房达665万观影人次，累计突破700万观影人次，刷新了韩国爱情片的票房纪录，凭此片获得第49届百想艺术大赏电影部门最佳男演员提名。宋仲基于2013年8月27日入伍，于2015年5月26日退伍。2016年，主演电视剧《太阳的后裔》播出；3月，宋仲基担任LG Health&Beauty品牌代言人。', '最帅就是我，我就是Song Joong Ki', '0', 'pbkdf2:sha1:1000$pwy7IKbJ$02625d6cb446f412a83e3f0c6b4f4de1b57c690e');
INSERT INTO `users` VALUES ('3', 'jiangsida@jsd.com', '姜思达', '/static/images/avatar_default.png', '/static/images/portrait_default.png', '2016-05-12', null, null, '0', 'pbkdf2:sha1:1000$yMdAlMZ7$0b293684b11d53c079947f65a88da9d374928379');
INSERT INTO `users` VALUES ('4', 'songhuiqiao@shq.com', '宋慧乔', 'http://127.0.0.1:5000/uploads/avatars/song.png', '/static/images/portrait_default.png', '2016-05-12', '宋慧乔（송혜교），1981年11月22日出生于韩国大邱广域市，韩国影视女演员。其初期参加模特大赛成名，先后拍摄多部电影电视剧，代表作有与宋承宪、元斌合演的电视剧《蓝色生死恋》，及与Rain演出的电视剧《浪漫满屋》，这两套剧集令她在亚洲各地皆为人所熟悉。2005年开始，宋慧乔开始专注于电影方面的发展，出演《我和我的女友》。2007年，她出演的电影《黄真伊》上映。2008年，她出演电视剧《他们生活的世界》。2009年，她参演了中国电影《一代宗师》。2009年6月到2011年3月期间，与玄彬相恋。2013年的《那年冬天，风在吹》是宋慧乔阔别荧屏四年之久的又一电视剧。2016年2月，宋慧乔以母亲名义斥资90亿韩元，在首尔三成洞购入一间别墅。[2]2015年与宋仲基搭档主演电视剧《太阳的后裔》', '新作品《月亮的祖宗》热映中，谢谢关注！', '0', 'pbkdf2:sha1:1000$CBontqK4$3daeb852240cb7cc075ae3544d0e0c145c83fee5');
INSERT INTO `users` VALUES ('5', 'gaoxiaosong@gxs.com', '高晓松', '/static/images/avatar_default.png', '/static/images/portrait_default.png', '2016-05-21', null, null, '0', 'pbkdf2:sha1:1000$6QId0PYt$9ed44aefae2ee86664dcde3c4ecce50620d22bba');
