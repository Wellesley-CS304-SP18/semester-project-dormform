-- MySQL dump 10.13  Distrib 5.5.50, for Linux (x86_64)
--
-- Host: localhost    Database: dormform_db
-- ------------------------------------------------------
-- Server version	5.5.50-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `favorite`
--

DROP TABLE IF EXISTS `favorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favorite` (
  `username` varchar(10) DEFAULT NULL,
  `roomID` varchar(10) DEFAULT NULL,
  KEY `username` (`username`),
  KEY `roomID` (`roomID`),
  CONSTRAINT `favorite_ibfk_1` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE CASCADE,
  CONSTRAINT `favorite_ibfk_2` FOREIGN KEY (`roomID`) REFERENCES `room` (`roomID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorite`
--

LOCK TABLES `favorite` WRITE;
/*!40000 ALTER TABLE `favorite` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `picture`
--

DROP TABLE IF EXISTS `picture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `picture` (
  `picID` int(11) NOT NULL AUTO_INCREMENT,
  `pictureFile` varchar(50) NOT NULL,
  `reviewID` int(11) NOT NULL,
  `roomID` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`picID`),
  KEY `reviewID` (`reviewID`),
  CONSTRAINT `picture_ibfk_1` FOREIGN KEY (`reviewID`) REFERENCES `review` (`reviewID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `picture`
--

LOCK TABLES `picture` WRITE;
/*!40000 ALTER TABLE `picture` DISABLE KEYS */;
INSERT INTO `picture` VALUES (1,'19lfutami02.jpeg',19,'SHA409'),(2,'20lfutami02.jpeg',20,'SHA410'),(3,'21lfutami02.jpeg',21,'SHA201'),(4,'20lfutami02_2.jpeg',20,'SHA410'),(5,'22bji.jpeg',22,'SHA208'),(6,'16bji.jpeg',16,'SHA408'),(7,'4bji.jpeg',4,'DAV265'),(8,'23bji.jpeg',23,'SHA206');
/*!40000 ALTER TABLE `picture` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `review` (
  `reviewID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(10) NOT NULL,
  `roomID` varchar(10) NOT NULL,
  `review` varchar(1000) NOT NULL,
  `overallRating` int(11) NOT NULL,
  `flooring` varchar(10) NOT NULL,
  PRIMARY KEY (`reviewID`),
  KEY `username` (`username`),
  KEY `roomID` (`roomID`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`username`) REFERENCES `student` (`username`) ON DELETE CASCADE,
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`roomID`) REFERENCES `room` (`roomID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (1,'lfutami','DAV265','It\'s a great room! The sun wakes you up in the morning',4,'Wood'),(2,'lfutami','DAV257','This room is bad. The garbage trucks will make you cry.',2,'carpet'),(3,'myang5','DAV265','It\'s a great room! The sun wakes you up in the morning',4,'Wood'),(4,'bji','DAV265','It\'s a great room! The sun wakes you up in the morning',4,'Wood'),(5,'bji','DAV259','super awful',1,'Linoleum'),(6,'bji','SHA404','scott',1,'Wood'),(7,'bji','SHA407','jesus christ',1,'Linoleum'),(8,'bji','SHA409','this room is okay!',3,'Linoleum'),(9,'bji','SHA413','great room!',1,'Linoleum'),(10,'bji','SHA403','DSadsSAD',4,'Linoleum'),(11,'bji','SHA200','why',1,'Wood'),(12,'lfutami','SHA200','why',1,'Wood'),(13,'bji','DAV257','great!',4,'Wood'),(14,'bji','SHA412','yes',5,'Wood'),(15,'bji','DAV260','it\'s not wood, i lie',5,'Wood'),(16,'bji','SHA408','jdfjkds;af',4,'Wood'),(17,'bji','SHA400','please work',4,'Carpet'),(18,'lfutami02','SHA413','great room!',1,'Linoleum'),(19,'lfutami02','SHA409','hi midori',3,'Carpet'),(20,'lfutami02','SHA410','I don\'t like it',3,'Carpet'),(21,'lfutami02','SHA201','very sticky',3,'Carpet'),(22,'bji','SHA208','great room!!',4,'Linoleum'),(23,'bji','SHA206','amazing',3,'Carpet');
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room` (
  `roomID` varchar(10) NOT NULL,
  `building` varchar(20) NOT NULL,
  `roomNum` int(11) NOT NULL,
  `type` varchar(10) NOT NULL,
  `avgRating` decimal(3,2) DEFAULT NULL,
  PRIMARY KEY (`roomID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES ('BAT201','Bates',201,'single',NULL),('BAT202','Bates',202,'double',NULL),('BAT203','Bates',203,'single',NULL),('BAT204','Bates',204,'double',NULL),('BAT205','Bates',205,'single',NULL),('BAT206','Bates',206,'double',NULL),('DAV257','Davis',257,'single',3.00),('DAV259','Davis',259,'firstyear',0.00),('DAV260','Davis',260,'firstyear',5.00),('DAV261','Davis',261,'firstyear',0.00),('DAV263','Davis',263,'single',0.00),('DAV264','Davis',264,'single',0.00),('DAV265','Davis',265,'single',0.00),('SHA200','Shafer',200,'triple',2.00),('SHA201','Shafer',201,'triple',3.00),('SHA206','Shafer',206,'double',3.00),('SHA208','Shafer',208,'firstyear',4.00),('SHA400','Shafer',400,'single',4.00),('SHA401','Shafer',401,'single',0.00),('SHA402','Shafer',402,'single',0.00),('SHA403','Shafer',403,'single',0.00),('SHA404','Shafer',404,'single',0.00),('SHA406','Shafer',406,'single',0.00),('SHA407','Shafer',407,'single',0.00),('SHA408','Shafer',408,'single',4.00),('SHA409','Shafer',409,'single',3.00),('SHA410','Shafer',410,'single',3.00),('SHA411','Shafer',411,'single',0.00),('SHA412','Shafer',412,'single',5.00),('SHA413','Shafer',413,'single',1.50);
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `username` varchar(10) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('bji','beemovie'),('lfutami','beemovie'),('lfutami02','beemovie02'),('lfutami03','beemovie03'),('myang5','beemovie');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-14 12:51:45
