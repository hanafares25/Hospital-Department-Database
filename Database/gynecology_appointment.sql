-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: gynecology
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `app_ID` int NOT NULL AUTO_INCREMENT,
  `date` varchar(45) DEFAULT NULL,
  `DOCTOR_D_ID` int NOT NULL,
  `ROOM_Room_number` int NOT NULL,
  `Urgency` varchar(45) DEFAULT NULL,
  `symptoms` varchar(45) DEFAULT NULL,
  `Patient_P_ID` int DEFAULT NULL,
  PRIMARY KEY (`app_ID`),
  UNIQUE KEY `app_ID_UNIQUE` (`app_ID`),
  KEY `fk_APPOINTMENT_DOCTOR1_idx` (`DOCTOR_D_ID`),
  KEY `fk_APPOINTMENT_ROOM1_idx` (`ROOM_Room_number`),
  CONSTRAINT `fk_APPOINTMENT_DOCTOR1` FOREIGN KEY (`DOCTOR_D_ID`) REFERENCES `doctor` (`D_ID`),
  CONSTRAINT `fk_APPOINTMENT_ROOM1` FOREIGN KEY (`ROOM_Room_number`) REFERENCES `room` (`Room_number`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,'12',2,3,'Urgent','headache',NULL),(2,'2023-01-10T02:16:00+02:00',2,3,'Urgent','headache',NULL),(3,'2023-01-09T08:45:00+02:00',19000,3,'Check-up','I have pain in my stomach',NULL),(4,'2023-01-09T10:35:00+02:00',19000,3,'Check-up','I feel sick',8),(5,'2023-03-06T16:30:00+02:00',19000,3,'Urgent','I have headache',8),(6,'2023-01-01T12:30:00+02:00',19000,3,'Check-up','I feel sick',8);
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-07 15:57:43
