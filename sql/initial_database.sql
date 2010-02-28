CREATE TABLE `account` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(250) NOT NULL,
  `password` char(40) NOT NULL,
  `trusted` tinyint(1) NOT NULL default '0',
  `can_create` tinyint(1) NOT NULL default '1',
  `can_update` tinyint(1) NOT NULL default '1',
  `can_delete` tinyint(1) NOT NULL default '1',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

CREATE TABLE `account_mask` (
  `id` int(11) NOT NULL auto_increment,
  `account_id` int(11) default NULL,
  `mask` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `mask` (`mask`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1858 DEFAULT CHARSET=latin1;

CREATE TABLE `intelligence` (
  `id` int(11) NOT NULL auto_increment,
  `mask` varchar(250) default NULL,
  `target` varchar(250) default NULL,
  `keywords` varchar(255) default NULL,
  `keyphrase` varchar(100) NOT NULL,
  `value` text NOT NULL,
  `indicator` varchar(10) NOT NULL COMMENT 'is / are / was / etcetera',
  `created` datetime NOT NULL,
  `modified` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `lastused` datetime default NULL,
  PRIMARY KEY  (`id`),
  FULLTEXT KEY `keyphrase` (`keyphrase`),
  FULLTEXT KEY `value` (`value`),
  FULLTEXT KEY `keyphrase_2` (`keyphrase`,`value`)
) ENGINE=MyISAM AUTO_INCREMENT=66607 DEFAULT CHARSET=latin1;

CREATE TABLE `phrase_category` (
  `id` int(11) NOT NULL auto_increment,
  `category` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `category` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

LOCK TABLES `phrase_category` WRITE;
/*!40000 ALTER TABLE `phrase_category` DISABLE KEYS */;
INSERT INTO `phrase_category` VALUES (5,'confirmation'),(7,'filler'),(4,'indicator'),(9,'interrogative'),(2,'preconception'),(1,'punctuation'),(6,'rebuttal'),(3,'statement'),(8,'to_someone');
/*!40000 ALTER TABLE `phrase_category` ENABLE KEYS */;
UNLOCK TABLES;


CREATE TABLE `phrase` (
  `id` int(11) NOT NULL auto_increment,
  `response` text NOT NULL,
  `category_id` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `phrase_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `phrase_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=457 DEFAULT CHARSET=latin1;

LOCK TABLES `phrase` WRITE;
/*!40000 ALTER TABLE `phrase` DISABLE KEYS */;
INSERT INTO `phrase` VALUES (1,'?',1,1),(2,'!',1,1),(3,'.',1,1),(4,'!?',1,1),(5,'?!',1,1),(6,'%s %s %s',2,1),(10,'is',4,1),(11,'are',4,1),(12,'was',4,1),(13,'has',4,1),(14,'ok',5,1),(15,'got it',5,1),(16,'understood',5,1),(19,'I already have that, %s',6,1),(20,'Someone already said that, %s',6,1),(21,'haha',7,1),(22,'lol',7,1),(23,'hehe',7,1),(24,'kek',7,1),(29,'%s',3,1),(30,'been',4,1),(31,'am',4,1),(32,'were',4,1),(420,'be',4,1),(422,'isn\'t',4,1),(424,'have',4,1),(425,'had',4,1),(426,'loves',4,1),(427,'will',4,1),(428,'looks',4,1),(429,'like',4,1),(430,'use',4,1),(431,'being',4,1),(432,'become',4,1),(433,'seems',4,1),(434,'hate',4,1),(435,'to',4,1),(436,'on',4,1),(437,'should',4,1),(438,'could',4,1),(439,'do',4,1),(440,'done',4,1),(441,'did',4,1),(442,'shall',4,1),(443,'should',4,1),(444,'may',4,1),(445,'might',4,1),(446,'must',4,1),(447,'for',4,1),(448,'%s, $who',8,1),(449,'$who: %s',8,1),(450,'$who, %s',8,1),(451,'who',9,1),(452,'what',9,1),(453,'when',9,1),(454,'where',9,1),(455,'why',9,1),(456,'how',9,1);
/*!40000 ALTER TABLE `phrase` ENABLE KEYS */;
UNLOCK TABLES;


