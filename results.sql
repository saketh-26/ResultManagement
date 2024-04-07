-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: result
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `userName` varchar(30) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phoneNumber` varchar(10) DEFAULT NULL,
  `password` varchar(10) NOT NULL,
  `passCode` varchar(40) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`userName`,`password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('rama','datta@codegnan.com','9988776655','rama@123','a1b2c3','male');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `userName` varchar(50) DEFAULT NULL,
  `password` varchar(10) DEFAULT NULL,
  KEY `FK_admin` (`userName`,`password`),
  CONSTRAINT `FK_admin` FOREIGN KEY (`userName`, `password`) REFERENCES `admin` (`userName`, `password`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marks`
--

DROP TABLE IF EXISTS `marks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marks` (
  `stud_id` int DEFAULT NULL,
  `subject` varchar(50) NOT NULL,
  `obtained` int DEFAULT NULL,
  KEY `stud_id` (`stud_id`),
  KEY `subject` (`subject`),
  CONSTRAINT `marks_ibfk_1` FOREIGN KEY (`stud_id`) REFERENCES `students` (`studentId`),
  CONSTRAINT `marks_ibfk_2` FOREIGN KEY (`subject`) REFERENCES `subjects` (`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marks`
--

LOCK TABLES `marks` WRITE;
/*!40000 ALTER TABLE `marks` DISABLE KEYS */;
INSERT INTO `marks` VALUES (206812,'Computer Science',50),(206812,'Hindi',65);
/*!40000 ALTER TABLE `marks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `msds1`
--

DROP TABLE IF EXISTS `msds1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `msds1` (
  `subject` varchar(50) DEFAULT NULL,
  `obtained_marks` int DEFAULT NULL,
  `total_marks` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `msds1`
--

LOCK TABLES `msds1` WRITE;
/*!40000 ALTER TABLE `msds1` DISABLE KEYS */;
/*!40000 ALTER TABLE `msds1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `msds2`
--

DROP TABLE IF EXISTS `msds2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `msds2` (
  `subject` varchar(50) DEFAULT NULL,
  `total_marks` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `msds2`
--

LOCK TABLES `msds2` WRITE;
/*!40000 ALTER TABLE `msds2` DISABLE KEYS */;
INSERT INTO `msds2` VALUES ('Maths',100);
/*!40000 ALTER TABLE `msds2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `msds3`
--

DROP TABLE IF EXISTS `msds3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `msds3` (
  `subject` varchar(50) DEFAULT NULL,
  `total_marks` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `msds3`
--

LOCK TABLES `msds3` WRITE;
/*!40000 ALTER TABLE `msds3` DISABLE KEYS */;
/*!40000 ALTER TABLE `msds3` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `studentId` int NOT NULL,
  `studentName` varchar(50) DEFAULT NULL,
  `fatherName` varchar(50) DEFAULT NULL,
  `motherName` varchar(50) DEFAULT NULL,
  `phoneNumber` varchar(10) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `emailId` varchar(30) DEFAULT NULL,
  `adharNumber` bigint DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `section` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`studentId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (206805,' Jonnala Vasudha Reddy','Jonnala Haritha','Jonnala Venkata Reddy','7330105552',' Beside ZP High School Nuthakki','vasudhareddyjonnala@gmail.com',761166011767,'Female','msds1'),(206810,'Peram Haritha','Peram Subramanyam','Peram.subbulu','8790672639','Srungarapuram','harithaperam1@gmail.com',884913859165,'Female','msds1'),(206811,'Shaziya','Shaik Rehman','Shaik Sharmila','9492965890','D.no:1044,Kandrika','farhanashaik986655@gmail.com',247630735548,'Female ','msds1'),(206812,'Sk Ayesha Begum','Sk Nagul Meera Bhai','Sk Shajabi','9381614384','vadlapudi, near  zp high school','shaikayesha21216@gmail.com',511586051272,'Female','msds1'),(206813,'Sk Farhana','Sk Moulali','Sk Bajidbi','9866556993','Beside anjaneya temple,Nutakki','farhanashaik986655@gmail.com',247630735548,'Female','msds1'),(206815,'Shaik Shaheena','Shaik Sadiq Rehman','Shaik Sharmila','9492965890','D.no:1044,Kandrika','shaikshaheena5421@gmail.com',401307238580,'Female','msds1');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `section` varchar(20) DEFAULT NULL,
  `course_id` varchar(20) DEFAULT NULL,
  `subject` varchar(50) NOT NULL,
  `total_marks` int DEFAULT NULL,
  PRIMARY KEY (`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES ('msds1','DSCT11A ','Computer Science',100),('msds1','ENGT11B','English',100),('msds1','DSCT22L ','ERTYUI',100),('msds1','HINT11','Hindi',100),('msds1','MATT16','Maths',100),('msds1','STAT13','Statistics',100);
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-27  4:01:49
