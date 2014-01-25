-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 28, 2010 at 04:10 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6-1+lenny4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `factoids`
--

-- KARMA TABLE
DROP TABLE IF EXISTS `karma`;
CREATE TABLE IF NOT EXISTS `karma` (
  `id` int(11) NOT NULL auto_increment,
  `term` varchar(30) NOT NULL,
  `karma` tinyint(1) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;


-- --------------------------------------------------------

--
-- Table structure for table `account`
--
DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(250) NOT NULL,
  `password` char(40) NOT NULL,
  `trusted` tinyint(1) NOT NULL default '0',
  `can_create` tinyint(1) NOT NULL default '1',
  `can_update` tinyint(1) NOT NULL default '1',
  `can_delete` tinyint(1) NOT NULL default '1',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;


--
-- Dumping data for table `account`
--


-- --------------------------------------------------------

--
-- Table structure for table `account_mask`
--

DROP TABLE IF EXISTS `account_mask`;
CREATE TABLE IF NOT EXISTS `account_mask` (
  `id` int(11) NOT NULL auto_increment,
  `account_id` int(11) default NULL,
  `mask` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `mask` (`mask`),
  KEY `account_id` (`account_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `intelligence`
--

DROP TABLE IF EXISTS `intelligence`;
CREATE TABLE IF NOT EXISTS `intelligence` (
  `id` int(11) NOT NULL auto_increment,
  `source` varchar(250) default NULL,
  `target` varchar(250) default NULL,
  `keywords` text,
  `message` text NOT NULL,
  `created` datetime NOT NULL,
  `modified` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `lastused` datetime default NULL,
  PRIMARY KEY  (`id`),
  FULLTEXT KEY `message` (`message`),
  FULLTEXT KEY `keywords` (`keywords`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Dumping data for table `intelligence`
--


-- --------------------------------------------------------

--
-- Table structure for table `phrase`
--

DROP TABLE IF EXISTS `phrase`;
CREATE TABLE IF NOT EXISTS `phrase` (
  `id` int(11) NOT NULL auto_increment,
  `response` text NOT NULL,
  `category_id` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY  (`id`),
  KEY `category_id` (`category_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=457 ;

--
-- Dumping data for table `phrase`
--

INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(1, '?', 1, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(2, '!', 1, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(3, '.', 1, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(4, '!?', 1, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(5, '?!', 1, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(6, '%s %s %s', 2, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(10, 'is', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(11, 'are', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(12, 'was', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(13, 'has', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(14, 'ok', 5, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(15, 'got it', 5, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(16, 'understood', 5, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(19, 'I already have that, %s', 6, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(20, 'Someone already said that, %s', 6, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(21, 'haha', 7, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(22, 'lol', 7, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(23, 'hehe', 7, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(24, 'kek', 7, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(29, '%s', 3, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(30, 'been', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(31, 'am', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(32, 'were', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(420, 'be', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(422, 'isn''t', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(424, 'have', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(425, 'had', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(426, 'loves', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(427, 'will', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(428, 'looks', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(429, 'like', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(430, 'use', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(431, 'being', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(432, 'become', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(433, 'seems', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(434, 'hate', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(435, 'to', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(436, 'on', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(437, 'should', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(438, 'could', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(439, 'do', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(440, 'done', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(441, 'did', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(442, 'shall', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(443, 'should', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(444, 'may', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(445, 'might', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(446, 'must', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(447, 'for', 4, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(448, '%s, $who', 8, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(449, '$who: %s', 8, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(450, '$who, %s', 8, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(451, 'who', 9, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(452, 'what', 9, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(453, 'when', 9, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(454, 'where', 9, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(455, 'why', 9, 1);
INSERT INTO `phrase` (`id`, `response`, `category_id`, `enabled`) VALUES(456, 'how', 9, 1);

-- --------------------------------------------------------

--
-- Table structure for table `phrase_category`
--

DROP TABLE IF EXISTS `phrase_category`;
CREATE TABLE IF NOT EXISTS `phrase_category` (
  `id` int(11) NOT NULL auto_increment,
  `category` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `category` (`category`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `phrase_category`
--

INSERT INTO `phrase_category` (`id`, `category`) VALUES(5, 'confirmation');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(7, 'filler');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(4, 'indicator');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(9, 'interrogative');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(2, 'preconception');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(1, 'punctuation');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(6, 'rebuttal');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(3, 'statement');
INSERT INTO `phrase_category` (`id`, `category`) VALUES(8, 'to_someone');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `phrase`
--
ALTER TABLE `phrase`
  ADD CONSTRAINT `phrase_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `phrase_category` (`id`);

DELIMITER $$
--
-- Procedures
--
DROP PROCEDURE IF EXISTS `search_intelligence`$$
CREATE DEFINER=`db9`@`localhost` PROCEDURE `search_intelligence`(
    query TEXT,
    minutes_since INT
)
BEGIN
    SELECT
        id,
        MATCH (message) AGAINST (query) AS score,
        lastused
    FROM intelligence
    WHERE (
        MATCH (message) AGAINST (query) > 0
    
        AND (
            lastused IS NULL
            OR timestampdiff(MINUTE , lastused, NOW()) > minutes_since
        )
    )
    ORDER BY lastused ASC, score DESC;
END$$

DELIMITER ;

 ALTER TABLE intelligence ADD FULLTEXT(keywords);
