-- MySQL dump 10.13  Distrib 9.5.0, for Win64 (x86_64)
--
-- Host: localhost    Database: darkerdatabase
-- ------------------------------------------------------
-- Server version	9.5.0

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
-- Current Database: `darkerdatabase`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `darkerdatabase` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `darkerdatabase`;

--
-- Table structure for table `adas_product_name_enum`
--

DROP TABLE IF EXISTS `adas_product_name_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adas_product_name_enum` (
  `Type` varchar(100) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adas_product_name_enum`
--

LOCK TABLES `adas_product_name_enum` WRITE;
/*!40000 ALTER TABLE `adas_product_name_enum` DISABLE KEYS */;
INSERT INTO `adas_product_name_enum` VALUES ('G-PILOT 2.0'),('G-PILOT 3.0');
/*!40000 ALTER TABLE `adas_product_name_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `algorithm_input`
--

DROP TABLE IF EXISTS `algorithm_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `algorithm_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `app_ID` int NOT NULL,
  `Algo_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_algorithm_input_app1_idx` (`app_ID`),
  KEY `fk_algorithm_input_algorithms1_idx` (`Algo_Name`),
  CONSTRAINT `fk_algorithm_input_algorithms1` FOREIGN KEY (`Algo_Name`) REFERENCES `algorithms` (`Name`),
  CONSTRAINT `fk_algorithm_input_app1` FOREIGN KEY (`app_ID`) REFERENCES `app` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `algorithm_input`
--

LOCK TABLES `algorithm_input` WRITE;
/*!40000 ALTER TABLE `algorithm_input` DISABLE KEYS */;
INSERT INTO `algorithm_input` VALUES (1,1,'CNN'),(2,2,'EKF'),(3,2,'Particle_Filter'),(4,3,'3rd ploynome'),(5,3,'5rd polynome'),(6,3,'PID');
/*!40000 ALTER TABLE `algorithm_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `algorithms`
--

DROP TABLE IF EXISTS `algorithms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `algorithms` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `algorithms`
--

LOCK TABLES `algorithms` WRITE;
/*!40000 ALTER TABLE `algorithms` DISABLE KEYS */;
INSERT INTO `algorithms` VALUES (1,'PID','/'),(2,'LQR','/'),(3,'CNN','/'),(4,'BEV','/'),(5,'OCC','/'),(6,'TRANSFORMER','/'),(7,'FREESPACE','/'),(8,'StateFlow','/'),(9,'VLA','/'),(10,'WorldModel','/'),(11,'EKF','/'),(12,'Particle_Filter','/'),(13,'Bezier Curb','/'),(14,'3rd ploynome','/'),(15,'5rd polynome','/');
/*!40000 ALTER TABLE `algorithms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app`
--

DROP TABLE IF EXISTS `app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `SupplierName` varchar(45) NOT NULL,
  `App_Type` varchar(45) NOT NULL,
  `App_Perimeter` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_app_suppliers1_idx` (`SupplierName`),
  KEY `fk_app_apptype_enum1_idx` (`App_Type`),
  KEY `fk_app_appperimeter_enum1_idx` (`App_Perimeter`),
  CONSTRAINT `fk_app_appperimeter_enum1` FOREIGN KEY (`App_Perimeter`) REFERENCES `appperimeter_enum` (`TYPE`),
  CONSTRAINT `fk_app_apptype_enum1` FOREIGN KEY (`App_Type`) REFERENCES `apptype_enum` (`TYPE`),
  CONSTRAINT `fk_app_suppliers1` FOREIGN KEY (`SupplierName`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app`
--

LOCK TABLES `app` WRITE;
/*!40000 ALTER TABLE `app` DISABLE KEYS */;
INSERT INTO `app` VALUES (1,'EQ4.0-Basic','Mobileye','Mixed','Perception'),(2,'OBJD','Valeo','Rule_Based','Perception'),(3,'V_PNC','Valeo','Rule_Based','PnC');
/*!40000 ALTER TABLE `app` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_input`
--

DROP TABLE IF EXISTS `app_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `App_Name` varchar(45) NOT NULL,
  `ecu_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_app_input_app1_idx` (`App_Name`),
  KEY `fk_app_input_ecu1_idx` (`ecu_ID`),
  CONSTRAINT `fk_app_input_app1` FOREIGN KEY (`App_Name`) REFERENCES `app` (`Name`),
  CONSTRAINT `fk_app_input_ecu1` FOREIGN KEY (`ecu_ID`) REFERENCES `ecu` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_input`
--

LOCK TABLES `app_input` WRITE;
/*!40000 ALTER TABLE `app_input` DISABLE KEYS */;
INSERT INTO `app_input` VALUES (6,'EQ4.0-Basic',1),(7,'OBJD',1),(8,'V_PNC',1),(9,'EQ4.0-Basic',3),(10,'OBJD',3),(11,'V_PNC',3);
/*!40000 ALTER TABLE `app_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applicalble_enum`
--

DROP TABLE IF EXISTS `applicalble_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicalble_enum` (
  `Value` varchar(45) NOT NULL,
  PRIMARY KEY (`Value`),
  UNIQUE KEY `Value_UNIQUE` (`Value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applicalble_enum`
--

LOCK TABLES `applicalble_enum` WRITE;
/*!40000 ALTER TABLE `applicalble_enum` DISABLE KEYS */;
INSERT INTO `applicalble_enum` VALUES ('M'),('N'),('O');
/*!40000 ALTER TABLE `applicalble_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appperimeter_enum`
--

DROP TABLE IF EXISTS `appperimeter_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appperimeter_enum` (
  `TYPE` varchar(45) NOT NULL,
  PRIMARY KEY (`TYPE`),
  UNIQUE KEY `TYPE_UNIQUE` (`TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appperimeter_enum`
--

LOCK TABLES `appperimeter_enum` WRITE;
/*!40000 ALTER TABLE `appperimeter_enum` DISABLE KEYS */;
INSERT INTO `appperimeter_enum` VALUES ('Driving+Parking Stack'),('DrivingStack'),('End-to-End'),('EnvModel'),('FunctionManagement'),('Fusion'),('Map&Loc'),('ParkingStack'),('Perception'),('PnC');
/*!40000 ALTER TABLE `appperimeter_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apptype_enum`
--

DROP TABLE IF EXISTS `apptype_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apptype_enum` (
  `TYPE` varchar(45) NOT NULL,
  PRIMARY KEY (`TYPE`),
  UNIQUE KEY `TYPE_UNIQUE` (`TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apptype_enum`
--

LOCK TABLES `apptype_enum` WRITE;
/*!40000 ALTER TABLE `apptype_enum` DISABLE KEYS */;
INSERT INTO `apptype_enum` VALUES ('AI_Based'),('Mixed'),('Rule_Based');
/*!40000 ALTER TABLE `apptype_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bsp`
--

DROP TABLE IF EXISTS `bsp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bsp` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bsp`
--

LOCK TABLES `bsp` WRITE;
/*!40000 ALTER TABLE `bsp` DISABLE KEYS */;
INSERT INTO `bsp` VALUES (1,'Example'),(2,'Example2');
/*!40000 ALTER TABLE `bsp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calculator`
--

DROP TABLE IF EXISTS `calculator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calculator` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Description` text,
  `CyberSecurity` tinyint DEFAULT NULL,
  `MAX_TEMP` float DEFAULT NULL,
  `MIN_TEMP` float DEFAULT NULL,
  `Temperature_Range` varchar(45) GENERATED ALWAYS AS (concat(_utf8mb4'[',`MIN_TEMP`,_utf8mb4'°C~',`MAX_TEMP`,_utf8mb4'°C]')) VIRTUAL,
  `Domain` varchar(45) NOT NULL,
  `Fusa_Level` varchar(45) NOT NULL,
  `Type` varchar(45) NOT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Power_Consumption` float DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Calculator_Name_UNIQUE` (`Name`),
  KEY `fk_calculator_domain_enum1_idx` (`Domain`),
  KEY `fk_calculator_fusa_enum1_idx` (`Fusa_Level`),
  KEY `fk_calculator_calculator_type_enum1_idx` (`Type`),
  KEY `fk_calculator_suppliers_enum1_idx` (`Supplier_Name`),
  KEY `NameIndex` (`Name`),
  CONSTRAINT `fk_calculator_calculator_type_enum1` FOREIGN KEY (`Type`) REFERENCES `calculator_type_enum` (`TYPE`),
  CONSTRAINT `fk_calculator_domain_enum1` FOREIGN KEY (`Domain`) REFERENCES `domain_enum` (`VALUE`),
  CONSTRAINT `fk_calculator_fusa_enum1` FOREIGN KEY (`Fusa_Level`) REFERENCES `fusa_enum` (`LEVEL`),
  CONSTRAINT `fk_calculator_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculator`
--

LOCK TABLES `calculator` WRITE;
/*!40000 ALTER TABLE `calculator` DISABLE KEYS */;
INSERT INTO `calculator` (`ID`, `Name`, `Description`, `CyberSecurity`, `MAX_TEMP`, `MIN_TEMP`, `Domain`, `Fusa_Level`, `Type`, `Supplier_Name`, `Power_Consumption`) VALUES (1,'TDA4-VM-PLUS','The TDA4VM processor family targeted at ADAS and Autonomous Vehicle (AV) applications and built on extensive market knowledge accumulated over a decade of TI’s leadership in the ADAS processor market. The unique combination high-performance compute, deep-learning engine, dedicated accelerators for signal and image processing in a functional safety compliant targeted architecture make the TDA4VM devices a great fit for several industrial applications, such as: Robotics, Machine Vision, Radar, and so on. ',0,105,-40,'ADAS','ASIL_D','SoC','TI',NULL),(2,'QC8650P-AAAA','[QAM8650P is the next generation Qualcomm® Snapdragon®\nadvanced driver-assistance systems (ADAS) module designed\nfor superior performance and power efficiency.\nIt has been developed as a Safety Element out of\nContext (SEooC). The key components of the QAM8650P\nmodule include the SA8650P SoC, PMM8650AU (×4) power\nmanagement IC, third party power management]',1,105,-40,'ADAS','ASIL_D','SoC','QualComm',30),(3,'RH850-U2A16','The RH850/U2A MCU is the first member of Renesas’ cross-domain MCUs, a new generation of automotive-control devices, designed to address the growing need to integrate multiple applications into a single chip to realize unified electronic control units (ECUs) for the evolving electrical/electronic architecture (E/E architecture). Based on 28 nanometer (nm) process technology, the 32-bit RH850/U2A automotive MCU builds on key functions from Renesas’ RH850/Px Series for chassis control and RH850/Fx Series for body control to deliver improved performance.',1,105,-40,'ADAS','ASIL_B','MCU','Renesas',NULL),(4,'QC8620P','This the description for the 8620P chipset product',0,105,-40,'ADAS','ASIL_D','SoC','QualComm',NULL),(5,'QC8775-AAAA','////',0,105,-40,'ADAS','ASIL_D','SIP','QualComm',NULL),(6,'J2','///',0,105,-40,'ADAS','ASIL_B','SoC','HorizonRobotics',NULL),(7,'J6E','///',0,105,-40,'ADAS','ASIL_D','SoC','HorizonRobotics',NULL),(8,'EQ4M','///',0,105,-40,'ADAS','ASIL_D','SoC','Mobileye',1),(10,'EQ6L','This is the Low gamme product 6 Generation of Mobileye EQ product series ',1,105,-40,'ADAS','ASIL_B','SoC','Mobileye',3);
/*!40000 ALTER TABLE `calculator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calculator_ecu_input`
--

DROP TABLE IF EXISTS `calculator_ecu_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calculator_ecu_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ecu_ID` int NOT NULL,
  `calculator_Name` varchar(45) NOT NULL,
  `Number` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_calculator_ecu_input_ecu1_idx` (`ecu_ID`),
  KEY `fk_calculator_ecu_input_calculator1_idx` (`calculator_Name`),
  CONSTRAINT `fk_calculator_ecu_input_calculator1` FOREIGN KEY (`calculator_Name`) REFERENCES `calculator` (`Name`),
  CONSTRAINT `fk_calculator_ecu_input_ecu1` FOREIGN KEY (`ecu_ID`) REFERENCES `ecu` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculator_ecu_input`
--

LOCK TABLES `calculator_ecu_input` WRITE;
/*!40000 ALTER TABLE `calculator_ecu_input` DISABLE KEYS */;
INSERT INTO `calculator_ecu_input` VALUES (1,1,'EQ4M',1),(2,1,'RH850-U2A16',1),(5,2,'TDA4-VM-PLUS',1),(6,3,'EQ4M',1),(7,3,'RH850-U2A16',1);
/*!40000 ALTER TABLE `calculator_ecu_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calculator_input`
--

DROP TABLE IF EXISTS `calculator_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calculator_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Number` int DEFAULT NULL,
  `Calculator_Name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_calculator_input_calculator1_idx` (`Calculator_Name`),
  CONSTRAINT `fk_calculator_input_calculator1` FOREIGN KEY (`Calculator_Name`) REFERENCES `calculator` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculator_input`
--

LOCK TABLES `calculator_input` WRITE;
/*!40000 ALTER TABLE `calculator_input` DISABLE KEYS */;
INSERT INTO `calculator_input` VALUES (1,1,'EQ4M'),(2,1,'RH850-U2A16');
/*!40000 ALTER TABLE `calculator_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `calculator_type_enum`
--

DROP TABLE IF EXISTS `calculator_type_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `calculator_type_enum` (
  `TYPE` varchar(45) NOT NULL,
  PRIMARY KEY (`TYPE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculator_type_enum`
--

LOCK TABLES `calculator_type_enum` WRITE;
/*!40000 ALTER TABLE `calculator_type_enum` DISABLE KEYS */;
INSERT INTO `calculator_type_enum` VALUES ('MCU'),('SIP'),('SoC');
/*!40000 ALTER TABLE `calculator_type_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camera`
--

DROP TABLE IF EXISTS `camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camera` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Type` varchar(45) DEFAULT NULL,
  `Image_Sensor` varchar(45) NOT NULL,
  `Lens` varchar(45) NOT NULL,
  `Serializer` varchar(45) NOT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_camera_Image_sensors1_idx` (`Image_Sensor`),
  KEY `fk_camera_lens1_idx` (`Lens`),
  KEY `fk_camera_serializers1_idx` (`Serializer`),
  KEY `fk_camera_suppliers_enum1_idx` (`Supplier_Name`),
  KEY `NAMEINDEX` (`Name`),
  KEY `fk_camera_camera_type_enum_idx` (`Type`),
  CONSTRAINT `fk_camera_camera_type_enum` FOREIGN KEY (`Type`) REFERENCES `camera_type_enum` (`Type`),
  CONSTRAINT `fk_camera_Image_sensors1` FOREIGN KEY (`Image_Sensor`) REFERENCES `image_sensors` (`Name`),
  CONSTRAINT `fk_camera_lens1` FOREIGN KEY (`Lens`) REFERENCES `lens` (`Name`),
  CONSTRAINT `fk_camera_serializers1` FOREIGN KEY (`Serializer`) REFERENCES `serializers` (`Name`),
  CONSTRAINT `fk_camera_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camera`
--

LOCK TABLES `camera` WRITE;
/*!40000 ALTER TABLE `camera` DISABLE KEYS */;
INSERT INTO `camera` VALUES (1,'CAM1','FISHEYE','IMX728','SF816WN','MAX96717F','Desay'),(5,'CAM 222','PIN HOLE','IMX728','SF816WN','MAX96717F','Valeo'),(6,'CAM SURRONG','PIN HOLE','IMX623','YTOT-MCP308','DS90UB971','Bosch'),(7,'CAM_VALEO_120_8M_PH','PIN HOLE','1H1','SF811ZG','MAX96717','Valeo'),(8,'CAM_VALEO_100_2M_PH','PIN HOLE','OV2775','SF811ZG','DS90UB953-Q1','Valeo'),(9,'CAM_8M_100_DRSide','PIN HOLE','ISX031','YTOT-MCP308','DS90UB971','Aptiv'),(10,'CAM_2M_FE_VALEO','FISHEYE','ISX031','YTOT-MCP308','DS90UB953-Q1','Valeo'),(11,'CAM_2M_100_DR','PIN HOLE','ISX031','YTOT-MCP308','DS90UB971','Desay'),(12,'CAM_2M_100_DR_Valeo','FISHEYE','ISX031','YTOT-MCP308','DS90UB971','Valeo');
/*!40000 ALTER TABLE `camera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camera_input`
--

DROP TABLE IF EXISTS `camera_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camera_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `POSITION` varchar(45) NOT NULL,
  `system_solution_ID` int NOT NULL,
  `Camera_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_camera_input_position_enum1_idx` (`POSITION`),
  KEY `fk_camera_input_system_solution1_idx` (`system_solution_ID`),
  KEY `fk_camera_input_camera1_idx` (`Camera_Name`),
  CONSTRAINT `fk_camera_input_camera1` FOREIGN KEY (`Camera_Name`) REFERENCES `camera` (`Name`),
  CONSTRAINT `fk_camera_input_position_enum1` FOREIGN KEY (`POSITION`) REFERENCES `position_enum` (`POSITION`),
  CONSTRAINT `fk_camera_input_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camera_input`
--

LOCK TABLES `camera_input` WRITE;
/*!40000 ALTER TABLE `camera_input` DISABLE KEYS */;
INSERT INTO `camera_input` VALUES (1,'Front_Center',3,'CAM_VALEO_100_2M_PH'),(2,'Left',3,'CAM_2M_FE_VALEO'),(3,'Right',3,'CAM_2M_FE_VALEO'),(4,'Rear_Center',3,'CAM_2M_FE_VALEO'),(5,'Front_Center',3,'CAM_2M_FE_VALEO'),(6,'Front_Center',4,'CAM_VALEO_120_8M_PH'),(7,'Rear_Center',4,'CAM_VALEO_100_2M_PH'),(8,'Left',4,'CAM_2M_FE_VALEO'),(9,'Front_Center',4,'CAM_2M_FE_VALEO'),(10,'Front_Center',4,'CAM_2M_FE_VALEO'),(11,'Rear_Center',4,'CAM_2M_FE_VALEO');
/*!40000 ALTER TABLE `camera_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `camera_type_enum`
--

DROP TABLE IF EXISTS `camera_type_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `camera_type_enum` (
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camera_type_enum`
--

LOCK TABLES `camera_type_enum` WRITE;
/*!40000 ALTER TABLE `camera_type_enum` DISABLE KEYS */;
INSERT INTO `camera_type_enum` VALUES ('COCKPIT'),('FISHEYE'),('PIN HOLE');
/*!40000 ALTER TABLE `camera_type_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Commenter_Name` varchar(45) DEFAULT NULL,
  `Comment_Content` text,
  `Comment_Likes` varchar(45) DEFAULT NULL,
  `forum_data_ID` int NOT NULL,
  `Comment_Time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `fk_comment_forum_data1_idx` (`forum_data_ID`),
  CONSTRAINT `fk_comment_forum_data1` FOREIGN KEY (`forum_data_ID`) REFERENCES `forum_data` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corperate_input`
--

DROP TABLE IF EXISTS `corperate_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corperate_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `vehicle_mark_ID` int NOT NULL,
  `Corperate_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_Corperate_input_suppliers1_idx` (`Corperate_Name`),
  KEY `fk_Corperate_input_vehicle_mark1_idx` (`vehicle_mark_ID`),
  CONSTRAINT `fk_Corperate_input_suppliers1` FOREIGN KEY (`Corperate_Name`) REFERENCES `suppliers` (`Name`),
  CONSTRAINT `fk_Corperate_input_vehicle_mark1` FOREIGN KEY (`vehicle_mark_ID`) REFERENCES `vehicle_mark` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corperate_input`
--

LOCK TABLES `corperate_input` WRITE;
/*!40000 ALTER TABLE `corperate_input` DISABLE KEYS */;
INSERT INTO `corperate_input` VALUES (1,180,'Daimler'),(2,180,'GEELY'),(3,135,'GEELY'),(4,135,'Volvo');
/*!40000 ALTER TABLE `corperate_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(90) DEFAULT NULL,
  `CN_Name` varchar(90) DEFAULT NULL,
  `Continent_Name` varchar(90) DEFAULT NULL,
  `Continent_Name_CN` varchar(90) DEFAULT NULL,
  `Remark` varchar(90) DEFAULT ' ',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=198 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
INSERT INTO `country` VALUES (1,'Afghanistan','阿富汗','Asia','亚洲','联合国会员国'),(2,'Bahrain','巴林','Asia','亚洲','联合国会员国'),(3,'Bangladesh','孟加拉国','Asia','亚洲','联合国会员国'),(4,'Bhutan','不丹','Asia','亚洲','联合国会员国'),(5,'Brunei Darussalam','文莱达鲁萨兰国','Asia','亚洲','联合国会员国'),(6,'Cambodia','柬埔寨','Asia','亚洲','联合国会员国'),(7,'China','中国','Asia','亚洲','联合国安理会常任理事国；台湾是中国省级行政区，非独立国家'),(8,'Cyprus','塞浦路斯','Asia','亚洲','联合国会员国，地理跨欧亚，行政归属亚洲'),(9,'East Timor','东帝汶','Asia','亚洲','联合国会员国，2002年独立'),(10,'Georgia','格鲁吉亚','Asia','亚洲','联合国会员国'),(11,'India','印度','Asia','亚洲','联合国会员国'),(12,'Indonesia','印度尼西亚','Asia','亚洲','联合国会员国，世界最大群岛国家'),(13,'Iran, Islamic Republic of','伊朗伊斯兰共和国','Asia','亚洲','联合国会员国'),(14,'Iraq','伊拉克','Asia','亚洲','联合国会员国'),(15,'Israel','以色列','Asia','亚洲','联合国会员国'),(16,'Japan','日本','Asia','亚洲','联合国会员国'),(17,'Jordan','约旦','Asia','亚洲','联合国会员国'),(18,'Kazakhstan','哈萨克斯坦','Asia','亚洲','联合国会员国，世界最大内陆国'),(19,'Kuwait','科威特','Asia','亚洲','联合国会员国'),(20,'Kyrgyzstan','吉尔吉斯斯坦','Asia','亚洲','联合国会员国'),(21,'Lebanon','黎巴嫩','Asia','亚洲','联合国会员国'),(22,'Malaysia','马来西亚','Asia','亚洲','联合国会员国'),(23,'Maldives','马尔代夫','Asia','亚洲','联合国会员国，印度洋岛国'),(24,'Mongolia','蒙古','Asia','亚洲','联合国会员国'),(25,'Myanmar','缅甸','Asia','亚洲','联合国会员国'),(26,'Nepal','尼泊尔','Asia','亚洲','联合国会员国'),(27,'Democratic People\'s Republic of Korea','朝鲜民主主义人民共和国','Asia','亚洲','联合国会员国'),(28,'Oman','阿曼','Asia','亚洲','联合国会员国'),(29,'Pakistan','巴基斯坦','Asia','亚洲','联合国会员国'),(30,'Palestine','巴勒斯坦','Asia','亚洲','联合国观察员国'),(31,'Philippines','菲律宾','Asia','亚洲','联合国会员国'),(32,'Qatar','卡塔尔','Asia','亚洲','联合国会员国'),(33,'Republic of Korea','大韩民国','Asia','亚洲','联合国会员国，简称韩国'),(34,'Saudi Arabia','沙特阿拉伯','Asia','亚洲','联合国会员国'),(35,'Singapore','新加坡','Asia','亚洲','联合国会员国'),(36,'Sri Lanka','斯里兰卡','Asia','亚洲','联合国会员国'),(37,'Syrian Arab Republic','阿拉伯叙利亚共和国','Asia','亚洲','联合国会员国，简称叙利亚'),(38,'Tajikistan','塔吉克斯坦','Asia','亚洲','联合国会员国'),(39,'Thailand','泰国','Asia','亚洲','联合国会员国'),(40,'Turkey','土耳其','Asia','亚洲','联合国会员国，地理跨欧亚，行政归属亚洲'),(41,'Turkmenistan','土库曼斯坦','Asia','亚洲','联合国会员国'),(42,'United Arab Emirates','阿拉伯联合酋长国','Asia','亚洲','联合国会员国，简称阿联酋'),(43,'Uzbekistan','乌兹别克斯坦','Asia','亚洲','联合国会员国'),(44,'Vietnam','越南','Asia','亚洲','联合国会员国'),(45,'Yemen','也门','Asia','亚洲','联合国会员国'),(46,'Armenia','亚美尼亚','Asia','亚洲','联合国会员国'),(47,'Azerbaijan','阿塞拜疆','Asia','亚洲','联合国会员国，地理跨欧亚，行政归属亚洲'),(48,'Laos','老挝','Asia','亚洲','联合国会员国，全称老挝人民民主共和国'),(49,'Albania','阿尔巴尼亚','Europe','欧洲','联合国会员国'),(50,'Andorra','安道尔','Europe','欧洲','联合国会员国'),(51,'Austria','奥地利','Europe','欧洲','联合国会员国'),(52,'Belarus','白俄罗斯','Europe','欧洲','联合国会员国'),(53,'Belgium','比利时','Europe','欧洲','联合国会员国，欧盟创始国'),(54,'Bosnia and Herzegovina','波斯尼亚和黑塞哥维那','Europe','欧洲','联合国会员国，简称波黑'),(55,'Bulgaria','保加利亚','Europe','欧洲','联合国会员国'),(56,'Croatia','克罗地亚','Europe','欧洲','联合国会员国'),(57,'Czech Republic','捷克共和国','Europe','欧洲','联合国会员国，简称捷克'),(58,'Denmark','丹麦','Europe','欧洲','联合国会员国'),(59,'Estonia','爱沙尼亚','Europe','欧洲','联合国会员国'),(60,'Finland','芬兰','Europe','欧洲','联合国会员国'),(61,'France','法兰西共和国','Europe','欧洲','联合国安理会常任理事国，简称法国'),(62,'Germany','德意志联邦共和国','Europe','欧洲','联合国会员国，简称德国'),(63,'Greece','希腊','Europe','欧洲','联合国会员国'),(64,'Hungary','匈牙利','Europe','欧洲','联合国会员国'),(65,'Iceland','冰岛','Europe','欧洲','联合国会员国'),(66,'Ireland','爱尔兰','Europe','欧洲','联合国会员国'),(67,'Italy','意大利','Europe','欧洲','联合国会员国'),(68,'Latvia','拉脱维亚','Europe','欧洲','联合国会员国'),(69,'Liechtenstein','列支敦士登','Europe','欧洲','联合国会员国'),(70,'Lithuania','立陶宛','Europe','欧洲','联合国会员国'),(71,'Luxembourg','卢森堡','Europe','欧洲','联合国会员国'),(72,'Malta','马耳他','Europe','欧洲','联合国会员国'),(73,'Republic of Moldova','摩尔多瓦共和国','Europe','欧洲','联合国会员国，简称摩尔多瓦'),(74,'Monaco','摩纳哥','Europe','欧洲','联合国会员国'),(75,'Montenegro','黑山','Europe','欧洲','联合国会员国'),(76,'Netherlands','荷兰王国','Europe','欧洲','联合国会员国，简称荷兰'),(77,'North Macedonia','北马其顿','Europe','欧洲','联合国会员国'),(78,'Norway','挪威','Europe','欧洲','联合国会员国'),(79,'Poland','波兰','Europe','欧洲','联合国会员国'),(80,'Portugal','葡萄牙','Europe','欧洲','联合国会员国'),(81,'Romania','罗马尼亚','Europe','欧洲','联合国会员国'),(82,'San Marino','圣马力诺','Europe','欧洲','联合国会员国'),(83,'Serbia','塞尔维亚','Europe','欧洲','联合国会员国'),(84,'Slovakia','斯洛伐克','Europe','欧洲','联合国会员国'),(85,'Slovenia','斯洛文尼亚','Europe','欧洲','联合国会员国'),(86,'Spain','西班牙','Europe','欧洲','联合国会员国'),(87,'Sweden','瑞典','Europe','欧洲','联合国会员国'),(88,'Switzerland','瑞士','Europe','欧洲','联合国会员国，永久中立国'),(89,'Ukraine','乌克兰','Europe','欧洲','联合国会员国'),(90,'United Kingdom of Great Britain and Northern Ireland','大不列颠及北爱尔兰联合王国','Europe','欧洲','联合国安理会常任理事国，简称英国'),(91,'Vatican City','梵蒂冈城国','Europe','欧洲','联合国观察员国，世界最小国家'),(92,'Russia','俄罗斯联邦','Europe','欧洲','联合国安理会常任理事国，地理跨欧亚，行政归属欧洲'),(93,'Algeria','阿尔及利亚','Africa','非洲','联合国会员国'),(94,'Angola','安哥拉','Africa','非洲','联合国会员国'),(95,'Benin','贝宁','Africa','非洲','联合国会员国'),(96,'Botswana','博茨瓦纳','Africa','非洲','联合国会员国'),(97,'Burkina Faso','布基纳法索','Africa','非洲','联合国会员国'),(98,'Burundi','布隆迪','Africa','非洲','联合国会员国'),(99,'Cameroon','喀麦隆','Africa','非洲','联合国会员国'),(100,'Cape Verde','佛得角','Africa','非洲','联合国会员国，大西洋岛国'),(101,'Central African Republic','中非共和国','Africa','非洲','联合国会员国，简称中非'),(102,'Chad','乍得','Africa','非洲','联合国会员国'),(103,'Comoros','科摩罗','Africa','非洲','联合国会员国，印度洋岛国'),(104,'Congo','刚果共和国','Africa','非洲','联合国会员国，简称刚果（布）'),(105,'Democratic Republic of the Congo','刚果民主共和国','Africa','非洲','联合国会员国，简称刚果（金）'),(106,'Côte d\'Ivoire','科特迪瓦','Africa','非洲','联合国会员国'),(107,'Djibouti','吉布提','Africa','非洲','联合国会员国'),(108,'Egypt','埃及','Africa','非洲','联合国会员国，地理跨亚非，行政归属非洲'),(109,'Equatorial Guinea','赤道几内亚','Africa','非洲','联合国会员国'),(110,'Eritrea','厄立特里亚','Africa','非洲','联合国会员国'),(111,'Eswatini','埃斯瓦蒂尼','Africa','非洲','联合国会员国，旧称斯威士兰'),(112,'Ethiopia','埃塞俄比亚','Africa','非洲','联合国会员国，非洲唯一未被殖民的国家'),(113,'Gabon','加蓬','Africa','非洲','联合国会员国'),(114,'Gambia','冈比亚','Africa','非洲','联合国会员国'),(115,'Ghana','加纳','Africa','非洲','联合国会员国'),(116,'Guinea','几内亚','Africa','非洲','联合国会员国'),(117,'Guinea-Bissau','几内亚比绍','Africa','非洲','联合国会员国'),(118,'Kenya','肯尼亚','Africa','非洲','联合国会员国'),(119,'Lesotho','莱索托','Africa','非洲','联合国会员国，被南非包围的内陆国'),(120,'Liberia','利比里亚','Africa','非洲','联合国会员国'),(121,'Libya','利比亚','Africa','非洲','联合国会员国'),(122,'Madagascar','马达加斯加','Africa','非洲','联合国会员国，世界第四大岛'),(123,'Malawi','马拉维','Africa','非洲','联合国会员国'),(124,'Mali','马里','Africa','非洲','联合国会员国'),(125,'Mauritania','毛里塔尼亚','Africa','非洲','联合国会员国'),(126,'Mauritius','毛里求斯','Africa','非洲','联合国会员国，印度洋岛国'),(127,'Morocco','摩洛哥','Africa','非洲','联合国会员国'),(128,'Mozambique','莫桑比克','Africa','非洲','联合国会员国'),(129,'Namibia','纳米比亚','Africa','非洲','联合国会员国'),(130,'Niger','尼日尔','Africa','非洲','联合国会员国'),(131,'Nigeria','尼日利亚','Africa','非洲','联合国会员国，非洲人口最多国家'),(132,'Rwanda','卢旺达','Africa','非洲','联合国会员国'),(133,'São Tomé and Príncipe','圣多美和普林西比','Africa','非洲','联合国会员国，几内亚湾岛国'),(134,'Senegal','塞内加尔','Africa','非洲','联合国会员国'),(135,'Seychelles','塞舌尔','Africa','非洲','联合国会员国，印度洋岛国'),(136,'Sierra Leone','塞拉利昂','Africa','非洲','联合国会员国'),(137,'Somalia','索马里','Africa','非洲','联合国会员国'),(138,'South Africa','南非','Africa','非洲','联合国会员国'),(139,'South Sudan','南苏丹','Africa','非洲','联合国会员国，2011年独立，最新加入联合国'),(140,'Sudan','苏丹','Africa','非洲','联合国会员国'),(141,'United Republic of Tanzania','坦桑尼亚联合共和国','Africa','非洲','联合国会员国，简称坦桑尼亚'),(142,'Togo','多哥','Africa','非洲','联合国会员国'),(143,'Tunisia','突尼斯','Africa','非洲','联合国会员国'),(144,'Uganda','乌干达','Africa','非洲','联合国会员国'),(145,'Zambia','赞比亚','Africa','非洲','联合国会员国'),(146,'Zimbabwe','津巴布韦','Africa','非洲','联合国会员国'),(147,'Antigua and Barbuda','安提瓜和巴布达','North America','北美洲','联合国会员国'),(148,'Bahamas','巴哈马','North America','北美洲','联合国会员国'),(149,'Barbados','巴巴多斯','North America','北美洲','联合国会员国'),(150,'Belize','伯利兹','North America','北美洲','联合国会员国'),(151,'Canada','加拿大','North America','北美洲','联合国会员国'),(152,'Costa Rica','哥斯达黎加','North America','北美洲','联合国会员国'),(153,'Cuba','古巴','North America','北美洲','联合国会员国'),(154,'Dominica','多米尼克','North America','北美洲','联合国会员国'),(155,'Dominican Republic','多米尼加共和国','North America','北美洲','联合国会员国'),(156,'El Salvador','萨尔瓦多','North America','北美洲','联合国会员国'),(157,'Grenada','格林纳达','North America','北美洲','联合国会员国'),(158,'Guatemala','危地马拉','North America','北美洲','联合国会员国'),(159,'Haiti','海地','North America','北美洲','联合国会员国'),(160,'Honduras','洪都拉斯','North America','北美洲','联合国会员国'),(161,'Jamaica','牙买加','North America','北美洲','联合国会员国'),(162,'Mexico','墨西哥','North America','北美洲','联合国会员国'),(163,'Nicaragua','尼加拉瓜','North America','北美洲','联合国会员国'),(164,'Panama','巴拿马','North America','北美洲','联合国会员国'),(165,'Saint Kitts and Nevis','圣基茨和尼维斯','North America','北美洲','联合国会员国'),(166,'Saint Lucia','圣卢西亚','North America','北美洲','联合国会员国'),(167,'Saint Vincent and the Grenadines','圣文森特和格林纳丁斯','North America','北美洲','联合国会员国'),(168,'Trinidad and Tobago','特立尼达和多巴哥','North America','北美洲','联合国会员国'),(169,'United States of America','美利坚合众国','North America','北美洲','联合国安理会常任理事国，简称美国'),(170,'Argentina','阿根廷','South America','南美洲','联合国会员国'),(171,'Bolivia, Plurinational State of','多民族玻利维亚国','South America','南美洲','联合国会员国，简称玻利维亚'),(172,'Brazil','巴西联邦共和国','South America','南美洲','联合国会员国，简称巴西，南美洲最大国家'),(173,'Chile','智利','South America','南美洲','联合国会员国'),(174,'Colombia','哥伦比亚','South America','南美洲','联合国会员国'),(175,'Ecuador','厄瓜多尔','South America','南美洲','联合国会员国'),(176,'Guyana','圭亚那','South America','南美洲','联合国会员国'),(177,'Paraguay','巴拉圭','South America','南美洲','联合国会员国，内陆国'),(178,'Peru','秘鲁','South America','南美洲','联合国会员国'),(179,'Suriname','苏里南','South America','南美洲','联合国会员国'),(180,'Uruguay','乌拉圭','South America','南美洲','联合国会员国'),(181,'Venezuela, Bolivarian Republic of','委内瑞拉玻利瓦尔共和国','South America','南美洲','联合国会员国，简称委内瑞拉'),(182,'Australia','澳大利亚','Oceania','大洋洲','联合国会员国'),(183,'Cook Islands','库克群岛','Oceania','大洋洲','准主权国家，与新西兰自由联系'),(184,'Fiji','斐济','Oceania','大洋洲','联合国会员国'),(185,'Federated States of Micronesia','密克罗尼西亚联邦','Oceania','大洋洲','联合国会员国'),(186,'Kiribati','基里巴斯','Oceania','大洋洲','联合国会员国'),(187,'Marshall Islands','马绍尔群岛','Oceania','大洋洲','联合国会员国'),(188,'Nauru','瑙鲁','Oceania','大洋洲','联合国会员国，世界最小岛国之一'),(189,'New Zealand','新西兰','Oceania','大洋洲','联合国会员国'),(190,'Niue','纽埃','Oceania','大洋洲','准主权国家，与新西兰自由联系'),(191,'Palau','帕劳','Oceania','大洋洲','联合国会员国'),(192,'Papua New Guinea','巴布亚新几内亚','Oceania','大洋洲','联合国会员国'),(193,'Samoa','萨摩亚','Oceania','大洋洲','联合国会员国'),(194,'Solomon Islands','所罗门群岛','Oceania','大洋洲','联合国会员国'),(195,'Tonga','汤加','Oceania','大洋洲','联合国会员国'),(196,'Tuvalu','图瓦卢','Oceania','大洋洲','联合国会员国'),(197,'Vanuatu','瓦努阿图','Oceania','大洋洲','联合国会员国');
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_structure`
--

DROP TABLE IF EXISTS `db_structure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `db_structure` (
  `Type` varchar(45) NOT NULL,
  `Description` varchar(45) DEFAULT NULL,
  `CN` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Type`),
  UNIQUE KEY `Type_UNIQUE` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_structure`
--

LOCK TABLES `db_structure` WRITE;
/*!40000 ALTER TABLE `db_structure` DISABLE KEYS */;
INSERT INTO `db_structure` VALUES ('objects','直接展现给用户的产品','顶层数据对象'),('subobject','独立存在的产品但是不直接针对用户','非顶层对象数据'),('supportobject','库数据或者枚举量数据','辅助数据');
/*!40000 ALTER TABLE `db_structure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliverables`
--

DROP TABLE IF EXISTS `deliverables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliverables` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Work_ID` int NOT NULL,
  `Deliverable` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_Deliverables_Work1_idx` (`Work_ID`),
  KEY `fk_Deliverables_Deliveralbe_content1_idx` (`Deliverable`),
  CONSTRAINT `fk_Deliverables_Deliveralbe_content1` FOREIGN KEY (`Deliverable`) REFERENCES `deliveralbe_content` (`Name`),
  CONSTRAINT `fk_Deliverables_Work1` FOREIGN KEY (`Work_ID`) REFERENCES `work` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliverables`
--

LOCK TABLES `deliverables` WRITE;
/*!40000 ALTER TABLE `deliverables` DISABLE KEYS */;
INSERT INTO `deliverables` VALUES (2,1,'产品PRD'),(3,2,'对标报告'),(4,2,'子系统规范');
/*!40000 ALTER TABLE `deliverables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliveralbe_content`
--

DROP TABLE IF EXISTS `deliveralbe_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveralbe_content` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Doc` varchar(45) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `NameIndex` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliveralbe_content`
--

LOCK TABLES `deliveralbe_content` WRITE;
/*!40000 ALTER TABLE `deliveralbe_content` DISABLE KEYS */;
INSERT INTO `deliveralbe_content` VALUES (1,'SSS','产品PRD'),(2,'KKK','对标报告'),(3,'PPP','子系统规范');
/*!40000 ALTER TABLE `deliveralbe_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deserializers`
--

DROP TABLE IF EXISTS `deserializers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deserializers` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) DEFAULT NULL,
  `Data_Rate` float DEFAULT NULL,
  `MIN_TEMP` float DEFAULT NULL,
  `MAX_TEMP` float DEFAULT NULL,
  `Supply_Voltage` float DEFAULT NULL,
  `EMI_Level` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Interface_Type` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_deserializers_suppliers1_idx` (`Supplier_Name`),
  KEY `fk_deserializers_interface_enum_sub1_idx` (`Interface_Type`),
  CONSTRAINT `fk_deserializers_interface_enum_sub1` FOREIGN KEY (`Interface_Type`) REFERENCES `interface_enum_sub` (`SUBTYPE_VALUE`),
  CONSTRAINT `fk_deserializers_suppliers1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deserializers`
--

LOCK TABLES `deserializers` WRITE;
/*!40000 ALTER TABLE `deserializers` DISABLE KEYS */;
INSERT INTO `deserializers` VALUES (1,'DS90UB954-Q1',6,-40,105,3.3,'CISPR 25 Class 2, ISO 11452-2','TI','FPD_LINK III'),(2,'DS90UB948-Q1',3.12,-40,105,1.8,'ISO 11452-4 Class 3','TI','MIPI CSI-2'),(3,'AD9671',12.5,-40,85,2.5,'CISPR 25 Class 2','ADI','LVDS'),(4,'AD9251',6.25,-40,85,3.3,'ISO 11452-6 Class 3','ADI','MIPI CSI-2'),(5,'MAX96713',6,-40,105,3.3,'CISPR 25 Class 2','Maxim Integrated','FPD_LINK III'),(6,'MAX9295',3,-40,85,1.8,'ISO 11452-2 Class 2','Maxim Integrated','LVDS'),(7,'RAA279951',5,-40,105,3.3,'CISPR 25 Class 3','Renesas','MIPI CSI-2'),(8,'S32V234配套Deserializer',4,-40,85,2.5,'ISO 11452-3 Class 2','NXP','LVDS'),(9,'NCV7686',3.12,-40,105,3.3,'CISPR 25 Class 2','ON-Semi','LVDS'),(10,'STDP702',6,-40,105,1.8,'ISO 11452-2 Class 3','ST','PCIe');
/*!40000 ALTER TABLE `deserializers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `digitalmap`
--

DROP TABLE IF EXISTS `digitalmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `digitalmap` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Map_Type` varchar(45) NOT NULL,
  `Map_Protocol` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_digitalmap_suppliers1_idx` (`Supplier_Name`),
  KEY `fk_digitalmap_maptype_enum1_idx` (`Map_Type`),
  KEY `fk_digitalmap_mapprotocol_enum1_idx` (`Map_Protocol`),
  CONSTRAINT `fk_digitalmap_mapprotocol_enum1` FOREIGN KEY (`Map_Protocol`) REFERENCES `mapprotocol_enum` (`Protocol`),
  CONSTRAINT `fk_digitalmap_maptype_enum1` FOREIGN KEY (`Map_Type`) REFERENCES `maptype_enum` (`Type`),
  CONSTRAINT `fk_digitalmap_suppliers1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `digitalmap`
--

LOCK TABLES `digitalmap` WRITE;
/*!40000 ALTER TABLE `digitalmap` DISABLE KEYS */;
INSERT INTO `digitalmap` VALUES (1,'Tecent SD+','Tecent','ADAS','API'),(2,'Navinfo HD','Navinfo','HD','ADASISV3'),(3,'HERE_ADAS_MAP','HERE','ADAS','ADASISV2'),(4,'Tecent HD Map','Tecent','HD','ADASISV3');
/*!40000 ALTER TABLE `digitalmap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain_enum`
--

DROP TABLE IF EXISTS `domain_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domain_enum` (
  `VALUE` varchar(45) NOT NULL,
  PRIMARY KEY (`VALUE`),
  UNIQUE KEY `DOMAIN_VALUE_UNIQUE` (`VALUE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain_enum`
--

LOCK TABLES `domain_enum` WRITE;
/*!40000 ALTER TABLE `domain_enum` DISABLE KEYS */;
INSERT INTO `domain_enum` VALUES ('ADAS'),('ADAS+IVI'),('IVI'),('VEH');
/*!40000 ALTER TABLE `domain_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecu`
--

DROP TABLE IF EXISTS `ecu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecu` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `suppliers_Name` varchar(45) NOT NULL,
  `Bsp_Name` varchar(45) NOT NULL,
  `middlewaretype_enum_Type` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_ecu_suppliers1_idx` (`suppliers_Name`),
  KEY `fk_ecu_bsp1_idx` (`Bsp_Name`),
  KEY `fk_ecu_middlewaretype_enum1_idx` (`middlewaretype_enum_Type`),
  CONSTRAINT `fk_ecu_bsp1` FOREIGN KEY (`Bsp_Name`) REFERENCES `bsp` (`Name`),
  CONSTRAINT `fk_ecu_middlewaretype_enum1` FOREIGN KEY (`middlewaretype_enum_Type`) REFERENCES `middlewaretype_enum` (`Type`),
  CONSTRAINT `fk_ecu_suppliers1` FOREIGN KEY (`suppliers_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecu`
--

LOCK TABLES `ecu` WRITE;
/*!40000 ALTER TABLE `ecu` DISABLE KEYS */;
INSERT INTO `ecu` VALUES (1,'Valeo Smart Cam Gen 2','Valeo','Example2','AUTOSAR CP RTE'),(2,'V Parking U5','Valeo','Example2','AUTOSAR AP RTE'),(3,'VALEO_VSS_360_GEN_1','Valeo','Example2','AUTOSAR CP RTE');
/*!40000 ALTER TABLE `ecu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecu_input`
--

DROP TABLE IF EXISTS `ecu_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecu_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `system_solution_ID` int NOT NULL,
  `ECU_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_ecu_input_system_solution1_idx` (`system_solution_ID`),
  KEY `fk_ecu_input_ecu1_idx` (`ECU_Name`),
  CONSTRAINT `fk_ecu_input_ecu1` FOREIGN KEY (`ECU_Name`) REFERENCES `ecu` (`Name`),
  CONSTRAINT `fk_ecu_input_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecu_input`
--

LOCK TABLES `ecu_input` WRITE;
/*!40000 ALTER TABLE `ecu_input` DISABLE KEYS */;
INSERT INTO `ecu_input` VALUES (1,3,'VALEO_VSS_360_GEN_1'),(3,4,'Valeo Smart Cam Gen 2'),(4,4,'V Parking U5');
/*!40000 ALTER TABLE `ecu_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecu_os_input`
--

DROP TABLE IF EXISTS `ecu_os_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecu_os_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ecu_ID` int NOT NULL,
  `Os_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_ecu_os_input_ecu1_idx` (`ecu_ID`),
  KEY `fk_ecu_os_input_os1_idx` (`Os_Name`),
  CONSTRAINT `fk_ecu_os_input_ecu1` FOREIGN KEY (`ecu_ID`) REFERENCES `ecu` (`ID`),
  CONSTRAINT `fk_ecu_os_input_os1` FOREIGN KEY (`Os_Name`) REFERENCES `os` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecu_os_input`
--

LOCK TABLES `ecu_os_input` WRITE;
/*!40000 ALTER TABLE `ecu_os_input` DISABLE KEYS */;
INSERT INTO `ecu_os_input` VALUES (1,1,'Autosar OS'),(2,3,'Autosar OS');
/*!40000 ALTER TABLE `ecu_os_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecu_storage_input`
--

DROP TABLE IF EXISTS `ecu_storage_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecu_storage_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ecu_ID` int NOT NULL,
  `Storage_Name` varchar(100) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_ecu_storage_input_ecu1_idx` (`ecu_ID`),
  KEY `fk_ecu_storage_input_storage_unit1_idx` (`Storage_Name`),
  CONSTRAINT `fk_ecu_storage_input_ecu1` FOREIGN KEY (`ecu_ID`) REFERENCES `ecu` (`ID`),
  CONSTRAINT `fk_ecu_storage_input_storage_unit1` FOREIGN KEY (`Storage_Name`) REFERENCES `storage_unit` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecu_storage_input`
--

LOCK TABLES `ecu_storage_input` WRITE;
/*!40000 ALTER TABLE `ecu_storage_input` DISABLE KEYS */;
INSERT INTO `ecu_storage_input` VALUES (1,1,'Kioxia THGBMFG9C1LBAIL'),(2,3,'Micron N25Q064A13ESF40F');
/*!40000 ALTER TABLE `ecu_storage_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ethernet_switch`
--

DROP TABLE IF EXISTS `ethernet_switch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ethernet_switch` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_ethernet_switch_suppliers1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_ethernet_switch_suppliers1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ethernet_switch`
--

LOCK TABLES `ethernet_switch` WRITE;
/*!40000 ALTER TABLE `ethernet_switch` DISABLE KEYS */;
INSERT INTO `ethernet_switch` VALUES (1,'88Q5072','Marvell'),(2,'88Q5152','Marvell');
/*!40000 ALTER TABLE `ethernet_switch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ethernet_switch_input`
--

DROP TABLE IF EXISTS `ethernet_switch_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ethernet_switch_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `ethernet_switch_Name` varchar(45) NOT NULL,
  `Switch_number` int DEFAULT NULL,
  `ecu_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_ethernet_switch_input_ethernet_switch1_idx` (`ethernet_switch_Name`),
  KEY `fk_ethernet_switch_input_ecu1_idx` (`ecu_ID`),
  CONSTRAINT `fk_ethernet_switch_input_ecu1` FOREIGN KEY (`ecu_ID`) REFERENCES `ecu` (`ID`),
  CONSTRAINT `fk_ethernet_switch_input_ethernet_switch1` FOREIGN KEY (`ethernet_switch_Name`) REFERENCES `ethernet_switch` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ethernet_switch_input`
--

LOCK TABLES `ethernet_switch_input` WRITE;
/*!40000 ALTER TABLE `ethernet_switch_input` DISABLE KEYS */;
INSERT INTO `ethernet_switch_input` VALUES (1,'88Q5072',1,0);
/*!40000 ALTER TABLE `ethernet_switch_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `euf`
--

DROP TABLE IF EXISTS `euf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `euf` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Description` text,
  `FUSA` varchar(45) NOT NULL,
  `SAE` varchar(45) NOT NULL,
  `Full_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `EUF_ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_euf_fusa_enum1_idx` (`FUSA`),
  KEY `fk_euf_sae_enum1_idx` (`SAE`),
  CONSTRAINT `fk_euf_fusa_enum1` FOREIGN KEY (`FUSA`) REFERENCES `fusa_enum` (`LEVEL`),
  CONSTRAINT `fk_euf_sae_enum1` FOREIGN KEY (`SAE`) REFERENCES `sae_enum` (`LEVEL`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `euf`
--

LOCK TABLES `euf` WRITE;
/*!40000 ALTER TABLE `euf` DISABLE KEYS */;
INSERT INTO `euf` VALUES (1,'ACC','This is the Adaptive Cruise Control Functinonality','ASIL_B','L1','Adaptive Cruise Control'),(2,'LKA','This is a user function which actively control the vehicle\'s lateral motion to avoide vechile from driving out of lane','QM','L0','Lane Keep Assist'),(3,'TSR','As a core ADAS feature, TSR uses a front-facing camera and AI algorithms to real-time detect traffic signs (e.g., speed limits, prohibitions, warnings) per traffic standards. It displays recognized info on the dashboard or HUD, alerts drivers to overspeeding, and collaborates with ACC/ISA for smarter cruising. While enhancing driving safety and compliance by reducing distractions, TSR is auxiliary—drivers must remain attentive, as harsh weather or obscured signs may affect accuracy.','QM','L0','Traffic Sign Recognition'),(4,'TLR','TLR is an ADAS feature using onboard cameras and AI algorithms to detect and interpret traffic light signals in real-time. The system identifies red, yellow, and green lights, displays their status on the dashboard/HUD, and provides visual/auditory alerts. It enhances safety by reducing driver distraction and enables smarter decisions at intersections. TLR also integrates with ACC and navigation for optimal speed adjustments and green wave predictions. Note: performance may degrade in poor weather or with obstructed lights—always remain attentive while driving.','QM','L0','Traffic Light Recognition'),(5,'ISA','XXXXXXX','QM','L0','Intelligent Speed Assist'),(6,'AHB','AHB is an ADAS feature that automatically switches between high and low beams to maximize visibility while preventing glare for other road users. Using a windshield-mounted camera, it detects oncoming vehicles\' headlights or preceding vehicles\' taillights and intelligently toggles between beam modes at speeds above 30km/h.','QM','L0','Adaptive High Beam'),(8,'EDR','Known as a car’s \"black box,\" EDR is an in-vehicle system that monitors and records critical vehicle data before, during, and after a collision or severe event (e.g., hard braking). Triggered by sudden acceleration changes, it captures speed, brake application, airbag deployment, throttle position, and steering angle for 5–20 seconds pre-event. Mandated in most regions (China, EU, US), the data aids accident investigation, liability determination, and vehicle safety improvements. It’s non-volatile, ensuring data retention even after power loss—purely objective for post-incident analysis.','QM','L0','Event Data Recorder'),(9,'ADB','ADB is an advanced ADAS lighting feature using matrix LED headlights and camera-based detection. It intelligently dims specific light segments to avoid dazzling oncoming/preceding vehicles, while keeping other areas illuminated with high beams. This maintains optimal nighttime visibility without compromising other road users’ safety, eliminating the \"on-off\" gap of basic AHB. ADB enhances driving comfort and reduces fatigue, typically available on mid-to-high-end vehicles. Note: It’s a driver aid—remain attentive to weather and road conditions.','QM','L0','Adaptive Driving Beam'),(10,'FCW','Automatic Emergency Braking (AEB) employs radar, lidar, and cameras to detect potential collisions. When it senses a threat and the driver doesn\'t respond, it first warns via visual and auditory signals. If there\'s no action, AEB automatically applies brakes, reducing collision severity or preventing crashes, thus enhancing road safety.','QM','L0','Front Collision Warning'),(11,'LDW','Lane Departure Warning function is to provide alert information to the driver while the vehicle is crossing the lane markers unintentionally','QM','L0','Lane Departure Warning'),(12,'SLCA','The ADAS system controls the vehicle\'s longitudianl motion and lateral motion to perform lane change manouver under driver\'s triggering','QM','L2','Semi Automatic Lane Change Assist'),(13,'H-NOP_Lite','NOP(Navigation on Pilot) is a integrated L2+ function which could provide Automated Driving Assist Under driver’s supervision (Hands On + Eyes On) within the Structural Road (Highway or Urban Express) from point A and point B (start point and destination defined by user) at full speed range (0-130 kph).\n\nNOP function including longitudinal, lateral control of the vehicle, and lane change assist (Full automatic, driver triggered and system suggested), which helps the driver to perform Automatic overtaking, Highway connections on top of the HWA functions today.','QM','L2+','Highway Navigation On Pilot Lite'),(14,'H-NOP_Full','NOP(Navigation on Pilot) is a integrated L2+ function which could provide Automated Driving Assist Under driver’s supervision (Hands On + Eyes On) within the Structural Road (Highway or Urban Express) from point A and point B (start point and destination defined by user) at full speed range (0-130 kph).\n\nNOP function including longitudinal, lateral control of the vehicle, and lane change assist (Full automatic, driver triggered and system suggested), which helps the driver to perform Automatic overtaking, Highway connections on top of the HWA functions today.','ASIL_B','L2+','Highway Navigation On Pilot Full.'),(15,'U-NOP','As an advanced ADAS feature, Urban NOP enables semi-autonomous driving in urban scenarios via navigation integration and sensor fusion. It autonomously handles following, lane-keeping, turns, and obstacle avoidance on urban arterials, adapting to traffic lights and congestion. Drivers remain responsible—must take over promptly when prompted. It enhances driving convenience while reducing urban commuting fatigue.','QM','L2++','Urban Navigation On Pilot'),(16,'TJC','TJC is a Level 3 autonomous driving feature designed for highway and motorway traffic jams, operating at speeds up to 60-80 km/h. As a \"Conditional Automation\" system, it allows drivers to fully disengage from driving tasks (both hands off the wheel and eyes off the road) while the vehicle autonomously handles acceleration, braking, lane keeping, and obstacle avoidance in congested conditions.','QM','L3','Traffic Jam Chauffeur'),(17,'D2D','This is a integrated functionality which allows the vehicle to driver from point A to point B without differentiating the scenarios, wheather is parking scenarsio or driving scenarios, whether is in public road or in parking garage.','QM','L2++','Door-to-Door'),(19,'BSD','The Blind Spot Detection function is designed to give driver indication or alert while traffic participant enters in the blind area of the driver by monitoring the surrondings of vechiel','QM','L0','Blind Spot Detection'),(20,'LCA','The Lane Change Assist function is designed to give driver indication or alert while the system detect collision risk if ego vehicle tries to perform a lane change manouver by scanning the environment on the rear end of the ego','QM','L0','Lane Change Assist'),(21,'DOW','DOW (Door Opening Warning) is an ADAS feature that detects rear-approaching vehicles, cyclists, or pedestrians when a vehicle is parked. Via sensors (radar/camera), it triggers visual/audio alerts to warn occupants, preventing collisions caused by sudden door opening. It enhances safety for vulnerable road users and reduces parking-related accidents, a key addition to modern vehicle safety systems.','QM','L0','Door Opening Warning'),(22,'RCW','RCW is an ADAS feature that uses rear-mounted radars/cameras to monitor following vehicles. It detects abnormal speed or distance, triggering visual/audio alerts to warn the driver of potential rear-end collisions. This function enhances driving safety by prompting proactive precautions, especially in heavy traffic or low-visibility conditions.','QM','L0','Rear Collision Warning'),(23,'FCTA','FCTA (Forward Collision Threat Alert) is an ADAS function that utilizes front sensors (radar/camera) to track preceding vehicles, pedestrians, or obstacles. It calculates collision risk based on speed and distance, issuing timely alerts to the driver. By enabling early reaction, it effectively reduces forward collision risks, a core safety feature for modern vehicles.','QM','L0','Front Crossing Traffic Warning'),(24,'RCTA','RCTA (Rear Cross Traffic Alert) is an ADAS feature for reversing scenarios. Using rear/side radars, it detects cross-approaching vehicles, cyclists, or pedestrians from blind spots. It triggers clear alerts to warn the driver, preventing collisions during reversing in parking lots or narrow roads, significantly improving low-speed maneuvering safety.','QM','L0','Rear Cross Traffic Alert'),(25,'AEB','Automatic Emergency Braking (AEB) employs radar, lidar, and cameras to detect potential collisions. When it senses a threat and the driver doesn\'t respond, it first warns via visual and auditory signals. If there\'s no action, AEB automatically applies brakes, reducing collision severity or preventing crashes, thus enhancing road safety.','ASIL_B','L0','Automatic Emergency Braking'),(26,'ELKA','The Emergency Lane Keep Assist function helps the vehicle return to its own lane in the RoadEdge/Oncoming/Overtaking/VRU situations when the vehicle is leaving the lane unintentionally','QM','L0','Emergency Lane Keep Assist'),(27,'ESS','ESS (Emergency Steering Assist) is an ADAS feature. Using front sensors (radar/camera), it detects imminent forward collisions when braking alone is insufficient. It provides gentle steering assistance to help the driver avoid obstacles while maintaining vehicle stability. This function enhances collision avoidance capability, especially in emergency scenarios, significantly improving driving safety.','QM','L0','Emergency Steering Assist'),(28,'AES','AES (Autonomous Emergency Steering) is an advanced ADAS feature. Using front sensors (radar/camera), it detects forward obstacles where braking alone can’t avoid collision. It autonomously applies precise steering to navigate around hazards while maintaining stability, without driver input. This function enhances emergency collision avoidance, significantly improving safety for occupants and vulnerable road users.','QM','L0','Autonomous Emergency Steering'),(29,'FCTB','FCTB is an advanced ADAS function. Using front sensors (radar/camera), it detects forward obstacles (vehicles, pedestrians) and assesses collision risk. When warnings fail to prompt driver action, it autonomously applies braking to mitigate or avoid impacts, enhancing forward driving safety significantly.','QM','L0','Front Crossing Traffic Braking'),(30,'RCTB','RCTB is a low-speed ADAS feature for reversing. Via rear/side radars, it detects cross-approaching traffic or obstacles. Beyond alerts, it automatically applies braking to prevent collisions if the driver doesn’t respond, critical for safe reversing in parking lots or busy areas.','QM','L0','Rear Cross Traffic Braking'),(31,'LCC','The Lane Centering Control is design to provide continous lateral vehicle control for the driver to keep the ego vehicle within the lanes with the help of detected lane marker','QM','L1','Lane Centering Control'),(32,'TJA','Traffic Jam Assist is combined function that provides continous longitudianl control as ACC function and also lateral control which includes LCC function but also lateral control based on target vehicle trajectory within the speed range from 0 kph to 60 kph.','QM','L2','Traffic Jam Assist'),(33,'HWA','HighWay Assist is combined function that provides continous longitudianl control as ACC function and also lateral control which as LCC within the speed range of 0 - 130 kph it also includes automatic SLCA function on the under defined ODD within the speed range of 45 - 130 kph','QM','L2','Highway Assist'),(34,'Urban_Commute','City Memory Driving is an L2+ ADAS feature, also called \"Commute NOA\". It learns fixed routes (e.g., commutes) via multi-sensors, building a memory map. It enables point-to-point autonomous navigation, handling traffic lights, obstacle avoidance, and lane changes. Supporting seamless human-machine collaboration, it simplifies daily driving and enhances safety for urban commuters.','QM','L2++','Urban_Commute'),(35,'HC','Highchauffeur is an L3-level autonomous driving feature for highways/urban expressways. Powered by multi-sensor fusion and AI, it takes over acceleration, braking, and steering, handling complex traffic scenarios independently. Drivers remain on standby to resume control when alerted. It balances automation convenience and safety, redefining semi-autonomous driving experiences for modern vehicles.','QM','L3','Highway chauffeur');
/*!40000 ALTER TABLE `euf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `euf_regulation_input`
--

DROP TABLE IF EXISTS `euf_regulation_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `euf_regulation_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `euf_ID` int NOT NULL,
  `Regulation_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_euf_regulation_input_euf1_idx` (`euf_ID`),
  KEY `fk_euf_regulation_input_regulation1_idx` (`Regulation_Name`),
  CONSTRAINT `fk_euf_regulation_input_euf1` FOREIGN KEY (`euf_ID`) REFERENCES `euf` (`ID`),
  CONSTRAINT `fk_euf_regulation_input_regulation1` FOREIGN KEY (`Regulation_Name`) REFERENCES `regulation` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `euf_regulation_input`
--

LOCK TABLES `euf_regulation_input` WRITE;
/*!40000 ALTER TABLE `euf_regulation_input` DISABLE KEYS */;
INSERT INTO `euf_regulation_input` VALUES (1,25,'FMVSS-127'),(2,25,'AIS-185'),(3,25,'UN-R152'),(4,25,'KMVSS-Article-90-3'),(6,25,'ADR-98'),(7,25,'GB/T-39901'),(8,5,'(EU)-2021/1958'),(9,5,'GB/T-44433-2024'),(10,1,'UN-R13H'),(11,1,'NCAP'),(12,1,'GB/T-20608-2006'),(13,1,'GB-21670-2008'),(14,11,'UN-R130'),(15,11,'ISO-17361:2017'),(16,11,'GB/T-26773-2011'),(17,11,'AIS-188'),(18,11,'ADR-99'),(19,2,'UN-R79'),(20,2,'GB/T-39323-2020'),(21,2,'AIS-193'),(22,26,'(EU)-2021/646'),(23,26,'UN-R79'),(24,26,'AIS-191'),(25,26,'ADR-107/00'),(26,27,'UN-R79'),(27,28,'UN-R79'),(28,12,'UN-R79'),(29,31,'UN-R79'),(30,6,'UN-R48'),(31,6,'FMVSS-108'),(32,6,'Resolution-CONTRAN-970/2022'),(33,6,'ADR-45/01'),(34,6,'UN-R48'),(35,6,'FMVSS-108'),(36,6,'Resolution-CONTRAN-970/2022'),(37,6,'ADR-45/01'),(38,8,'UN-R160'),(39,8,'GB-39732-2020'),(40,8,'AIS-192'),(41,14,'UN-R171'),(42,14,'GB/T-Multi-lane-manoeuver'),(43,13,'GB/T-Multi-lane-manoeuver'),(44,13,'UN-R171'),(45,15,'UN-R171'),(46,15,'GB 7258-202X'),(47,17,'UN-R171'),(48,17,'GB 7258-202X'),(49,34,'UN-R171'),(50,34,'GB 7258-202X'),(51,16,'UN-R157'),(52,35,'UN-R157'),(57,8,'UN-R157/VMAD');
/*!40000 ALTER TABLE `euf_regulation_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forum_data`
--

DROP TABLE IF EXISTS `forum_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_data` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Post_Title` text,
  `Post_Content` text,
  `Poster_Name` varchar(45) DEFAULT NULL,
  `Post_View_Count` varchar(45) DEFAULT NULL,
  `Post_Like_Count` varchar(45) DEFAULT NULL,
  `Post_Category` varchar(45) DEFAULT NULL,
  `Post_Time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_data`
--

LOCK TABLES `forum_data` WRITE;
/*!40000 ALTER TABLE `forum_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `forum_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `function_features`
--

DROP TABLE IF EXISTS `function_features`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `function_features` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Description` text,
  `euf_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_function_features_euf1_idx` (`euf_ID`),
  CONSTRAINT `fk_function_features_euf1` FOREIGN KEY (`euf_ID`) REFERENCES `euf` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `function_features`
--

LOCK TABLES `function_features` WRITE;
/*!40000 ALTER TABLE `function_features` DISABLE KEYS */;
INSERT INTO `function_features` VALUES (1,'ACC-Basic','This the Basic feature of ACC function that controls the vehicle\'s longitudinal motion status according to the driver\'s input of set speed or the distance between ego vehicle and target vehicle.',1),(2,'ACC-Stop&Go','This feautre belongs to ACC functionality which enables the system to control the vehicle\'s dynamic motion status to stop and hold standstill then enables the vehicle to start.',1),(3,'TSR-Basic','This the basci feature of TSR function which captured and recognized the traffic signs and provide speed limit informations to the driver',3),(4,'TLR-Basic','This the main feature of TLF funationly which capture and recognize the traffic light and provides its semantic information.',4),(5,'ISA-Basic','This the main feature of the ISA functionality',5),(6,'AHB-Basic','This is the main feature of AHB functionality',6),(8,'EDR-Basic','This the main feature for EDR functionality',8),(9,'ADB-Basic','This is the main feature of ADB functionality',9),(10,'FCW-Basic','This is the main feature of FCW functionality',10),(11,'LDW-Basic','This is the main featrue for LDW funcationality',11),(12,'SLCA-Basic','This is the main feature for SLCA functionality',12),(13,'H-NOP_Lite-Basic','placeholders',13),(14,'H-NOP_Lite-MRM - SIL','placeholders',13),(15,'H-NOP_Full-MRM - SIL','XXXXXXX',14),(16,'H-NOP_Full-MRM - SST','XXXXX',14),(17,'U-NOP-Basic','XXXXXXXXXXXXXXX',15),(18,'TJC-Basic','This is the main fucntion for TJC functionality',16),(19,'D2D-Basic','This the only feature for D2D functionality',17),(20,'H-NOP_Full - AOT','This the automatic overtaking feature from function NOP which the system detecte the travel efficiency of different lanes and the surrongding environment situation to determine wether a lane change is needed to gain higher traval efficiency and wether the envinroment allows a safe lane change and eventually propose and execute a lane change manouver.',14),(24,'BSD-Basic','This is the main functionality of BSD function',19),(25,'LCA-Basic','This the main feature for the parent function LCA',20),(26,'DOW-Basic','This the main feature for the parent function DOW',21),(27,'RCW-Basic','This the main feature for the parent function RCW',22),(28,'FCTA-Basic','This the main feature for the parent function FCTA',23),(29,'RCTA-Basic','This the main feature for the parent function RCTA',24),(30,'AEB-CarToCar','This the main feature for the parent function AEB',25),(32,'AEB-VRU','This the feature of AEB function where the system take braking actions to imminent collision risk against VRU',25),(33,'ACC- Overtaking','placeholder',1),(34,'LKA-Basic','This the main feature for the parent function LKA',2),(35,'ELKA-Roadedge','This is the feature of ELKA where the system take steering actions to the roadedge on top of LKA scenarios',26),(36,'ELKA-Oncoming Vehicle','This is the feature of ELKA where the system takes steering actions to avoid oncoming vehicles on top of the LKA scenarios',26),(37,'ELKA-Overtaking Objects','This is theThis is the feature of ELKA where the system takes steering actions to avoid overtaking vehicles on top of the LKA scenarios',26),(38,'ESS-Basic','This is the main feature for the parent function ESS',27),(39,'AES-Basic','This is the main feature of the parent function AES',28),(41,'FCTB-Basic','This is the main feature of parent function FCTB',29),(42,'RCTB-Basic','This is the main feature of parent function RCTB',30),(43,'LCC-Basic','This is the main feature of parent function LCC',31),(44,'LCC_Shift in Lane','This is the feature of LCC where the system take action to the oversize vehicle in the adjacent lane and create automatically lateral distance for comfort consideration',31),(45,'TJA-Basic','This the main feature of the parent fucntion TJA',32),(46,'HWA-Basic','This the main feature of the parent fucntion Basic',33),(47,'HWA-Driver In Loop','This is the feature where the system detect and monitor the driver\'s in loop status and give warning or abort the function when conditions are met',33),(48,'H-NOP_Full-Basic','This is the main feature of the parent function H-NOP_Full-Basic',14),(49,'Urban Commute-Basic','This the main feature of the parent function Urban Commute',34),(50,'Urban Commute-MultiMap stiching','This the feature of Urban Commute where the system takes and merge the learning results from different leanring phase then to enhanced the ODD of the function',34),(51,'HC-Basic','This the main feature of the parent function HC',35);
/*!40000 ALTER TABLE `function_features` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fusa_enum`
--

DROP TABLE IF EXISTS `fusa_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fusa_enum` (
  `LEVEL` varchar(45) NOT NULL,
  PRIMARY KEY (`LEVEL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fusa_enum`
--

LOCK TABLES `fusa_enum` WRITE;
/*!40000 ALTER TABLE `fusa_enum` DISABLE KEYS */;
INSERT INTO `fusa_enum` VALUES ('ASIL_A'),('ASIL_B'),('ASIL_C'),('ASIL_D'),('QM');
/*!40000 ALTER TABLE `fusa_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_sensors`
--

DROP TABLE IF EXISTS `image_sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_sensors` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Resolution` int DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Pixel_Size` float DEFAULT NULL,
  `Frame_Rate` int DEFAULT NULL,
  `Dynamic_Range` float DEFAULT NULL,
  `Spectral_Range_Min` float DEFAULT NULL,
  `Spectral_Range_Max` float DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `NAME_INDEX` (`Name`),
  KEY `fk_Image_sensors_suppliers_enum1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_Image_sensors_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_sensors`
--

LOCK TABLES `image_sensors` WRITE;
/*!40000 ALTER TABLE `image_sensors` DISABLE KEYS */;
INSERT INTO `image_sensors` VALUES (1,'1H1',8,'QualComm',NULL,NULL,NULL,NULL,NULL),(2,'IMX728',8,'Sony',1.4,60,140,400,1050),(3,'ISX031',5,'Sony',1.6,30,130,400,1000),(4,'IMX623',8,'Sony',1.6,60,138,400,1050),(5,'IMX620',8,'Sony',1.6,60,140,400,1050),(6,'IMX735',12,'Sony',1.4,30,144,400,1050),(7,'IMX490',5,'Sony',1.6,60,132,400,1050),(8,'AR0820',8,'ON-Semi',1.4,60,120,400,1000),(9,'AR0234',2,'ON-Semi',3,60,110,400,1000),(10,'AR0331',3,'ON-Semi',1.75,30,115,400,950),(11,'OV10640',10,'OmniVision',1,30,130,400,1050),(12,'OV2775',2,'OmniVision',2.8,60,108,400,1000),(13,'OV5695',5,'OmniVision',1.4,60,126,400,1050),(14,'ISOCELL Auto4AC',8,'Samsung',1.5,60,135,400,1050),(15,'ISOCELL Auto2X1',4,'Samsung',2,60,125,400,1000),(16,'ISOCELL Auto1H',12,'Samsung',1.2,30,140,400,1050),(17,'SC8238',8,'SmartSens',1.4,60,130,400,1050),(18,'SC4300',4,'SmartSens',1.6,60,128,400,1000),(19,'SC5300',10,'SmartSens',1.2,30,135,400,1050);
/*!40000 ALTER TABLE `image_sensors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface`
--

DROP TABLE IF EXISTS `interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interface` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Interface_Number` int DEFAULT NULL,
  `Property` varchar(45) DEFAULT NULL,
  `calculator_ID` int NOT NULL,
  `Type` varchar(45) NOT NULL,
  `SubType` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_interface_calculator1_idx` (`calculator_ID`),
  KEY `fk_interface_interface_enum1_idx` (`Type`),
  KEY `fk_interface_interface_enum_sub1_idx` (`SubType`),
  CONSTRAINT `fk_interface_calculator1` FOREIGN KEY (`calculator_ID`) REFERENCES `calculator` (`ID`),
  CONSTRAINT `fk_interface_interface_enum1` FOREIGN KEY (`Type`) REFERENCES `interface_enum` (`TYPE_VALUE`),
  CONSTRAINT `fk_interface_interface_enum_sub1` FOREIGN KEY (`SubType`) REFERENCES `interface_enum_sub` (`SUBTYPE_VALUE`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface`
--

LOCK TABLES `interface` WRITE;
/*!40000 ALTER TABLE `interface` DISABLE KEYS */;
INSERT INTO `interface` VALUES (11,1,'///',1,'USB','USB 3.1'),(12,3,'4 Lanes',1,'VIDEO','MIPI CSI-2(C-PHY)'),(13,1,'4 Lane DSI',1,'VIDEO','MIPI DSI-2'),(14,1,' ',1,'VIDEO','DP'),(15,20,'CAN FD',1,'CAN','CAN_FD'),(16,2,'100Mbps',1,'ETHERNET','RGMII'),(17,11,'Normal SPI',1,'SPI','Dual-SPI'),(18,1,'///',1,'GENERAL','I2C'),(19,1,'///',1,'GENERAL','GPIO'),(20,1,'eMMC 5.1',1,'STORAGE','eMMC'),(21,12,'//',1,'GENERAL','UART'),(22,1,'???',2,'USB','USB 3.1'),(23,1,'???',2,'USB','USB 2.0'),(24,4,'???',2,'VIDEO','MIPI CSI-2(C-PHY)'),(25,8,'CAN FD',2,'CAN','CAN_FD'),(26,1,'100',2,'ETHERNET','RGMII'),(27,1,'???',2,'ETHERNET','SGMII'),(28,1,'SPI',2,'SPI','Octal-SPI'),(29,1,'???',2,'GENERAL','I2C'),(30,2,'UFS 3.1 gear 4',2,'STORAGE','UFS'),(31,1,'eMMC 5.1',2,'STORAGE','eMMC'),(32,1,'64B FIFO',2,'GENERAL','UART'),(33,16,'//',3,'USB','USB 2.0'),(34,1,'1000Mbps',3,'ETHERNET','SGMII'),(35,1,'100Mbps',3,'ETHERNET','HSGMII'),(36,2,'//',3,'FLEXRAY','FLEXRAY'),(37,12,'/',3,'LIN','LIN2.1'),(38,1,'/',3,'SPI','Dual-SPI'),(39,6,'MSPI',3,'SPI','Multi-Master SPI'),(40,1,'YES',3,'GENERAL','I2C'),(41,1,'32ch DMA',3,'STORAGE','DMA'),(42,0,'//',4,'AUDIO','USB 3.1'),(43,0,'D-PHYv1.2',4,'AUDIO','MIPI CSI-2 (D-PHY)'),(44,0,'/',4,'AUDIO','CAN_FD'),(45,0,'//',4,'AUDIO','RGMII'),(46,0,'//',4,'AUDIO','SGMII'),(47,0,'//',4,'AUDIO','Octal-SPI'),(48,10,' ',4,'GENERAL','I2C'),(49,2,'UFS3.1 gear 4',4,'STORAGE','eMMC'),(50,1,'eMMC5.1',4,'STORAGE','eMMC'),(51,1,'////',8,'SPI','Multi-Master SPI'),(52,3,'///',6,'VIDEO','MIPI CSI-2 (D-PHY)'),(53,2,'///',6,'CAN','CAN_FD'),(54,3,'///',7,'ETHERNET','GMII'),(55,0,'///',5,'VIDEO','MIPI CSI-2 (D-PHY)'),(57,2,'llll',5,'USB','USB 3.1'),(58,10,'////',6,'GENERAL','GPIO'),(59,2,'nnn',10,'AUDIO','LVDS'),(60,1,'aaa',10,'SPI','Dual-SPI');
/*!40000 ALTER TABLE `interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface_enum`
--

DROP TABLE IF EXISTS `interface_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interface_enum` (
  `TYPE_VALUE` varchar(45) NOT NULL,
  PRIMARY KEY (`TYPE_VALUE`),
  UNIQUE KEY `INTERFACE_TYPE_VALUE_UNIQUE` (`TYPE_VALUE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface_enum`
--

LOCK TABLES `interface_enum` WRITE;
/*!40000 ALTER TABLE `interface_enum` DISABLE KEYS */;
INSERT INTO `interface_enum` VALUES ('AUDIO'),('CAN'),('ETHERNET'),('FLEXRAY'),('GENERAL'),('LIN'),('SPI'),('STORAGE'),('USB'),('VIDEO');
/*!40000 ALTER TABLE `interface_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface_enum_sub`
--

DROP TABLE IF EXISTS `interface_enum_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interface_enum_sub` (
  `SUBTYPE_VALUE` varchar(45) NOT NULL,
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`SUBTYPE_VALUE`),
  UNIQUE KEY `INTERFACE_SUBTYPE_VALUE_UNIQUE` (`SUBTYPE_VALUE`),
  KEY `fk_interface_enum_sub_interface_enum1_idx` (`Type`),
  CONSTRAINT `fk_interface_enum_sub_interface_enum1` FOREIGN KEY (`Type`) REFERENCES `interface_enum` (`TYPE_VALUE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface_enum_sub`
--

LOCK TABLES `interface_enum_sub` WRITE;
/*!40000 ALTER TABLE `interface_enum_sub` DISABLE KEYS */;
INSERT INTO `interface_enum_sub` VALUES ('I2S','AUDIO'),('CAN_FD','CAN'),('CAN_HS','CAN'),('CAN_LS','CAN'),('GMII','ETHERNET'),('HSGMII','ETHERNET'),('MII','ETHERNET'),('RGMII','ETHERNET'),('RMII','ETHERNET'),('SGMII','ETHERNET'),('TBI','ETHERNET'),('USXGMII','ETHERNET'),('FLEXRAY','FLEXRAY'),('GPIO','GENERAL'),('I2C','GENERAL'),('JTAG','GENERAL'),('PCIe','GENERAL'),('PCle Gen2','GENERAL'),('UART','GENERAL'),('LIN SBC','LIN'),('LIN2.1','LIN'),('LIN2.2','LIN'),('Multi-Channel LIN','LIN'),('Dual-SPI','SPI'),('Multi-Master SPI','SPI'),('Octal-SPI','SPI'),('Quad-SPI','SPI'),('DDR','STORAGE'),('DMA','STORAGE'),('eMMC','STORAGE'),('LPDDR','STORAGE'),('SPI NAND Flash','STORAGE'),('UFS','STORAGE'),('USB 2.0','USB'),('USB 3.0','USB'),('USB 3.1','USB'),('CoaxPress','VIDEO'),('DP','VIDEO'),('eDP','VIDEO'),('FPD_LINK III','VIDEO'),('GMSL','VIDEO'),('LVDS','VIDEO'),('MIPI CSI-2','VIDEO'),('MIPI CSI-2 (D-PHY)','VIDEO'),('MIPI CSI-2(C-PHY)','VIDEO'),('MIPI CSI-3','VIDEO'),('MIPI DSI-2','VIDEO');
/*!40000 ALTER TABLE `interface_enum_sub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_level_enum`
--

DROP TABLE IF EXISTS `ip_level_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ip_level_enum` (
  `LEVEL` varchar(45) NOT NULL,
  PRIMARY KEY (`LEVEL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_level_enum`
--

LOCK TABLES `ip_level_enum` WRITE;
/*!40000 ALTER TABLE `ip_level_enum` DISABLE KEYS */;
INSERT INTO `ip_level_enum` VALUES ('IP54'),('IP67'),('IP68'),('IP6K9K'),('IPX7'),('IPX9K');
/*!40000 ALTER TABLE `ip_level_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issuesandadvice`
--

DROP TABLE IF EXISTS `issuesandadvice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issuesandadvice` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Description` varchar(45) DEFAULT NULL,
  `Create_Time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Email` varchar(45) DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `UserName` varchar(45) DEFAULT NULL,
  `Category` varchar(45) DEFAULT NULL,
  `Last_Modified` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issuesandadvice`
--

LOCK TABLES `issuesandadvice` WRITE;
/*!40000 ALTER TABLE `issuesandadvice` DISABLE KEYS */;
INSERT INTO `issuesandadvice` VALUES (17,'我就试试，嘿嘿','2025-11-21 09:45:47','woshishuanghe@qq.com','suggestion','已采纳','YANG YUQI','general','2025-12-07 04:35:29'),(20,'Hello,大佬。我想看市面上关于域控的主流的系统芯片方案有哪些？要去哪里找','2025-11-21 13:04:21','xiaolan@outlook.com','suggestion','待处理','xiaolan','general',NULL),(21,'1. 初始化页面无法选中和移动传感器 2. 保存的2D图，车模位置不正确','2025-11-21 13:05:12','1273880613@qq.com','issue','处理中','Jiawei_SONG','fov_builder','2025-12-08 07:17:25'),(22,'我试一下第六个你会怎么处理呢？','2025-11-21 14:01:23','xiaolan@outlook.com','suggestion','已拒绝','xiaolan','general','2025-12-01 02:23:24'),(27,'lllll','2025-12-07 15:53:25','1273880613@qq.com','issue','处理中','Jiawei_SONG','产品配置器','2025-12-08 06:14:44'),(28,'3D预览功能无法使用','2025-12-08 06:21:47','1273880613@qq.com','issue','已解决','Jiawei_SONG','环境生成器','2025-12-08 06:47:39'),(29,'服务器无法连接-返回fail-to-fetch','2025-12-10 02:20:20','1273880613@qq.com','issue','已解决','Jiawei_SONG','通用信息','2025-12-10 02:29:12');
/*!40000 ALTER TABLE `issuesandadvice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge`
--

DROP TABLE IF EXISTS `knowledge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knowledge` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Work_ID` int NOT NULL,
  `Knowledge` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_Knowledge_Work1_idx` (`Work_ID`),
  KEY `fk_Knowledge_Knowledge_content1_idx` (`Knowledge`),
  CONSTRAINT `fk_Knowledge_Knowledge_content1` FOREIGN KEY (`Knowledge`) REFERENCES `knowledge_content` (`Name`),
  CONSTRAINT `fk_Knowledge_Work1` FOREIGN KEY (`Work_ID`) REFERENCES `work` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge`
--

LOCK TABLES `knowledge` WRITE;
/*!40000 ALTER TABLE `knowledge` DISABLE KEYS */;
INSERT INTO `knowledge` VALUES (1,1,'ADAS功能介绍'),(2,2,'功能体验通用知识');
/*!40000 ALTER TABLE `knowledge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `knowledge_content`
--

DROP TABLE IF EXISTS `knowledge_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `knowledge_content` (
  `ID` int NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `link` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `nameindex` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `knowledge_content`
--

LOCK TABLES `knowledge_content` WRITE;
/*!40000 ALTER TABLE `knowledge_content` DISABLE KEYS */;
INSERT INTO `knowledge_content` VALUES (1,'ADAS功能介绍','aaaa'),(2,'功能体验通用知识','bbbb');
/*!40000 ALTER TABLE `knowledge_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lens`
--

DROP TABLE IF EXISTS `lens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lens` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) DEFAULT NULL,
  `HFOV` float DEFAULT NULL,
  `VFOV` float DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Resolution` varchar(45) DEFAULT NULL,
  `Sensor_Size_Match` varchar(20) DEFAULT NULL,
  `Depth_Min` float DEFAULT NULL,
  `Depth_Max` float DEFAULT NULL,
  `Lens_Diameter` float DEFAULT NULL,
  `Lens_Element_Count` int DEFAULT NULL,
  `Optical_Structure` varchar(45) DEFAULT NULL,
  `Lens_Material` varchar(50) NOT NULL,
  `Distortion_Rate` float DEFAULT NULL,
  `Lens_Length` float DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `NAMEINDEX` (`Name`),
  KEY `fk_lens_suppliers_enum1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_lens_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lens`
--

LOCK TABLES `lens` WRITE;
/*!40000 ALTER TABLE `lens` DISABLE KEYS */;
INSERT INTO `lens` VALUES (1,'SF811ZG',120,60,'Sunny','8','1/1.8\"',0.3,NULL,16.5,7,'5G2P+1IR','Glass-Plastic Hybrid',-3.8,28.2),(2,'SF816WN',172,125,'Sunny','5','1/2.7\"',0.1,50,14.8,6,'4G2P+1IR','Glass-Plastic Hybrid',-3.5,22.6),(3,'YTOT-MCP308',82,61,'Yutong Jiuzhou','6','1/2.7\"',0.15,NULL,13.2,5,'3G2P+1IR','Glass-Plastic Hybrid+IR',-2.2,24.5),(4,'JZ-M8356',200,200,'Yutong Jiuzhou','10','2/3\"',0.12,0.12,NULL,NULL,'9G','All Glass (Low Dispersion)',-0.008,NULL),(25,'YT-7598-C1',52,30,'WintopLens','2','1/2.7\"',0.2,NULL,14,6,'6G+1IR','All Glass (BK7 Optical Glass)',-5,21),(26,'LC1007D26-02',170,120,'Hsell','8','1/1.8\"',0.1,50,16,7,'4G3P','Glass-Plastic Hybrid',-3.2,24.49),(27,'BT-118C1228MP10',12,9,'XAMV','10','1/1.8\"',0.15,NULL,29,8,'8G','All Glass',0.05,33.5),(28,'RHL120523A6-01',45,34,'Ronghua','5','1/2.7\"',0.1,10,8.5,5,'1GM3P+1IR','Glass-Plastic Hybrid+IR',1.2,7.8),(29,'GMHR2514MCN',60,45,'TowinLens','2','2/3\"',0.25,NULL,32.5,6,'6G','All Glass (High Refractive Index)',-0.003,29),(30,'YT-7591-D1',120,80,'WintopLens','2','1/3\"',0.1,5,12,5,'3G2P+1IR','Glass-Plastic Hybrid+IR',-4,20.4),(31,'L-OFM10062MN',8,6,'Nikon','10','2/3\"',0.05,0.15,45,12,'12G','All Glass (Low Dispersion)',0.01,90),(32,'TS-2722G-A00',110,82,'Tesoo Optical','5','1/2.9\"',0.1,20,12,6,'3G2P+1IR','Glass-Plastic Hybrid+IR',-2,22.4);
/*!40000 ALTER TABLE `lens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lidar`
--

DROP TABLE IF EXISTS `lidar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lidar` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) DEFAULT NULL,
  `Laser_Length` varchar(45) DEFAULT NULL,
  `Laser_Class` varchar(45) DEFAULT NULL,
  `Max_Detection_Range` float DEFAULT NULL,
  `Min_Detection_Range` float DEFAULT NULL,
  `Distance_Resolution` float DEFAULT NULL,
  `Reflection_Resolution` float DEFAULT NULL,
  `Horizontal_FOV` float DEFAULT NULL,
  `Vertical_FOV` float DEFAULT NULL,
  `Horizontal_Resolution` float DEFAULT NULL,
  `Vertical_Resolution` float DEFAULT NULL,
  `Channel_number` int DEFAULT NULL,
  `Point_perScond` float DEFAULT NULL,
  `Scan_Frequency` float DEFAULT NULL,
  `Echo_Type` varchar(45) DEFAULT NULL,
  `Point_Density` float DEFAULT NULL,
  `Length` float DEFAULT NULL,
  `Width` float DEFAULT NULL,
  `Height` float DEFAULT NULL,
  `Size` varchar(45) GENERATED ALWAYS AS (concat(`Length`,_utf8mb4'*',`Width`,_utf8mb4'*',`Height`)) VIRTUAL,
  `Power_Consumption` float DEFAULT NULL,
  `MAX_TEMP` float DEFAULT NULL,
  `MIN_TEMP` float DEFAULT NULL,
  `Working_Tempature` varchar(45) GENERATED ALWAYS AS (concat(`MIN_TEMP`,_utf8mb4'°~',`MAX_TEMP`,_utf8mb4'°')) VIRTUAL,
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_lidar_lidar_enum1_idx` (`Type`),
  KEY `fk_lidar_suppliers_enum1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_lidar_lidar_enum1` FOREIGN KEY (`Type`) REFERENCES `lidar_enum` (`Type`),
  CONSTRAINT `fk_lidar_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lidar`
--

LOCK TABLES `lidar` WRITE;
/*!40000 ALTER TABLE `lidar` DISABLE KEYS */;
INSERT INTO `lidar` (`ID`, `Name`, `Supplier_Name`, `Laser_Length`, `Laser_Class`, `Max_Detection_Range`, `Min_Detection_Range`, `Distance_Resolution`, `Reflection_Resolution`, `Horizontal_FOV`, `Vertical_FOV`, `Horizontal_Resolution`, `Vertical_Resolution`, `Channel_number`, `Point_perScond`, `Scan_Frequency`, `Echo_Type`, `Point_Density`, `Length`, `Width`, `Height`, `Power_Consumption`, `MAX_TEMP`, `MIN_TEMP`, `Type`) VALUES (2,'AT1440','HESAI','905','Class 1',300,1,NULL,NULL,360,40,0.02,0.02,1440,3400,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'MECHANICAL'),(3,'EM4','Robosense','940','Class 1',600,65535,65535,9999,120,27,0.05,0.025,1080,2592,65535,'',65535,100,80,60,65535,65535,65535,'MEMES'),(4,'ATX','HESAI','905','Class 1',230,10,65535,65535,360,40,0.08,0.05,256,384,65535,'',65535,103,103,76,65535,65535,65535,'MEMES'),(5,'D2','HUAWEI','905','Class 1',200,0.1,3,10,120,25,0.25,0.26,96,120,25,'',65535,120,100,90,65535,65535,65535,'MEMES'),(6,'D3','HUAWEI','905','Class 1',250,0.1,2,8,120,30,0.08,0.05,192,384,20,'',65535,103,103,76,65535,65535,65535,'MEMES'),(7,'D3PRO','HUAWEI','905','Class 1',230,0.1,2,8,120,30,0.08,0.05,192,384,20,'',65535,103,103,76,65535,65535,65535,'SOLID-STATE'),(8,'ADS4.0','HUAWEI','1550','Class 1',500,0.05,3,5,120,25,0.05,0.025,65535,180,10,'',65535,45,55,44,65535,65535,65535,'SOLID-STATE');
/*!40000 ALTER TABLE `lidar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lidar_enum`
--

DROP TABLE IF EXISTS `lidar_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lidar_enum` (
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lidar_enum`
--

LOCK TABLES `lidar_enum` WRITE;
/*!40000 ALTER TABLE `lidar_enum` DISABLE KEYS */;
INSERT INTO `lidar_enum` VALUES ('FLASH'),('MECHANICAL'),('MEMES'),('OPA'),('SOLID-STATE');
/*!40000 ALTER TABLE `lidar_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lidar_input`
--

DROP TABLE IF EXISTS `lidar_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lidar_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `system_solution_ID` int NOT NULL,
  `Lidar_Name` varchar(45) NOT NULL,
  `POSITION` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_lidar_input_system_solution1_idx` (`system_solution_ID`),
  KEY `fk_lidar_input_lidar1_idx` (`Lidar_Name`),
  KEY `fk_lidar_input_position_enum1_idx` (`POSITION`),
  CONSTRAINT `fk_lidar_input_lidar1` FOREIGN KEY (`Lidar_Name`) REFERENCES `lidar` (`Name`),
  CONSTRAINT `fk_lidar_input_position_enum1` FOREIGN KEY (`POSITION`) REFERENCES `position_enum` (`POSITION`),
  CONSTRAINT `fk_lidar_input_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lidar_input`
--

LOCK TABLES `lidar_input` WRITE;
/*!40000 ALTER TABLE `lidar_input` DISABLE KEYS */;
/*!40000 ALTER TABLE `lidar_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager_account`
--

DROP TABLE IF EXISTS `manager_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager_account` (
  `ID` int NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  `isAllRight` tinyint DEFAULT NULL,
  `isModification` tinyint DEFAULT NULL,
  `isAdding` tinyint DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_account`
--

LOCK TABLES `manager_account` WRITE;
/*!40000 ALTER TABLE `manager_account` DISABLE KEYS */;
INSERT INTO `manager_account` VALUES (1,'Admin','1234',1,1,1),(2,'Xinyu','dtsite2025',0,1,1),(3,'Jiahua','darker',0,1,1);
/*!40000 ALTER TABLE `manager_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_euf_input`
--

DROP TABLE IF EXISTS `map_euf_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_euf_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Map_Name` varchar(45) NOT NULL,
  `euf_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_map_input_digitalmap1_idx` (`Map_Name`),
  KEY `fk_map_euf_input_euf1_idx` (`euf_ID`),
  CONSTRAINT `fk_map_euf_input_euf1` FOREIGN KEY (`euf_ID`) REFERENCES `euf` (`ID`),
  CONSTRAINT `fk_map_input_digitalmap10` FOREIGN KEY (`Map_Name`) REFERENCES `digitalmap` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_euf_input`
--

LOCK TABLES `map_euf_input` WRITE;
/*!40000 ALTER TABLE `map_euf_input` DISABLE KEYS */;
/*!40000 ALTER TABLE `map_euf_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_input`
--

DROP TABLE IF EXISTS `map_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `map_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `system_solution_ID` int NOT NULL,
  `Map_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_map_input_system_solution1_idx` (`system_solution_ID`),
  KEY `fk_map_input_digitalmap1_idx` (`Map_Name`),
  CONSTRAINT `fk_map_input_digitalmap1` FOREIGN KEY (`Map_Name`) REFERENCES `digitalmap` (`Name`),
  CONSTRAINT `fk_map_input_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_input`
--

LOCK TABLES `map_input` WRITE;
/*!40000 ALTER TABLE `map_input` DISABLE KEYS */;
INSERT INTO `map_input` VALUES (1,3,'HERE_ADAS_MAP'),(2,4,'Tecent HD Map');
/*!40000 ALTER TABLE `map_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mapprotocol_enum`
--

DROP TABLE IF EXISTS `mapprotocol_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mapprotocol_enum` (
  `Protocol` varchar(45) NOT NULL,
  PRIMARY KEY (`Protocol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mapprotocol_enum`
--

LOCK TABLES `mapprotocol_enum` WRITE;
/*!40000 ALTER TABLE `mapprotocol_enum` DISABLE KEYS */;
INSERT INTO `mapprotocol_enum` VALUES ('ADASISV2'),('ADASISV3'),('API'),('REM');
/*!40000 ALTER TABLE `mapprotocol_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maptype_enum`
--

DROP TABLE IF EXISTS `maptype_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maptype_enum` (
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maptype_enum`
--

LOCK TABLES `maptype_enum` WRITE;
/*!40000 ALTER TABLE `maptype_enum` DISABLE KEYS */;
INSERT INTO `maptype_enum` VALUES ('ADAS'),('HD'),('HD Lite'),('REM'),('SD'),('SD+');
/*!40000 ALTER TABLE `maptype_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `memory_unit`
--

DROP TABLE IF EXISTS `memory_unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `memory_unit` (
  `MEMORY_UNIT_ID` int NOT NULL AUTO_INCREMENT,
  `MEMORY_TYPE` varchar(45) NOT NULL,
  `MEMORY_SUBTYPE` varchar(45) DEFAULT NULL,
  `MEMORY_UNIT_NAME` varchar(45) DEFAULT NULL,
  `MEMORY_UNIT_SIZE` varchar(45) DEFAULT NULL,
  `MEMORY_UNIT_UNIT` varchar(45) DEFAULT NULL,
  `calculator_ID` int NOT NULL,
  PRIMARY KEY (`MEMORY_UNIT_ID`),
  UNIQUE KEY `uk_memory_unit_calculator` (`MEMORY_UNIT_ID`,`MEMORY_SUBTYPE`),
  KEY `fk_memory_unit_calculator1_idx` (`calculator_ID`),
  CONSTRAINT `fk_memory_unit_calculator1` FOREIGN KEY (`calculator_ID`) REFERENCES `calculator` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memory_unit`
--

LOCK TABLES `memory_unit` WRITE;
/*!40000 ALTER TABLE `memory_unit` DISABLE KEYS */;
INSERT INTO `memory_unit` VALUES (1,'FLASH','CODE','/','16','MB',0);
/*!40000 ALTER TABLE `memory_unit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metiers`
--

DROP TABLE IF EXISTS `metiers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metiers` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `JD` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metiers`
--

LOCK TABLES `metiers` WRITE;
/*!40000 ALTER TABLE `metiers` DISABLE KEYS */;
INSERT INTO `metiers` VALUES (1,'产品工程师',NULL),(2,'功能开发工程师',NULL),(3,'系统工程师',NULL),(4,'软件开发工程师',NULL),(5,'软件验证工程师',NULL),(6,'系统验证工程师',NULL),(7,'功能架构师',NULL),(8,'系统架构师',NULL),(9,'软件架构师',NULL),(10,'算法开发工程师',NULL);
/*!40000 ALTER TABLE `metiers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `middlewaretype_enum`
--

DROP TABLE IF EXISTS `middlewaretype_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `middlewaretype_enum` (
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`Type`),
  UNIQUE KEY `Type_UNIQUE` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `middlewaretype_enum`
--

LOCK TABLES `middlewaretype_enum` WRITE;
/*!40000 ALTER TABLE `middlewaretype_enum` DISABLE KEYS */;
INSERT INTO `middlewaretype_enum` VALUES ('Apollo Cyber'),('AUTOSAR AP RTE'),('AUTOSAR CP RTE'),('ROS2');
/*!40000 ALTER TABLE `middlewaretype_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `objects`
--

DROP TABLE IF EXISTS `objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `objects` (
  `OBJECT` varchar(45) NOT NULL,
  `NAME` varchar(45) DEFAULT NULL,
  `ID` varchar(45) DEFAULT NULL,
  `CN` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`OBJECT`),
  UNIQUE KEY `OBJECT_UNIQUE` (`OBJECT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `objects`
--

LOCK TABLES `objects` WRITE;
/*!40000 ALTER TABLE `objects` DISABLE KEYS */;
INSERT INTO `objects` VALUES ('calculator','Name','ID','计算芯片'),('camera','Name','ID','摄像头'),('ecu','Name','ID','电控单元'),('euf','Name','ID','用户功能'),('lidar','Name','ID','激光雷达'),('radar','Name','ID','毫米波雷达'),('regulation','Name','ID','法律法规'),('system_solution','Name','ID','系统方案'),('uss','Name','ID','超声波雷达'),('vehiclemodel','Name','ID','车型'),('work','Name','ID','任务列表');
/*!40000 ALTER TABLE `objects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `online_status_enum`
--

DROP TABLE IF EXISTS `online_status_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `online_status_enum` (
  `Status` varchar(45) NOT NULL,
  PRIMARY KEY (`Status`),
  UNIQUE KEY `Status_UNIQUE` (`Status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `online_status_enum`
--

LOCK TABLES `online_status_enum` WRITE;
/*!40000 ALTER TABLE `online_status_enum` DISABLE KEYS */;
INSERT INTO `online_status_enum` VALUES ('新产品上线'),('未上线'),('正式版本上线'),('测试版本上线'),('规划中');
/*!40000 ALTER TABLE `online_status_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `option_enum`
--

DROP TABLE IF EXISTS `option_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `option_enum` (
  `Name` varchar(30) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `option_enum`
--

LOCK TABLES `option_enum` WRITE;
/*!40000 ALTER TABLE `option_enum` DISABLE KEYS */;
/*!40000 ALTER TABLE `option_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `os`
--

DROP TABLE IF EXISTS `os`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `os` (
  `ID` int NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_os_suppliers1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_os_suppliers1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `os`
--

LOCK TABLES `os` WRITE;
/*!40000 ALTER TABLE `os` DISABLE KEYS */;
INSERT INTO `os` VALUES (1,'Linux','OpenSource'),(2,'QNX','Blackberry'),(4,'INTEGRITY RTOS','GreenHills'),(5,'Autosar OS','OpenSource'),(6,'MDC OS','HUAWEI'),(7,'Android','Google'),(8,'DRIVE OS','NVIDIA'),(9,'Apollo OS','Baidu');
/*!40000 ALTER TABLE `os` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `position_enum`
--

DROP TABLE IF EXISTS `position_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `position_enum` (
  `POSITION` varchar(45) NOT NULL,
  PRIMARY KEY (`POSITION`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `position_enum`
--

LOCK TABLES `position_enum` WRITE;
/*!40000 ALTER TABLE `position_enum` DISABLE KEYS */;
INSERT INTO `position_enum` VALUES ('Front_Center'),('Front_inner_left'),('Front_inner_right'),('Front_Left'),('Front_Left_Corner'),('Front_outer_left'),('Front_outer_right'),('Front_Right'),('Front_Right_Corner'),('Front_side_left'),('Front_side_right'),('Left'),('Rear_Center'),('Rear_inner_left'),('Rear_inner_right'),('Rear_Left'),('Rear_Left_Corner'),('Rear_outer_left'),('Rear_outer_right'),('Rear_Right'),('Rear_Right_Corner'),('Rear_side_left'),('Rear_side_right'),('Right'),('Top_Center'),('Top_Left'),('Top_Right');
/*!40000 ALTER TABLE `position_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `power_type`
--

DROP TABLE IF EXISTS `power_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `power_type` (
  `Name` varchar(45) NOT NULL,
  `CN_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Name`),
  UNIQUE KEY `Type_UNIQUE` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `power_type`
--

LOCK TABLES `power_type` WRITE;
/*!40000 ALTER TABLE `power_type` DISABLE KEYS */;
INSERT INTO `power_type` VALUES ('BEV','纯电动汽车'),('EREV','增程式电动汽车'),('FCEV','Hydrogen Fuel Cell Vehicle'),('HEV','Hybrid Electric Vehicle'),('ICE','燃油车'),('PHEV','插电式混合动力汽车');
/*!40000 ALTER TABLE `power_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processor`
--

DROP TABLE IF EXISTS `processor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processor` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Number` int DEFAULT NULL,
  `Name` varchar(45) NOT NULL,
  `Power` float DEFAULT NULL,
  `Lockstep` tinyint DEFAULT NULL,
  `calculator_ID` int NOT NULL,
  `Type` varchar(45) NOT NULL,
  `Unit` varchar(45) GENERATED ALWAYS AS ((case when (`Type` = _utf8mb3'ASIC') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'BPU') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'CODEC') then _utf8mb4'/' when (`Type` = _utf8mb3'CPU') then _utf8mb4'KDMIPS' when (`Type` = _utf8mb3'DECODE') then _utf8mb4'FPS' when (`Type` = _utf8mb3'DOF') then _utf8mb4'MP/s' when (`Type` = _utf8mb3'DSP') then _utf8mb4'GFLOPS' when (`Type` = _utf8mb3'ENCODE') then _utf8mb4'FPS' when (`Type` = _utf8mb3'FPGA') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'GPU') then _utf8mb4'GFLOPS' when (`Type` = _utf8mb3'ISP') then _utf8mb4'MP/s' when (`Type` = _utf8mb3'MMA') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'NPU') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'RPU') then _utf8mb4'KDMIPS' when (`Type` = _utf8mb3'TPU') then _utf8mb4'TOPS' else _utf8mb4'UNIT' end)) STORED,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `PROCESSOR_ID_UNIQUE` (`ID`),
  KEY `fk_processor_calculator1_idx` (`calculator_ID`),
  KEY `fk_processor_processor_enum1_idx` (`Type`),
  CONSTRAINT `fk_processor_calculator1` FOREIGN KEY (`calculator_ID`) REFERENCES `calculator` (`ID`),
  CONSTRAINT `fk_processor_processor_enum1` FOREIGN KEY (`Type`) REFERENCES `processor_enum` (`Type`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processor`
--

LOCK TABLES `processor` WRITE;
/*!40000 ALTER TABLE `processor` DISABLE KEYS */;
INSERT INTO `processor` (`ID`, `Number`, `Name`, `Power`, `Lockstep`, `calculator_ID`, `Type`) VALUES (16,2,'Matrix Multiply Accelerator',16,0,1,'MMA'),(17,3,'Dual Cortex R5F',12,1,1,'RPU'),(18,1,'BXS-64-4',50,0,1,'GPU'),(23,3,'C7x',240,0,1,'DSP'),(24,1,'VPACv3',720,0,1,'ISP'),(25,2,'Cortex-A72@2Ghz',50,0,1,'CPU'),(26,2,'HTP',100,0,2,'NPU'),(27,4,'Cortex-R52',18,1,2,'RPU'),(28,1,'ADRENO_663',15000,0,2,'GPU'),(29,8,'Hexagon Vector eXtensions',100,0,2,'DSP'),(30,1,'Spectra 690 camera ISP',2.4,0,2,'ISP'),(31,1,'Adreno 765 VPU',10000,0,2,'CODEC'),(32,1,'???',240,0,2,'DOF'),(34,8,'Kyro Gen 6',245,0,2,'CPU'),(35,4,'RH850G4MH@400MHz',6.32,1,3,'CPU'),(36,1,'HTP',36,0,4,'NPU'),(37,4,'Cortex-R52',4,1,4,'RPU'),(38,1,'ADRENO',400,0,4,'GPU'),(39,4,'Hexagon Vector eXtension',1,0,4,'DSP'),(40,1,'Spectra 690 camera ISP',2457,0,4,'ISP'),(41,4,'Kryo Gold cores@21.GHz',100,0,4,'CPU'),(42,1,'////',3,0,8,'FPGA'),(43,1,'///',8,0,6,'BPU'),(44,3,'AAAA',30,0,7,'BPU'),(47,1,'NSP',96,0,5,'NPU'),(49,3,'Nan',5,1,10,'FPGA');
/*!40000 ALTER TABLE `processor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processor_enum`
--

DROP TABLE IF EXISTS `processor_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processor_enum` (
  `Type` varchar(45) NOT NULL,
  `UNIT` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Type`),
  UNIQUE KEY `PROCESSOR_TYPE_VALUE_UNIQUE` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processor_enum`
--

LOCK TABLES `processor_enum` WRITE;
/*!40000 ALTER TABLE `processor_enum` DISABLE KEYS */;
INSERT INTO `processor_enum` VALUES ('ASIC','TOPS'),('BPU','TOPS'),('CODEC','/'),('CPU','KDMIPS'),('DECODE','FPS'),('DOF','MP/s'),('DSP','GFLOPS'),('ENCODE','FPS'),('FPGA','TOPS'),('GPU','GFLOPS'),('ISP','MP/s'),('MMA','TOPS'),('NPU','TOPS'),('RPU','KDMIPS'),('TPU','TOPS');
/*!40000 ALTER TABLE `processor_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processor_enum_sub`
--

DROP TABLE IF EXISTS `processor_enum_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processor_enum_sub` (
  `Unit` varchar(45) NOT NULL,
  PRIMARY KEY (`Unit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processor_enum_sub`
--

LOCK TABLES `processor_enum_sub` WRITE;
/*!40000 ALTER TABLE `processor_enum_sub` DISABLE KEYS */;
/*!40000 ALTER TABLE `processor_enum_sub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productfeatures`
--

DROP TABLE IF EXISTS `productfeatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productfeatures` (
  `ID` int unsigned NOT NULL,
  `Function` varchar(45) DEFAULT NULL,
  `Category` varchar(45) DEFAULT NULL,
  `Description` varchar(45) DEFAULT NULL,
  `CN_Name` varchar(45) DEFAULT NULL,
  `Status` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Function_UNIQUE` (`Function`),
  KEY `fk_productfeatures_online_status_enum1_idx` (`Status`),
  CONSTRAINT `fk_productfeatures_online_status_enum1` FOREIGN KEY (`Status`) REFERENCES `online_status_enum` (`Status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productfeatures`
--

LOCK TABLES `productfeatures` WRITE;
/*!40000 ALTER TABLE `productfeatures` DISABLE KEYS */;
INSERT INTO `productfeatures` VALUES (1,'FunctionHall','知识宇宙','提供应用层功能知识','功能星球','正式版本上线'),(2,'SensorHall','知识宇宙','提供传感器知识和数据库','传感器星球','正式版本上线'),(3,'HardWareHall','知识宇宙','提供硬件知识和数据库','硬件星球','正式版本上线'),(4,'Knowledgenet','知识网络','提供硬件知识和数据库','知识网络','正式版本上线'),(5,'RegulationMap','知识宇宙','提供法规相关知识','法规/标准星球','测试版本上线'),(6,'ArchitectureBuild','知识宇宙','提供架构开发的相关知识','架构星球','未上线'),(7,'AdasBenchmark','行业纵横','提供ADAS对标库','车型矩阵','测试版本上线'),(8,'Configurator','智驾军火库','ADAS方案配置工具','产品配置器','测试版本上线'),(9,'RoadBuilder','智驾军火库','环境绘制生成工具','环境生成器','测试版本上线'),(10,'FoV_build','智驾军火库','定制传感器乌龟图','传感器配置器','测试版本上线'),(11,'SensorInspector','智驾军火库','在3D环境下检查传感器视角功能','传感器仿真','新产品上线'),(12,'SimulationPlatform','智驾军火库','完整的仿真平台','仿真平台','未上线'),(13,'PhyArchiTool','智驾军火库','提供生成标准物理架构的工具','物理架构工具','未上线'),(14,'solutionbenchmark','行业纵横','提供ADAS系统方案级别的陈列以及对比','方案矩阵','未上线'),(15,'comparison','行业纵横','提供整车级别,方案级别等的对比工具以及报告输出','方案角斗场','未上线'),(16,'markettrend','行业纵横','提供行业分析','市场通','未上线'),(17,'eco-system net','行业纵横','提供行业内不同公司的合作关系','生态网络','未上线'),(18,'Forum','智驾论坛','提供智能驾驶行业信息交流的空间','智驾论坛','未上线'),(19,'General','通用信息','辅助网站工作','通用信息','未上线');
/*!40000 ALTER TABLE `productfeatures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productversion`
--

DROP TABLE IF EXISTS `productversion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productversion` (
  `VERSION_MAJOR` int NOT NULL,
  `VERSION_MINOR` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`VERSION_MAJOR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productversion`
--

LOCK TABLES `productversion` WRITE;
/*!40000 ALTER TABLE `productversion` DISABLE KEYS */;
/*!40000 ALTER TABLE `productversion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radar`
--

DROP TABLE IF EXISTS `radar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `radar` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Calculator` varchar(45) NOT NULL,
  `Maximum_Instrument_Range` float DEFAULT NULL,
  `Azimuth_FOV_min` float DEFAULT NULL,
  `Azimuth_FOV_max` float DEFAULT NULL,
  `Azimuth_FOV` varchar(45) GENERATED ALWAYS AS (concat(`Azimuth_FOV_min`,_utf8mb4'°~',`Azimuth_FOV_max`,_utf8mb4'°')) VIRTUAL,
  `Elevation_FOV_min` float DEFAULT NULL,
  `Elevation_FOV_max` float DEFAULT NULL,
  `Elevation_FOV` varchar(45) GENERATED ALWAYS AS (concat(`Elevation_FOV_min`,_utf8mb4'°~',`Elevation_FOV_max`,_utf8mb4'°')) VIRTUAL,
  `Type` varchar(45) DEFAULT NULL,
  `Array_Aperture` float DEFAULT NULL,
  `Length` float DEFAULT NULL,
  `Width` float DEFAULT NULL,
  `Height` float DEFAULT NULL,
  `Atenna_Tx_number` int DEFAULT NULL,
  `Atenna_Rx_number` int DEFAULT NULL,
  `Atenna_Info` varchar(45) GENERATED ALWAYS AS (concat(`Atenna_Rx_number`,_utf8mb4'Rx',`Atenna_Tx_number`,_utf8mb4'Tx')) VIRTUAL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_radar_suppliers_enum1_idx` (`Supplier_Name`),
  KEY `fk_radar_calculator1_idx` (`Calculator`),
  CONSTRAINT `fk_radar_calculator1` FOREIGN KEY (`Calculator`) REFERENCES `calculator` (`Name`),
  CONSTRAINT `fk_radar_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radar`
--

LOCK TABLES `radar` WRITE;
/*!40000 ALTER TABLE `radar` DISABLE KEYS */;
INSERT INTO `radar` (`ID`, `Name`, `Supplier_Name`, `Calculator`, `Maximum_Instrument_Range`, `Azimuth_FOV_min`, `Azimuth_FOV_max`, `Elevation_FOV_min`, `Elevation_FOV_max`, `Type`, `Array_Aperture`, `Length`, `Width`, `Height`, `Atenna_Tx_number`, `Atenna_Rx_number`) VALUES (1,'MCR1.2C','Valeo','RH850-U2A16',200,-77.5,77.5,-12.5,12.5,'3D',3.2,83.6,74.4,26.5,4,4),(2,'GEN5','Bosch','RH850-U2A16',NULL,NULL,NULL,NULL,NULL,'3D',3.2,NULL,NULL,NULL,NULL,NULL),(3,'MFR1.2C','Valeo','RH850-U2A16',250,-60,60,-12.5,12.5,'3D',3.2,NULL,NULL,NULL,4,4),(4,'Aptiv Gen7 FLR7','Aptiv','RH850-U2A16',290,-60,60,-15,15,'4D',3.2,65535,65535,65535,4,4),(5,'ARS540','Continental','RH850-U2A16',300,-60,60,-20,20,'4D',3.2,65535,65535,65535,4,4),(6,'Bosch Front Radar Premium','Bosch','RH850-U2A16',302,-60,60,-15,15,'4D',3.2,1,1,1,4,4),(7,'Huawei ASN850','HUAWEI','RH850-U2A16',280,-75,75,-15,15,'4D',3.2,65535,65535,65536,4,4),(8,'ARS620','Continental','RH850-U2A16',250,-60,60,-15,15,'4D',3.2,1,1,1,4,4),(9,'HW5.0 4D Radar','Tesla','RH850-U2A16',300,-60,60,-30,30,'4D',3.2,1,1,1,3,4),(10,'CMR40','NanoRadar','RH850-U2A16',40,-45,45,-15,15,'4D',3.2,1,1,1,3,4),(21,'ARS408-21','Continental','RH850-U2A16',250,-60,60,-15,15,'3D',3.2,NULL,NULL,NULL,2,4),(22,'SRR308-21','Continental','RH850-U2A16',95,-90,90,-40,40,'3D',3.2,NULL,NULL,NULL,2,4),(23,'Front Radar Plus (Gen6 Basic Version)','Bosch','RH850-U2A16',300,-60,60,-15,15,'3D',3.2,NULL,NULL,NULL,2,4),(24,'Bosch Corner Gen4','Bosch','RH850-U2A16',236,-80,80,-15,15,'3D',3.2,NULL,NULL,NULL,2,4),(25,'SRR3','Aptiv','RH850-U2A16',80,-75,75,-20,20,'3D',3.2,NULL,NULL,NULL,2,4),(26,'SRR5','Aptiv','RH850-U2A16',80,-75,75,-20,20,'3D',3.2,NULL,NULL,NULL,2,4),(27,'SRR7710','LimRadar','RH850-U2A16',100,-60,60,-30,30,'3D',3.2,NULL,NULL,NULL,2,4),(28,'CHR77M','Chuhang Technology','RH850-U2A16',200,-60,60,-15,15,'3D',3.2,NULL,NULL,NULL,2,4),(29,'ARS410','Continental','RH850-U2A16',250,-60,60,-15,15,'3D',3.2,NULL,NULL,NULL,2,4),(30,'WLR7720','Wide Area Radar','RH850-U2A16',300,-60,60,-15,15,'3D',3.2,NULL,NULL,NULL,2,4),(31,'I79 4D','MuniuTech','RH850-U2A16',350,-60,60,-15,15,'4D',3.2,1,1,1,4,4),(32,'K77-G3','Aptiv','TDA4-VM-PLUS',220,-60,60,-15,15,'3D',3.2,1,1,1,4,4),(33,'T79-G3','MuniuTech','RH850-U2A16',80,-80,80,-20,20,'3D',3.2,1,1,1,4,4);
/*!40000 ALTER TABLE `radar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radar_input`
--

DROP TABLE IF EXISTS `radar_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `radar_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `system_solution_ID` int NOT NULL,
  `POSITION` varchar(45) NOT NULL,
  `Radar_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_radar_input_system_solution1_idx` (`system_solution_ID`),
  KEY `fk_radar_input_position_enum1_idx` (`POSITION`),
  KEY `fk_radar_input_radar1_idx` (`Radar_Name`),
  CONSTRAINT `fk_radar_input_position_enum1` FOREIGN KEY (`POSITION`) REFERENCES `position_enum` (`POSITION`),
  CONSTRAINT `fk_radar_input_radar1` FOREIGN KEY (`Radar_Name`) REFERENCES `radar` (`Name`),
  CONSTRAINT `fk_radar_input_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radar_input`
--

LOCK TABLES `radar_input` WRITE;
/*!40000 ALTER TABLE `radar_input` DISABLE KEYS */;
INSERT INTO `radar_input` VALUES (1,3,'Front_Center','MCR1.2C'),(2,3,'Front_Right_Corner','MCR1.2C'),(3,3,'Front_Left_Corner','MCR1.2C'),(4,3,'Rear_Left_Corner','MCR1.2C'),(5,3,'Rear_Right_Corner','MCR1.2C'),(7,4,'Front_Left_Corner','MCR1.2C'),(8,4,'Front_Right_Corner','MCR1.2C'),(9,4,'Rear_Left_Corner','MCR1.2C'),(10,4,'Rear_Right_Corner','MCR1.2C'),(11,4,'Front_Center','MFR1.2C');
/*!40000 ALTER TABLE `radar_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name_CN` varchar(45) DEFAULT NULL,
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'欧盟','European Union (EU)'),(2,'UNECE成员国','UNECE Contracting Parties'),(3,'中国','China'),(4,'美国','United States'),(5,'印度','India'),(6,'巴西','Brazil'),(7,'澳大利亚','Australia'),(8,'澳新地区','Australia & New Zealand'),(9,'韩国','South Korea'),(10,'日本','Japan'),(11,'越南','Vietnam');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region_input`
--

DROP TABLE IF EXISTS `region_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Country_ID` int NOT NULL,
  `Region_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_region_input_Country1_idx` (`Country_ID`),
  KEY `fk_region_input_region1` (`Region_Name`),
  CONSTRAINT `fk_region_input_Country1` FOREIGN KEY (`Country_ID`) REFERENCES `country` (`ID`),
  CONSTRAINT `fk_region_input_region1` FOREIGN KEY (`Region_Name`) REFERENCES `region` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=228 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region_input`
--

LOCK TABLES `region_input` WRITE;
/*!40000 ALTER TABLE `region_input` DISABLE KEYS */;
INSERT INTO `region_input` VALUES (63,51,'European Union (EU)'),(64,53,'European Union (EU)'),(65,55,'European Union (EU)'),(66,56,'European Union (EU)'),(67,8,'European Union (EU)'),(68,57,'European Union (EU)'),(69,58,'European Union (EU)'),(70,59,'European Union (EU)'),(71,60,'European Union (EU)'),(72,61,'European Union (EU)'),(73,62,'European Union (EU)'),(74,63,'European Union (EU)'),(75,64,'European Union (EU)'),(76,66,'European Union (EU)'),(77,67,'European Union (EU)'),(78,68,'European Union (EU)'),(79,70,'European Union (EU)'),(80,71,'European Union (EU)'),(81,72,'European Union (EU)'),(82,76,'European Union (EU)'),(83,79,'European Union (EU)'),(84,80,'European Union (EU)'),(85,81,'European Union (EU)'),(86,84,'European Union (EU)'),(87,85,'European Union (EU)'),(88,86,'European Union (EU)'),(89,87,'European Union (EU)'),(94,1,'UNECE Contracting Parties'),(95,49,'UNECE Contracting Parties'),(96,93,'UNECE Contracting Parties'),(97,50,'UNECE Contracting Parties'),(98,94,'UNECE Contracting Parties'),(99,170,'UNECE Contracting Parties'),(100,46,'UNECE Contracting Parties'),(101,182,'Australia & New Zealand'),(102,51,'UNECE Contracting Parties'),(103,47,'UNECE Contracting Parties'),(104,2,'UNECE Contracting Parties'),(105,3,'UNECE Contracting Parties'),(106,149,'UNECE Contracting Parties'),(107,52,'UNECE Contracting Parties'),(108,53,'UNECE Contracting Parties'),(109,150,'UNECE Contracting Parties'),(110,95,'UNECE Contracting Parties'),(111,4,'UNECE Contracting Parties'),(112,54,'UNECE Contracting Parties'),(113,96,'UNECE Contracting Parties'),(114,172,'UNECE Contracting Parties'),(115,5,'UNECE Contracting Parties'),(116,55,'UNECE Contracting Parties'),(117,151,'UNECE Contracting Parties'),(118,173,'UNECE Contracting Parties'),(120,174,'UNECE Contracting Parties'),(121,152,'UNECE Contracting Parties'),(122,106,'UNECE Contracting Parties'),(123,56,'UNECE Contracting Parties'),(124,153,'UNECE Contracting Parties'),(125,8,'UNECE Contracting Parties'),(126,57,'UNECE Contracting Parties'),(127,58,'UNECE Contracting Parties'),(128,155,'UNECE Contracting Parties'),(129,108,'UNECE Contracting Parties'),(130,156,'UNECE Contracting Parties'),(131,59,'UNECE Contracting Parties'),(132,184,'UNECE Contracting Parties'),(133,60,'UNECE Contracting Parties'),(134,61,'UNECE Contracting Parties'),(135,10,'UNECE Contracting Parties'),(136,62,'UNECE Contracting Parties'),(137,115,'UNECE Contracting Parties'),(138,63,'UNECE Contracting Parties'),(139,158,'UNECE Contracting Parties'),(140,160,'UNECE Contracting Parties'),(141,64,'UNECE Contracting Parties'),(142,65,'UNECE Contracting Parties'),(143,11,'UNECE Contracting Parties'),(144,12,'UNECE Contracting Parties'),(145,14,'UNECE Contracting Parties'),(146,66,'UNECE Contracting Parties'),(147,15,'UNECE Contracting Parties'),(148,67,'UNECE Contracting Parties'),(149,161,'UNECE Contracting Parties'),(150,16,'UNECE Contracting Parties'),(151,17,'UNECE Contracting Parties'),(152,18,'UNECE Contracting Parties'),(153,118,'UNECE Contracting Parties'),(154,19,'UNECE Contracting Parties'),(155,20,'UNECE Contracting Parties'),(156,68,'UNECE Contracting Parties'),(157,21,'UNECE Contracting Parties'),(158,121,'UNECE Contracting Parties'),(159,69,'UNECE Contracting Parties'),(160,70,'UNECE Contracting Parties'),(161,71,'UNECE Contracting Parties'),(162,122,'UNECE Contracting Parties'),(163,22,'UNECE Contracting Parties'),(164,72,'UNECE Contracting Parties'),(165,126,'UNECE Contracting Parties'),(166,162,'UNECE Contracting Parties'),(167,74,'UNECE Contracting Parties'),(168,75,'UNECE Contracting Parties'),(169,127,'UNECE Contracting Parties'),(170,76,'UNECE Contracting Parties'),(171,189,'UNECE Contracting Parties'),(172,163,'UNECE Contracting Parties'),(173,130,'UNECE Contracting Parties'),(174,131,'UNECE Contracting Parties'),(175,77,'UNECE Contracting Parties'),(176,78,'UNECE Contracting Parties'),(177,28,'UNECE Contracting Parties'),(178,29,'UNECE Contracting Parties'),(179,164,'UNECE Contracting Parties'),(180,192,'UNECE Contracting Parties'),(181,177,'UNECE Contracting Parties'),(182,178,'UNECE Contracting Parties'),(183,31,'UNECE Contracting Parties'),(184,79,'UNECE Contracting Parties'),(185,80,'UNECE Contracting Parties'),(186,32,'UNECE Contracting Parties'),(187,33,'UNECE Contracting Parties'),(188,81,'UNECE Contracting Parties'),(189,92,'UNECE Contracting Parties'),(190,82,'UNECE Contracting Parties'),(191,34,'UNECE Contracting Parties'),(192,134,'UNECE Contracting Parties'),(193,83,'UNECE Contracting Parties'),(194,135,'UNECE Contracting Parties'),(195,35,'UNECE Contracting Parties'),(196,84,'UNECE Contracting Parties'),(197,85,'UNECE Contracting Parties'),(198,138,'UNECE Contracting Parties'),(199,86,'UNECE Contracting Parties'),(200,36,'UNECE Contracting Parties'),(201,140,'UNECE Contracting Parties'),(202,87,'UNECE Contracting Parties'),(203,88,'UNECE Contracting Parties'),(204,37,'UNECE Contracting Parties'),(205,38,'UNECE Contracting Parties'),(206,39,'UNECE Contracting Parties'),(207,143,'UNECE Contracting Parties'),(208,40,'UNECE Contracting Parties'),(209,41,'UNECE Contracting Parties'),(210,89,'UNECE Contracting Parties'),(211,42,'UNECE Contracting Parties'),(212,90,'UNECE Contracting Parties'),(213,169,'UNECE Contracting Parties'),(214,180,'UNECE Contracting Parties'),(215,43,'UNECE Contracting Parties'),(216,44,'Vietnam'),(217,45,'UNECE Contracting Parties'),(218,145,'UNECE Contracting Parties'),(221,7,'China'),(222,11,'India'),(223,169,'United States'),(224,172,'Brazil'),(225,16,'Japan'),(226,33,'South Korea'),(227,189,'Australia & New Zealand');
/*!40000 ALTER TABLE `region_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regulation`
--

DROP TABLE IF EXISTS `regulation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regulation` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `CN_Name` text,
  `EN_Name` text,
  `Region_Name` varchar(45) NOT NULL,
  `isMandatory` tinyint DEFAULT NULL,
  `M1` varchar(45) NOT NULL,
  `M2` varchar(45) NOT NULL,
  `M3` varchar(45) NOT NULL,
  `N1` varchar(45) NOT NULL,
  `N2` varchar(45) NOT NULL,
  `N3` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_regulation_region1_idx` (`Region_Name`),
  KEY `fk_regulation_applicalble_enum1_idx` (`M1`),
  KEY `fk_regulation_applicalble_enum2_idx` (`M2`),
  KEY `fk_regulation_applicalble_enum3_idx` (`M3`),
  KEY `fk_regulation_applicalble_enum4_idx` (`N1`),
  KEY `fk_regulation_applicalble_enum5_idx` (`N2`),
  KEY `fk_regulation_applicalble_enum6_idx` (`N3`),
  CONSTRAINT `fk_regulation_applicalble_enum1` FOREIGN KEY (`M1`) REFERENCES `applicalble_enum` (`Value`),
  CONSTRAINT `fk_regulation_applicalble_enum2` FOREIGN KEY (`M2`) REFERENCES `applicalble_enum` (`Value`),
  CONSTRAINT `fk_regulation_applicalble_enum3` FOREIGN KEY (`M3`) REFERENCES `applicalble_enum` (`Value`),
  CONSTRAINT `fk_regulation_applicalble_enum4` FOREIGN KEY (`N1`) REFERENCES `applicalble_enum` (`Value`),
  CONSTRAINT `fk_regulation_applicalble_enum5` FOREIGN KEY (`N2`) REFERENCES `applicalble_enum` (`Value`),
  CONSTRAINT `fk_regulation_applicalble_enum6` FOREIGN KEY (`N3`) REFERENCES `applicalble_enum` (`Value`),
  CONSTRAINT `fk_regulation_region1` FOREIGN KEY (`Region_Name`) REFERENCES `region` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regulation`
--

LOCK TABLES `regulation` WRITE;
/*!40000 ALTER TABLE `regulation` DISABLE KEYS */;
INSERT INTO `regulation` VALUES (2,'(EU)-2015/758','欧盟2015/758号委员会条例，修订关于机动车高级驾驶辅助系统（ADAS）型式认证要求的(EC)第661/2009号条例','Commission Regulation (EU) 2015/758 of 29 April 2015 amending Regulation (EC) No 661/2009 of the European Parliament and of the Council as regards the type-approval requirements for the safety of motor vehicles with regard to advanced driver assistance systems (ADAS)','European Union (EU)',NULL,'M','O','O','O','N','N'),(3,'(EU)-2021/1243','欧盟2021/1243号委员会条例，修订关于机动车一般安全及碰撞时乘员保护型式认证的(EU)2018/858号条例','Commission Regulation (EU) 2021/1243 of 14 July 2021 amending Regulation (EU) 2018/858 as regards the type-approval of motor vehicles with respect to their general safety and the protection of vehicle occupants in the event of a collision','European Union (EU)',NULL,'M','O','O','M','N','N'),(4,'(EU)-2021/1341','欧盟2021/1341号委员会条例，制定关于机动车智能速度辅助系统安全型式认证要求的(EU)2019/2144号条例实施的技术规范','Commission Regulation (EU) 2021/1341 of 22 July 2021 laying down technical specifications for the implementation of Regulation (EU) 2019/2144 as regards the type-approval requirements for the safety of motor vehicles with regard to intelligent speed assistance systems','European Union (EU)',NULL,'M','O','O','M','O','O'),(5,'(EU)-2021/1958','欧盟2021/1958号实施条例，制定关于机动车高级驾驶辅助系统（ADAS）安全型式认证要求的(EU)2019/2144号条例实施的技术规范','Commission Implementing Regulation (EU) 2021/1958 of 5 November 2021 laying down technical specifications for the implementation of Regulation (EU) 2019/2144 as regards the type-approval requirements for the safety of motor vehicles with respect to advanced driver assistance systems (ADAS)','European Union (EU)',NULL,'M','M','M','M','M','M'),(6,'(EU)-2021/646','欧盟2021/646号委员会条例，修订关于轻型乘用车和商用车排放型式认证的(EC)第715/2007号条例（欧6标准）','Commission Regulation (EU) 2021/646 of 21 April 2021 amending Regulation (EC) No 715/2007 of the European Parliament and of the Council as regards the type-approval of motor vehicles with respect to emissions from light passenger and commercial vehicles (Euro 6)','European Union (EU)',NULL,'M','O','O','M','O','O'),(7,'(EU)-2022/1426','欧盟2022/1426号条例，关于全自动和半自动驾驶系统的型式认证，并修订(EU)2018/858和(EU)2019/2144号条例','Regulation (EU) 2022/1426 of the European Parliament and of the Council of 30 June 2022 on the type-approval of fully automated and semi-automated driving systems and amending Regulations (EU) 2018/858 and (EU) 2019/2144','European Union (EU)',NULL,'M','O','O','M','O','O'),(8,'(EU)-2023/2590','欧盟2023/2590号委员会条例，修订关于机动车一般安全型式认证的(EU)2018/858号条例','Commission Regulation (EU) 2023/2590 of 20 November 2023 amending Regulation (EU) 2018/858 as regards the type-approval of motor vehicles with respect to their general safety','European Union (EU)',NULL,'M','O','O','M','O','O'),(9,'ADR-107/00','澳大利亚设计规则107/00 - 照明和光信号装置（修订版00）','Australian Design Rule 107/00 - Lighting and Light Signalling Devices (Amendment 00)','Australia & New Zealand',NULL,'M','M','M','M','M','M'),(10,'ADR-108','澳大利亚设计规则108 - 后视镜','Australian Design Rule 108 - Rear Vision Mirrors','Australia & New Zealand',NULL,'M','O','O','M','N','N'),(11,'ADR-45/01','澳大利亚设计规则45/01 - 被动乘员保护（修订版01）','Australian Design Rule 45/01 - Passive Occupant Protection (Amendment 01)','Australia & New Zealand',NULL,'N','M','M','N','M','M'),(12,'ADR-97','澳大利亚设计规则97 - 高级驾驶辅助系统（ADAS）','Australian Design Rule 97 - Advanced Driver Assistance Systems (ADAS)','Australia & New Zealand',NULL,'M','O','O','M','O','O'),(13,'ADR-99','澳大利亚设计规则99 - 自动车道保持系统（ALKS）','Australian Design Rule 99 - Automated Lane Keeping Systems (ALKS)','Australia',NULL,'M','O','O','M','N','N'),(14,'ADR-98','澳大利亚设计规则98 - 驾驶员监控系统（DMS）','Australian Design Rule 98 - Driver Monitoring Systems (DMS)','Australia',NULL,'M','O','O','O','N','N'),(15,'AIS-001','印度汽车工业标准001 - 汽车用安全玻璃','Automotive Industry Standard 001 - Safety Glass for Automotive Purposes','India',NULL,'M','O','O','M','O','O'),(16,'AIS-002','印度汽车工业标准002 - 机动车后视镜','Automotive Industry Standard 002 - Rear View Mirrors for Motor Vehicles','India',NULL,'M','O','O','M','O','O'),(17,'AIS-008-Rev2','印度汽车工业标准008修订版2 - 机动车照明和光信号装置','Automotive Industry Standard 008 Revision 2 - Lighting and Light Signalling Devices for Motor Vehicles','India',NULL,'N','N','N','N','N','N'),(18,'AIS-140','印度汽车工业标准140 - 基于全球导航卫星系统（GNSS）的机动车跟踪系统','Automotive Industry Standard 140 - Global Navigation Satellite System (GNSS) Based Vehicle Tracking System for Motor Vehicles','India',NULL,'N','M','M','N','M','M'),(19,'AIS-145','印度汽车工业标准145 - 机动车高级驾驶辅助系统（ADAS）要求','Automotive Industry Standard 145 - Requirements for Automated Driver Assistance Systems (ADAS) for Motor Vehicles','India',NULL,'N','N','N','N','N','N'),(20,'AIS-150','印度汽车工业标准150 - 机动车自动车道保持系统（ALKS）','Automotive Industry Standard 150 - Automated Lane Keeping System (ALKS) for Motor Vehicles','India',NULL,'M','O','O','M','O','O'),(21,'AIS-151','印度汽车工业标准151 - 机动车驾驶员监控系统（DMS）','Automotive Industry Standard 151 - Driver Monitoring System (DMS) for Motor Vehicles','India',NULL,'M','O','O','M','O','O'),(22,'AIS-162','印度汽车工业标准162 - 电动汽车充电系统要求','Automotive Industry Standard 162 - Electric Vehicle Charging System Requirements','India',NULL,'M','O','O','M','N','N'),(23,'AIS-184','印度汽车工业标准184 - 《驾驶员疲劳与注意力警告系统 (DDAWS)》','Automotive Industry Standard 184 - Requirements for Advanced Emergency Braking System (AEBS) for Commercial Vehicles','India',NULL,'M','N','N','O','N','N'),(24,'AIS-185','印度汽车工业标准185 - 商用车高级紧急制动系统（AEBS）要求','Automotive Industry Standard 185 - Requirements for Lane Departure Warning System (LDWS) for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(25,'AIS-186','印度汽车工业标准186 - 机动车盲点检测系统（BSDS）要求','Automotive Industry Standard 186 - Requirements for Blind Spot Detection System (BSDS) for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(26,'AIS-187','印度汽车工业标准187 - 机动车自适应巡航控制（ACC）系统要求','Automotive Industry Standard 187 - Requirements for Adaptive Cruise Control (ACC) System for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(27,'AIS-188','印度汽车工业标准188 - 机动车前向碰撞预警系统（FCWS）要求','Automotive Industry Standard 188 - Requirements for Forward Collision Warning System (FCWS) for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(28,'AIS-189','印度汽车工业标准189 - 机动车自动泊车系统（APS）要求','Automotive Industry Standard 189 - Requirements for Automatic Parking System (APS) for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(29,'AIS-190','印度汽车工业标准190 - 机动车交通标志识别（TSR）系统要求','Automotive Industry Standard 190 - Requirements for Traffic Sign Recognition (TSR) System for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(30,'AIS-191','印度汽车工业标准191 - 机动车智能速度辅助（ISA）系统要求','Automotive Industry Standard 191 - Requirements for Intelligent Speed Assistance (ISA) System for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(31,'AIS-192','印度汽车工业标准192 - 机动车紧急车道保持系统（ELKS）要求','Automotive Industry Standard 192 - Requirements for Emergency Lane Keeping System (ELKS) for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(32,'AIS-193','印度汽车工业标准193 - 机动车后方横向交通预警（RCTA）系统要求','Automotive Industry Standard 193 - Requirements for Rear Cross Traffic Alert (RCTA) System for Motor Vehicles','India',NULL,'M','N','N','O','N','N'),(33,'BR_Port_SENATRAN_1554-2022_EN_2023-01-17.pdf','巴西国家交通局（SENATRAN）2022年12月22日第1554号法令（英文版，2023年1月17日）- 巴西自动驾驶系统（ADS）型式批准要求','Portaria SENATRAN nº 1554, de 22 de dezembro de 2022 (English Version) - Requirements for the Homologation of Automated Driving Systems (ADS) in Brazil (2023-01-17)','Brazil',NULL,'O','M','M','O','M','M'),(34,'FMVSS-108','美国联邦机动车安全标准108 - 灯具、反光装置及相关设备','Federal Motor Vehicle Safety Standard No. 108 - Lamps, Reflective Devices, and Associated Equipment','United States',NULL,'M','N','N','O','N','N'),(35,'FMVSS-111','美国联邦机动车安全标准111 - 后视镜','Federal Motor Vehicle Safety Standard No. 111 - Rearview Mirrors','United States',NULL,'M','O','O','M','N','N'),(36,'FMVSS-127','美国联邦机动车安全标准127 - 挂车制动系统','Federal Motor Vehicle Safety Standard No. 127 - Trailer Brake Systems','United States',NULL,'M','O','O','M','O','O'),(37,'FMVSS-128','美国联邦机动车安全标准128 - 电子稳定控制系统','Federal Motor Vehicle Safety Standard No. 128 - Electronic Stability Control Systems','United States',NULL,'M','N','N','O','N','N'),(38,'GB-15084-2022','机动车间接视野装置性能和安装要求（GB 15084-2022）','National Standard of the People\'s Republic of China 15084-2022 - Performance and Installation Requirements for Indirect Vision Devices of Motor Vehicles','China',NULL,'M','O','O','M','N','N'),(39,'GB-21670-2008','乘用车制动系统技术要求及试验方法（GB 21670-2008）','National Standard of the People\'s Republic of China 21670-2008 - Technical Requirements and Test Methods for Braking Systems of Passenger Cars','China',NULL,'M','O','O','M','O','O'),(41,'GB-39732-2020','汽车事件数据记录系统（GB 39732-2020）','National Standard of the People\'s Republic of China 39732-2020 - Automotive Event Data Recorder System','China',NULL,'M','N','N','O','N','N'),(42,'GB-5768.3.2009','道路交通标志和标线 第3部分：道路交通标线','National Standard of the People\'s Republic of China 5768.3-2009 - Road Traffic Signs and Markings Part 3: Road Traffic Markings','China',NULL,'O','O','O','O','O','O'),(43,'GB/T-20608-2006','汽车行驶记录仪（GB/T 20608-2006）','National Recommended Standard of the People\'s Republic of China 20608-2006 - Vehicle Travel Data Recorder','China',NULL,'O','N','N','N','N','N'),(44,'GB/T-26773-2011','商用车辆车道保持辅助系统性能要求和试验方法（GB/T 26773-2011）','National Recommended Standard of the People\'s Republic of China 26773-2011 - Performance Requirements and Test Methods for Lane Keeping Assistance Systems of Commercial Vehicles','China',NULL,'O','N','N','N','N','N'),(45,'GB/T-38186','汽车智能泊车辅助系统性能要求与试验方法（GB/T 38186-2019，注：补全年份）','National Recommended Standard of the People\'s Republic of China 38186-2019 - Performance Requirements and Test Methods for Intelligent Parking Assistance Systems of Automobiles','China',NULL,'O','N','N','O','N','N'),(46,'GB/T-39265-2020','汽车驾驶自动化分级（GB/T 39265-2020）','National Recommended Standard of the People\'s Republic of China 39265-2020 - Classification of Automobile Driving Automation','China',NULL,'M','O','O','M','O','O'),(47,'GB/T-39323-2020','汽车先进驾驶辅助系统（ADAS）术语（GB/T 39323-2020）','National Recommended Standard of the People\'s Republic of China 39323-2020 - Terminology for Advanced Driver Assistance Systems (ADAS) of Automobiles','China',NULL,'O','M','M','O','M','M'),(48,'GB/T-39901','汽车自动紧急制动系统（AEBS）性能要求和试验方法（GB/T 39901-2021，注：补全年份）','National Recommended Standard of the People\'s Republic of China 39901-2021 - Performance Requirements and Test Methods for Automotive Advanced Emergency Braking System (AEBS)','China',NULL,'M','O','O','M','O','O'),(49,'GB/T-41630-2022','汽车智能巡航控制系统性能要求与试验方法（GB/T 41630-2022）','National Recommended Standard of the People\'s Republic of China 41630-2022 - Performance Requirements and Test Methods for Intelligent Cruise Control Systems of Automobiles','China',NULL,'O','O','O','O','O','O'),(50,'GB/T-44433-2024','汽车车道居中控制系统性能要求与试验方法（GB/T 44433-2024）','National Recommended Standard of the People\'s Republic of China 44433-2024 - Performance Requirements and Test Methods for Automotive Lane Centering Control Systems','China',NULL,'M','O','O','M','O','O'),(51,'GB/T-Multi-lane-manoeuver','汽车多车道变道辅助系统性能要求与试验方法（GB/T 多车道变道专项标准，注：非官方编号）','National Recommended Standard of the People\'s Republic of China - Performance Requirements and Test Methods for Automotive Multi-Lane Maneuver Assistance Systems','China',NULL,'O','N','N','O','N','N'),(52,'GB/T-Single-Lane-Manouvre','汽车单车道保持辅助系统性能要求与试验方法（GB/T 单车道操作专项标准，注：非官方编号）','National Recommended Standard of the People\'s Republic of China - Performance Requirements and Test Methods for Automotive Single-Lane Maneuver Assistance Systems','China',NULL,'O','N','N','O','N','N'),(53,'GB_T_44173-2024','汽车驾驶员监控系统性能要求与试验方法（GB/T 44173-2024，注：下划线为笔误）','National Recommended Standard of the People\'s Republic of China 44173-2024 - Performance Requirements and Test Methods for Automotive Driver Monitoring Systems','China',NULL,'M','O','O','M','N','N'),(54,'IRC:35:2015','印度道路协会规范35:2015 - 国家公路和邦级公路的道路标志和标线规范','Indian Road Congress Code 35:2015 - Specifications for Road Signs and Markings for National Highways and State Highways','India',NULL,'O','O','O','O','O','O'),(55,'IS-11852-2019','印度标准11852:2019 - 机动车 - 高级驾驶辅助系统（ADAS） - 性能要求和试验方法','Indian Standard 11852:2019 - Motor Vehicles - Advanced Driver Assistance Systems (ADAS) - Performance Requirements and Test Methods','India',NULL,'M','N','N','O','N','N'),(56,'IS-15986-2015','印度标准15986:2015 - 机动车 - 碰撞预警系统 - 规范','Indian Standard 15986:2015 - Motor Vehicles - Collision Warning System - Specifications','India',NULL,'N','M','M','N','M','M'),(57,'ISO-17361:2017','ISO 17361:2017 - 道路车辆 - 电子收费 - 车载单元与外部设备的通信接口','ISO 17361:2017 - Road vehicles - Electronic fee collection - Communication interface between on-board unit and external equipment','UNECE Contracting Parties',NULL,'O','M','M','O','M','M'),(58,'KMVSS-Article-90-3','韩国机动车安全标准第90-3条 - 自动驾驶系统安全要求','Korean Motor Vehicle Safety Standards Article 90-3 - Safety Requirements for Automated Driving Systems','South Korea',NULL,'M','N','N','O','N','N'),(59,'KR_KMVSS_complete_corr_EN_2022-02-15.pdf','韩国机动车安全标准（KMVSS）完整修正版（英文版，2022年2月15日）','Complete Corrected English Version of Korean Motor Vehicle Safety Standards (KMVSS) (2022-02-15)','South Korea',NULL,'M','O','O','M','N','N'),(60,'MLIT-619','日本国土交通省第619号通知 - 机动车自动驾驶系统安全标准','Ministry of Land, Infrastructure, Transport and Tourism (Japan) Notification No. 619 - Safety Standards for Automated Driving Systems for Motor Vehicles','Japan',NULL,'M','N','N','O','N','N'),(61,'MLIT-619-Att-130','日本国土交通省第619号通知附件130 - 自动驾驶系统试验方法','Ministry of Land, Infrastructure, Transport and Tourism (Japan) Notification No. 619 Attachment 130 - Test Methods for Automated Driving Systems','Japan',NULL,'M','N','N','O','N','N'),(62,'NCAP','新车评价规程 - 新型机动车安全评级全球协议','New Car Assessment Program - Global Protocol for Safety Rating of New Motor Vehicles','UNECE Contracting Parties',NULL,'M','N','N','O','N','N'),(63,'Resolution-CONTRAN-759/2018','巴西国家交通委员会（CONTRAN）2018年12月19日第759号决议 - 配备高级驾驶辅助系统（ADAS）的机动车型式批准规范','Resolução CONTRAN nº 759, de 19 de dezembro de 2018 - Normas para Homologação de Veículos Automotores com Sistemas de Assistência ao Condutor Avançados (ADAS)','Brazil',NULL,'M','N','N','O','N','N'),(64,'Resolution-CONTRAN-970/2022','巴西国家交通委员会（CONTRAN）2022年7月28日第970号决议 - 机动车3级自动驾驶系统型式批准规范','Resolução CONTRAN nº 970, de 28 de julho de 2022 - Normas para Homologação de Sistemas de Direção Automatizada de Nível 3 em Veículos Automotores','Brazil',NULL,'O','M','M','O','M','M'),(65,'UN-R13','联合国欧洲经济委员会第13号法规 - 关于机动车制动系统批准的统一规定','UNECE Regulation No. 13 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to the Braking System','UNECE Contracting Parties',NULL,'M','M','M','M','M','M'),(66,'UN-R130','联合国欧洲经济委员会第130号法规 - 关于机动车车道偏离预警系统（LDWS）批准的统一规定','UNECE Regulation No. 130 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Lane Departure Warning Systems (LDWS)','UNECE Contracting Parties',NULL,'M','O','O','M','O','O'),(67,'UN-R131','联合国欧洲经济委员会第131号法规 - 关于乘用车高级紧急制动系统（AEBS）批准的统一规定','UNECE Regulation No. 131 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Advanced Emergency Braking Systems (AEBS) for Passenger Cars','UNECE Contracting Parties',NULL,'M','O','O','M','O','O'),(68,'UN-R13H','联合国欧洲经济委员会第13号法规修订版H - 重型车辆制动系统要求修订','UNECE Regulation No. 13 Amendment H - Revision to Braking System Requirements for Heavy-Duty Vehicles','UNECE Contracting Parties',NULL,'N','M','M','N','M','M'),(69,'UN-R144','联合国欧洲经济委员会第144号法规 - 关于机动车事件数据记录器（EDR）批准的统一规定','UNECE Regulation No. 144 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Event Data Recorders (EDR)','UNECE Contracting Parties',NULL,'M','O','O','M','N','N'),(70,'UN-R151','联合国欧洲经济委员会第151号法规 - 关于机动车电动和电子系统网络安全批准的统一规定','UNECE Regulation No. 151 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Cybersecurity for Electric and Electronic Vehicle Systems','UNECE Contracting Parties',NULL,'M','O','O','M','N','N'),(71,'UN-R152','联合国欧洲经济委员会第152号法规 - 关于商用车高级紧急制动系统（AEBS）批准的统一规定','UNECE Regulation No. 152 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Advanced Emergency Braking Systems (AEBS) for Commercial Vehicles','UNECE Contracting Parties',NULL,'M','O','O','O','N','N'),(72,'UN-R155','联合国欧洲经济委员会第155号法规 - 关于机动车网络安全和网络安全管理体系（CSMS）批准的统一规定','UNECE Regulation No. 155 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Cybersecurity and Cyber Security Management System (CSMS)','UNECE Contracting Parties',NULL,'M','O','O','M','N','N'),(73,'UN-R156','联合国欧洲经济委员会第156号法规 - 关于机动车软件更新和软件更新管理体系（SUMS）批准的统一规定','UNECE Regulation No. 156 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Software Update and Software Update Management System (SUMS)','UNECE Contracting Parties',NULL,'M','M','M','M','M','M'),(74,'UN-R157','联合国欧洲经济委员会第157号法规 - 关于机动车自动车道保持系统（ALKS）批准的统一规定','UNECE Regulation No. 157 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Automated Lane Keeping Systems (ALKS)','UNECE Contracting Parties',NULL,'M','O','O','M','N','N'),(75,'UN-R157/VMAD','联合国欧洲经济委员会第157号法规（含VMAD修订版） - 自动车道保持系统车辆自动化数据记录','UNECE Regulation No. 157 with VMAD Amendment - Vehicle Automated Data Recording for Automated Lane Keeping Systems','UNECE Contracting Parties',NULL,'M','O','O','M','N','N'),(76,'UN-R158','联合国欧洲经济委员会第158号法规 - 关于机动车电动助力转向系统批准的统一规定','UNECE Regulation No. 158 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to the Electric Power Steering System','UNECE Contracting Parties',NULL,'M','O','O','M','O','O'),(77,'UN-R159','联合国欧洲经济委员会第159号法规 - 关于机动车自适应巡航控制系统批准的统一规定','UNECE Regulation No. 159 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to the Adaptive Cruise Control System','UNECE Contracting Parties',NULL,'M','O','O','M','O','O'),(78,'UN-R160','联合国欧洲经济委员会第160号法规 - 关于机动车盲点检测系统批准的统一规定','UNECE Regulation No. 160 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to the Blind Spot Detection System','UNECE Contracting Parties',NULL,'M','N','N','O','N','N'),(79,'UN-R166','联合国欧洲经济委员会第166号法规 - 关于电动和混合动力电动汽车特定安全要求批准的统一规定','UNECE Regulation No. 166 - Uniform Provisions Concerning the Approval of Electric and Hybrid Electric Vehicles with Regard to Specific Safety Requirements','UNECE Contracting Parties',NULL,'M','O','O','O','N','N'),(80,'UN-R171','联合国欧洲经济委员会第171号法规 - 关于机动车驾驶员控制辅助系统（DCAS）批准的统一规定','UNECE Regulation No. 171 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Driver Control Assistance Systems (DCAS)','UNECE Contracting Parties',NULL,'M','O','O','M','O','O'),(81,'UN-R175','联合国欧洲经济委员会第175号法规 - 关于机动车远程泊车辅助系统（RPAS）批准的统一规定','UNECE Regulation No. 175 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to Remote Parking Assistance Systems (RPAS)','UNECE Contracting Parties',NULL,'M','O','O','M','O','O'),(82,'UN-R46','联合国欧洲经济委员会第46号法规 - 关于机动车视野和间接视野装置批准的统一规定','UNECE Regulation No. 46 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to the Field of Vision and Indirect Vision Devices','UNECE Contracting Parties',NULL,'M','O','O','M','N','N'),(83,'UN-R48','联合国欧洲经济委员会第48号法规 - 关于机动车照明和光信号装置批准的统一规定','UNECE Regulation No. 48 - Uniform Provisions Concerning the Approval of Vehicles with Regard to their Lighting and Light-Signalling Devices','UNECE Contracting Parties',NULL,'M','M','M','M','M','M'),(84,'UN-R79','联合国欧洲经济委员会第79号法规 - 关于机动车转向装置批准的统一规定','UNECE Regulation No. 79 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to the Steering Equipment','UNECE Contracting Parties',NULL,'N','N','N','N','N','N'),(85,'VSTD-035','越南机动车技术标准035 - 高级驾驶辅助系统（ADAS）安全要求','Vietnamese Technical Standard for Vehicles 035 - Safety Requirements for Advanced Driver Assistance Systems (ADAS)','Vietnam',NULL,'O','N','N','N','N','N'),(86,'VSTD-232','越南机动车技术标准232 - 机动车照明和光信号装置','Vietnamese Technical Standard for Vehicles 232 - Lighting and Light Signalling Devices for Motor Vehicles','Vietnam',NULL,'O','N','N','N','N','N'),(87,'VSTD-271','越南机动车技术标准271 - 乘用车制动系统','Vietnamese Technical Standard for Vehicles 271 - Braking Systems for Passenger Cars','Vietnam',NULL,'O','N','N','N','N','N'),(88,'VSTD-472','越南机动车技术标准472 - 机动车驾驶员监控系统（DMS）','Vietnamese Technical Standard for Vehicles 472 - Driver Monitoring Systems (DMS) for Motor Vehicles','Vietnam',NULL,'O','N','N','N','N','N'),(89,'VSTD-700','越南机动车技术标准700 - 自动驾驶系统通用安全要求','Vietnamese Technical Standard for Vehicles 700 - General Safety Requirements for Automated Driving Systems','Vietnam',NULL,'O','N','N','N','N','N'),(90,'VSTD-710','越南机动车技术标准710 - 机动车自动车道保持系统（ALKS）','Vietnamese Technical Standard for Vehicles 710 - Automated Lane Keeping System (ALKS) for Motor Vehicles','Vietnam',NULL,'O','N','N','N','N','N'),(91,'VSTD-720','越南机动车技术标准720 - 机动车自适应巡航控制（ACC）系统','Vietnamese Technical Standard for Vehicles 720 - Adaptive Cruise Control (ACC) System for Motor Vehicles','Vietnam',NULL,'O','N','N','N','N','N'),(92,'VSTD-940','越南机动车技术标准940 - 机动车事件数据记录器（EDR）','Vietnamese Technical Standard for Vehicles 940 - Event Data Recorder (EDR) for Motor Vehicles','Vietnam',NULL,'O','N','N','N','N','N'),(93,'VSTD-960','越南机动车技术标准960 - 机动车电子系统网络安全要求','Vietnamese Technical Standard for Vehicles 960 - Cybersecurity Requirements for Motor Vehicle Electronic Systems','Vietnam',NULL,'O','N','N','N','N','N'),(94,'VSTD-970','越南机动车技术标准970 - 机动车系统软件更新要求','Vietnamese Technical Standard for Vehicles 970 - Software Update Requirements for Motor Vehicle Systems','Vietnam',NULL,'O','N','N','N','N','N'),(95,'VSTD-980','越南机动车技术标准980 - 机动车远程泊车辅助系统（RPAS）','Vietnamese Technical Standard for Vehicles 980 - Remote Parking Assistance System (RPAS) for Motor Vehicles','Vietnam',NULL,'O','N','N','N','N','N'),(96,'UN-R89','联合国欧洲经济委员会第89号法规 - 关于机动车限速装置批准的统一规定','UNECE Regulation No. 89 - Uniform Provisions Concerning the Approval of Motor Vehicles with Regard to the Speed Limiting Device','UNECE Contracting Parties',NULL,'N','M','M','N','M','M'),(97,'GB 7258-202X','《智能网联汽车 组合驾驶辅助系统安全要求》','CDCAS','China',1,'M','M','M','M','M','M');
/*!40000 ALTER TABLE `regulation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `release_content`
--

DROP TABLE IF EXISTS `release_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `release_content` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Content` varchar(45) DEFAULT NULL,
  `Planned_Release_Date` varchar(45) DEFAULT NULL,
  `Release_Version` varchar(100) DEFAULT NULL,
  `Item_Status` varchar(45) DEFAULT NULL,
  `Belong_Feature` varchar(45) DEFAULT NULL,
  `Create_Time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Content_Type` varchar(45) DEFAULT NULL,
  `Bug_ID` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Bug_ID_UNIQUE` (`Bug_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `release_content`
--

LOCK TABLES `release_content` WRITE;
/*!40000 ALTER TABLE `release_content` DISABLE KEYS */;
INSERT INTO `release_content` VALUES (1,'发布\"功能星球”板块业务，提供ADAS用户功能知识信息','2025-12-11','Alpha.25.12.3','已上线','功能星球','2025-12-07 05:20:30','creation','NO-1'),(2,'发布\"硬件星球”板块业务，提供ADAS用户功能知识信息','2025-12-07','','规划中','硬件星球','2025-12-07 05:21:49','creation','NO-2'),(3,'发布“知识网络”功能，通过交互式网络图提供ADAS学习的脉络和方法','2025-12-07','','开发中','知识网络','2025-12-07 15:09:42','creation','NO-3'),(4,'发布“传感器星球”功能','2025-12-08','','规划中','传感器星球','2025-12-07 15:10:48','creation','NO-4'),(5,'发布“环境生成器”功能','2025-11-29','','完成_待上线','环境生成器','2025-12-07 15:11:24','creation','NO-5'),(6,'发布“传感器配置器”功能，自行定义，快速绘制你的传感器配置图','2025-12-06','ALPHA-25-12-1','开发中','传感器配置器','2025-12-07 15:34:06','creation','NO-6'),(9,'lllll','2025-12-12',NULL,'规划中','产品配置器','2025-12-08 06:14:44','bug_fix','27'),(10,'3D预览功能无法使用','2025-12-13','','已上线','环境生成器','2025-12-08 06:21:57','bug_fix','28'),(26,'111','2025-12-20',NULL,'开发中','知识网络','2025-12-08 07:50:31','creation','NO-26'),(27,'替换后台服务器数据库','2025-12-06','','开发中','通用修改','2025-12-10 01:58:42','creation','NO-27'),(28,'服务器无法连接-返回fail-to-fetch','2025-12-17',NULL,'完成_待上线','通用信息','2025-12-10 02:27:27','bug_fix','29');
/*!40000 ALTER TABLE `release_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sae_enum`
--

DROP TABLE IF EXISTS `sae_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sae_enum` (
  `LEVEL` varchar(45) NOT NULL,
  PRIMARY KEY (`LEVEL`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sae_enum`
--

LOCK TABLES `sae_enum` WRITE;
/*!40000 ALTER TABLE `sae_enum` DISABLE KEYS */;
INSERT INTO `sae_enum` VALUES ('L0'),('L1'),('L2'),('L2+'),('L2++'),('L3'),('L4'),('L5');
/*!40000 ALTER TABLE `sae_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_type_enum`
--

DROP TABLE IF EXISTS `sensor_type_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_type_enum` (
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`Type`),
  UNIQUE KEY `TYPE_UNIQUE` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_type_enum`
--

LOCK TABLES `sensor_type_enum` WRITE;
/*!40000 ALTER TABLE `sensor_type_enum` DISABLE KEYS */;
INSERT INTO `sensor_type_enum` VALUES ('Camera_FE'),('Camera_PH'),('Lidar'),('Radar'),('Ultrasonic_Sensor');
/*!40000 ALTER TABLE `sensor_type_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_type_enum_sub`
--

DROP TABLE IF EXISTS `sensor_type_enum_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_type_enum_sub` (
  `SubType` varchar(45) NOT NULL,
  `Type` varchar(45) NOT NULL,
  PRIMARY KEY (`SubType`),
  KEY `fk_sensor_type_enum_sub_sensor_type_enum1_idx` (`Type`),
  CONSTRAINT `fk_sensor_type_enum_sub_sensor_type_enum1` FOREIGN KEY (`Type`) REFERENCES `sensor_type_enum` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_type_enum_sub`
--

LOCK TABLES `sensor_type_enum_sub` WRITE;
/*!40000 ALTER TABLE `sensor_type_enum_sub` DISABLE KEYS */;
INSERT INTO `sensor_type_enum_sub` VALUES ('FISHEYE','Camera_FE'),('General','Camera_PH'),('MIDDLE','Camera_PH'),('NARROW','Camera_PH'),('WIDE','Camera_PH'),('MECHANICAL','Lidar'),('MEMS','Lidar'),('3D','Radar'),('4D','Radar'),('USS','Ultrasonic_Sensor');
/*!40000 ALTER TABLE `sensor_type_enum_sub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensors`
--

DROP TABLE IF EXISTS `sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensors` (
  `ID` int NOT NULL,
  `NAME` varchar(45) DEFAULT NULL,
  `sensorscol` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensors`
--

LOCK TABLES `sensors` WRITE;
/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensors_equipement`
--

DROP TABLE IF EXISTS `sensors_equipement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensors_equipement` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `function_features_ID` int NOT NULL,
  `POSITION` varchar(45) NOT NULL,
  `Type` varchar(45) NOT NULL,
  `SubType` varchar(45) NOT NULL,
  `Mandatory` tinyint DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_sensors_function_features1_idx` (`function_features_ID`),
  KEY `fk_sensors_position_enum1_idx` (`POSITION`),
  KEY `fk_sensors_sensor_type_enum1_idx` (`Type`),
  KEY `fk_sensors_sensor_type_enum_sub1_idx` (`SubType`),
  CONSTRAINT `fk_sensors_function_features1` FOREIGN KEY (`function_features_ID`) REFERENCES `function_features` (`ID`),
  CONSTRAINT `fk_sensors_position_enum1` FOREIGN KEY (`POSITION`) REFERENCES `position_enum` (`POSITION`),
  CONSTRAINT `fk_sensors_sensor_type_enum1` FOREIGN KEY (`Type`) REFERENCES `sensor_type_enum` (`Type`),
  CONSTRAINT `fk_sensors_sensor_type_enum_sub1` FOREIGN KEY (`SubType`) REFERENCES `sensor_type_enum_sub` (`SubType`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensors_equipement`
--

LOCK TABLES `sensors_equipement` WRITE;
/*!40000 ALTER TABLE `sensors_equipement` DISABLE KEYS */;
INSERT INTO `sensors_equipement` VALUES (1,1,'Front_Center','Camera_PH','General',1),(2,1,'Front_Center','Radar','3D',0),(3,2,'Front_Center','Camera_PH','General',1),(4,2,'Front_Center','Radar','3D',1),(5,11,'Front_Center','Camera_PH','General',1),(6,20,'Front_Center','Camera_PH','WIDE',1),(7,20,'Rear_Center','Camera_PH','MIDDLE',1),(8,20,'Left','Camera_FE','FISHEYE',1),(9,20,'Right','Camera_FE','FISHEYE',0),(10,20,'Front_Center','Radar','3D',1),(11,20,'Front_Left_Corner','Radar','3D',1),(12,20,'Front_Right_Corner','Radar','3D',1),(13,20,'Rear_Left_Corner','Radar','3D',1),(14,20,'Rear_Right_Corner','Radar','3D',1),(15,24,'Rear_Left_Corner','Radar','3D',1),(16,24,'Rear_Right_Corner','Radar','3D',1),(17,33,'Front_Center','Camera_PH','General',1),(18,34,'Front_Center','Camera_PH','General',1),(19,3,'Front_Center','Camera_PH','General',0),(20,4,'Front_Center','Camera_PH','General',0),(21,5,'Front_Center','Camera_PH','General',1),(22,9,'Front_Center','Camera_PH','General',1),(23,6,'Front_Center','Camera_PH','General',1),(24,10,'Front_Center','Camera_PH','General',1),(25,10,'Front_Center','Radar','3D',0),(26,12,'Front_Center','Camera_PH','General',1),(27,12,'Front_Center','Radar','3D',1),(28,12,'Front_Left_Corner','Radar','3D',1),(29,12,'Front_Right_Corner','Radar','3D',1),(30,12,'Rear_Left_Corner','Radar','3D',1),(31,12,'Rear_Right_Corner','Radar','3D',1),(32,13,'Front_Center','Camera_PH','General',1),(33,13,'Front_Center','Radar','3D',1),(34,13,'Front_Left_Corner','Radar','3D',1),(35,13,'Front_Right_Corner','Radar','3D',1),(36,13,'Rear_Right_Corner','Radar','3D',1),(37,13,'Rear_Left_Corner','Radar','3D',1),(38,17,'Front_Center','Camera_PH','NARROW',1),(39,17,'Front_Center','Camera_PH','WIDE',1),(40,17,'Front_Left','Camera_PH','General',1),(41,17,'Front_Right','Camera_PH','General',1),(42,17,'Rear_Left','Camera_PH','General',1),(43,17,'Rear_Right','Camera_PH','General',1),(44,17,'Rear_Center','Camera_PH','MIDDLE',1),(45,17,'Front_Center','Camera_FE','FISHEYE',1),(46,17,'Left','Camera_FE','FISHEYE',1),(47,17,'Right','Camera_FE','FISHEYE',1),(48,17,'Rear_Center','Camera_FE','FISHEYE',1),(49,17,'Front_Center','Radar','3D',0),(50,17,'Front_Center','Lidar','MEMS',0),(51,19,'Front_Center','Camera_PH','NARROW',1),(52,19,'Front_Right','Camera_PH','WIDE',1),(53,19,'Front_Left','Camera_PH','MIDDLE',1),(54,19,'Front_Right','Camera_PH','MIDDLE',1),(55,19,'Rear_Left','Camera_PH','MIDDLE',1),(56,19,'Rear_Right','Camera_PH','MIDDLE',1),(57,19,'Front_Center','Camera_FE','FISHEYE',1),(58,19,'Left','Camera_FE','FISHEYE',1),(59,19,'Right','Camera_FE','FISHEYE',1),(60,19,'Rear_Center','Camera_FE','FISHEYE',1),(61,19,'Front_Center','Lidar','MEMS',1),(62,19,'Front_Left_Corner','Lidar','MEMS',0),(63,19,'Front_Right_Corner','Lidar','MEMS',0),(64,25,'Rear_Left_Corner','Radar','3D',1),(65,25,'Rear_Right_Corner','Radar','3D',1),(66,25,'Rear_Left_Corner','Radar','3D',1),(67,25,'Rear_Right_Corner','Radar','3D',1),(68,26,'Rear_Left_Corner','Radar','3D',1),(69,26,'Rear_Right_Corner','Radar','3D',1),(70,27,'Rear_Left_Corner','Radar','3D',1),(71,27,'Rear_Right_Corner','Radar','3D',1),(72,28,'Front_Center','Camera_PH','General',1),(73,28,'Front_Left_Corner','Radar','3D',1),(74,28,'Front_Right_Corner','Radar','3D',1),(75,29,'Front_Center','Camera_PH','General',1),(76,29,'Front_Left_Corner','Radar','3D',1),(77,29,'Front_Right_Corner','Radar','3D',1),(78,30,'Front_Center','Camera_PH','General',1),(79,30,'Front_Center','Radar','3D',1),(80,36,'Front_Center','Camera_PH','General',1),(81,36,'Front_Right_Corner','Radar','3D',1),(82,36,'Front_Left_Corner','Radar','3D',1),(83,37,'Front_Center','Camera_PH','General',1),(84,37,'Rear_Left_Corner','Radar','3D',1),(85,37,'Rear_Right_Corner','Radar','3D',1),(86,38,'Front_Center','Camera_PH','General',1),(87,38,'Front_Left_Corner','Radar','3D',1),(88,38,'Front_Right_Corner','Radar','3D',1),(89,38,'Rear_Left_Corner','Radar','3D',1),(90,38,'Rear_Right_Corner','Radar','3D',1),(91,38,'Front_Center','Radar','3D',1),(92,39,'Front_Center','Camera_PH','General',1),(93,39,'Front_Right_Corner','Radar','3D',1),(94,39,'Front_Left_Corner','Radar','3D',1),(95,39,'Front_Center','Radar','3D',1),(96,39,'Rear_Left_Corner','Radar','3D',1),(97,39,'Rear_Right_Corner','Radar','3D',1),(98,41,'Front_Center','Camera_PH','MIDDLE',1),(99,41,'Front_Left_Corner','Radar','3D',1),(100,41,'Front_Right_Corner','Radar','3D',1),(101,42,'Front_inner_left','Camera_PH','General',1),(102,42,'Rear_Right_Corner','Radar','3D',1),(103,42,'Rear_Left_Corner','Radar','3D',1),(104,43,'Front_Center','Camera_PH','General',1),(105,45,'Front_Center','Camera_PH','General',1),(106,45,'Front_Center','Radar','3D',1),(107,46,'Front_Center','Camera_PH','General',1),(108,46,'Front_Center','Radar','3D',1),(109,49,'Front_Center','Camera_PH','NARROW',1),(110,49,'Front_Center','Camera_PH','WIDE',1),(111,49,'Front_Left','Camera_PH','General',1),(112,49,'Front_Right','Camera_PH','General',1),(113,49,'Rear_Left','Camera_PH','General',1),(114,49,'Rear_Right','Camera_PH','General',1),(115,49,'Rear_Center','Camera_PH','MIDDLE',1),(116,49,'Front_Center','Camera_FE','FISHEYE',1),(117,49,'Left','Camera_FE','FISHEYE',1),(118,49,'Right','Camera_FE','FISHEYE',1),(119,49,'Rear_Center','Camera_FE','FISHEYE',1),(120,49,'Front_Center','Radar','3D',0),(121,18,'Front_Center','Camera_PH','NARROW',1),(122,18,'Front_Right','Camera_PH','WIDE',1),(123,18,'Front_Left','Camera_PH','MIDDLE',1),(124,18,'Front_Right','Camera_PH','MIDDLE',1),(125,18,'Rear_Left','Camera_PH','MIDDLE',1),(126,18,'Rear_Right','Camera_PH','MIDDLE',1),(127,18,'Front_Center','Camera_FE','FISHEYE',1),(128,18,'Left','Camera_FE','FISHEYE',1),(129,18,'Right','Camera_FE','FISHEYE',1),(130,18,'Rear_Center','Camera_FE','FISHEYE',1),(131,18,'Front_Center','Lidar','MEMS',1),(132,18,'Front_Left_Corner','Lidar','MEMS',0),(133,18,'Front_Right_Corner','Lidar','MEMS',0),(134,51,'Front_Center','Camera_PH','NARROW',1),(135,51,'Front_Right','Camera_PH','WIDE',1),(136,51,'Front_Left','Camera_PH','MIDDLE',1),(137,51,'Front_Center','Camera_PH','WIDE',1),(138,51,'Rear_Left','Camera_PH','MIDDLE',1),(139,51,'Rear_Right','Camera_PH','MIDDLE',1),(140,51,'Front_Center','Camera_FE','FISHEYE',1),(141,51,'Left','Camera_FE','FISHEYE',1),(142,51,'Right','Camera_FE','FISHEYE',1),(143,51,'Rear_Center','Camera_FE','FISHEYE',1),(144,51,'Front_Center','Lidar','MEMS',1),(145,51,'Front_Left_Corner','Lidar','MEMS',0),(146,51,'Front_Right_Corner','Lidar','MEMS',0),(147,51,'Rear_Center','Camera_PH','NARROW',1),(148,19,'Rear_Center','Camera_PH','MIDDLE',1),(149,18,'Rear_Center','Camera_PH','General',1);
/*!40000 ALTER TABLE `sensors_equipement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serializers`
--

DROP TABLE IF EXISTS `serializers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serializers` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Data_Rate` float DEFAULT NULL,
  `MIN_TEMP` float DEFAULT NULL,
  `MAX_TEMP` float DEFAULT NULL,
  `EMI_Level` varchar(100) DEFAULT NULL,
  `Supply_Voltage` float DEFAULT NULL,
  `Interface_Type` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `NAMEINDEX` (`Name`) /*!80000 INVISIBLE */,
  KEY `fk_serializers_suppliers_enum1_idx` (`Supplier_Name`),
  KEY `fk_serializers_interface_enum_sub1_idx` (`Interface_Type`),
  CONSTRAINT `fk_serializers_interface_enum_sub1` FOREIGN KEY (`Interface_Type`) REFERENCES `interface_enum_sub` (`SUBTYPE_VALUE`),
  CONSTRAINT `fk_serializers_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serializers`
--

LOCK TABLES `serializers` WRITE;
/*!40000 ALTER TABLE `serializers` DISABLE KEYS */;
INSERT INTO `serializers` VALUES (1,'MAX96717','Maxim Integrated',6,-40,105,'CISPR 25 Class 2, ISO 11452-2',3.3,'FPD_LINK III'),(2,'MAX96717F','Maxim Integrated',6,-40,105,'CISPR 25 Class 3, ISO 11452-4',3.3,'FPD_LINK III'),(3,'DS90UB971','TI',6,-40,105,'CISPR 25 Class 2, ISO 11452-2',3.3,'FPD_LINK III'),(54,'DS90UB953-Q1','TI',6,-40,105,'CISPR 25 Class 2, ISO 11452-2',3.3,'FPD_LINK III'),(55,'DS90UB947-Q1','TI',3.12,-40,105,'ISO 11452-4 Class 3',1.8,'MIPI CSI-2'),(56,'AD9250-1GSPS','ADI',12.5,-40,85,'CISPR 25 Class 2',2.5,'LVDS'),(57,'AD9680','ADI',6.25,-40,85,'ISO 11452-6 Class 3',3.3,'MIPI CSI-2'),(59,'MAX96712','Maxim Integrated',6,-40,105,'CISPR 25 Class 2',3.3,'FPD_LINK III'),(60,'MAX9296','Maxim Integrated',3,-40,85,'ISO 11452-2 Class 2',1.8,'LVDS'),(61,'RAA279950','Renesas',5,-40,105,'CISPR 25 Class 3',3.3,'MIPI CSI-2'),(62,'S32V234配套Serializer','NXP',4,-40,85,'ISO 11452-3 Class 2',2.5,'LVDS'),(63,'NCV7685','ON-Semi',3.12,-40,105,'CISPR 25 Class 2',3.3,'LVDS'),(64,'STDP701','ST',6,-40,105,'ISO 11452-2 Class 3',1.8,'FPD_LINK III');
/*!40000 ALTER TABLE `serializers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution_euf_group`
--

DROP TABLE IF EXISTS `solution_euf_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solution_euf_group` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `ACC` tinyint(1) DEFAULT '0' COMMENT '是否具备自适应巡航功能（1=是，0=否）',
  `LKA` tinyint(1) DEFAULT '0' COMMENT '是否具备车道保持辅助功能（1=是，0=否）',
  `TSR` tinyint(1) DEFAULT '0' COMMENT '是否具备交通标志识别功能（1=是，0=否）',
  `TLR` tinyint(1) DEFAULT '0' COMMENT '是否具备交通灯识别功能（1=是，0=否）',
  `ISA` tinyint(1) DEFAULT '0' COMMENT '是否具备智能速度辅助功能（1=是，0=否）',
  `AHB` tinyint(1) DEFAULT '0' COMMENT '是否具备自动远光控制功能（1=是，0=否）',
  `EDR` tinyint(1) DEFAULT '0' COMMENT '是否具备事件数据记录器功能（1=是，0=否）',
  `ADB` tinyint(1) DEFAULT '0' COMMENT '是否具备自适应远光灯功能（1=是，0=否）',
  `FCW` tinyint(1) DEFAULT '0' COMMENT '是否具备前向碰撞预警功能（1=是，0=否）',
  `LDW` tinyint(1) DEFAULT '0' COMMENT '是否具备车道偏离预警功能（1=是，0=否）',
  `SLCA` tinyint(1) DEFAULT '0' COMMENT '是否具备侧方车道变更辅助功能（1=是，0=否）',
  `BSD` tinyint(1) DEFAULT '0' COMMENT '是否具备盲点监测功能（1=是，0=否）',
  `LCA` tinyint(1) DEFAULT '0' COMMENT '是否具备车道变更辅助功能（1=是，0=否）',
  `DOW` tinyint(1) DEFAULT '0' COMMENT '是否具备开门预警功能（1=是，0=否）',
  `RCW` tinyint(1) DEFAULT '0' COMMENT '是否具备后方碰撞预警功能（1=是，0=否）',
  `FCTA` tinyint(1) DEFAULT '0' COMMENT '是否具备前向交叉交通预警功能（1=是，0=否）',
  `RCTA` tinyint(1) DEFAULT '0' COMMENT '是否具备后方交叉交通预警功能（1=是，0=否）',
  `AEB` tinyint(1) DEFAULT '0' COMMENT '是否具备自动紧急制动功能（1=是，0=否）',
  `ELKA` tinyint(1) DEFAULT '0' COMMENT '是否具备紧急车道保持辅助功能（1=是，0=否）',
  `ESS` tinyint(1) DEFAULT '0' COMMENT '是否具备紧急转向辅助功能（1=是，0=否）',
  `AES` tinyint(1) DEFAULT '0' COMMENT '是否具备自动紧急转向功能（1=是，0=否）',
  `FCTB` tinyint(1) DEFAULT '0' COMMENT '是否具备前向碰撞威胁制动功能（1=是，0=否）',
  `RCTB` tinyint(1) DEFAULT '0' COMMENT '是否具备后方交叉交通制动功能（1=是，0=否）',
  `LCC` tinyint(1) DEFAULT '0' COMMENT '是否具备车道居中控制功能（1=是，0=否）',
  `TJA` tinyint(1) DEFAULT '0' COMMENT '是否具备交通拥堵辅助功能（1=是，0=否）',
  `HWA` tinyint(1) DEFAULT '0' COMMENT '是否具备高速公路辅助功能（1=是，0=否）',
  `Urban_Commute` tinyint(1) DEFAULT '0' COMMENT '是否具备城市通勤辅助功能（1=是，0=否）',
  `HC` tinyint(1) DEFAULT '0' COMMENT '是否具备高阶智驾(Highchauffeur)功能（1=是，0=否）',
  `H-NOP_Lite` tinyint(1) DEFAULT '0' COMMENT '是否具备高速领航辅助(精简版)功能（1=是，0=否）',
  `H-NOP_Full` tinyint(1) DEFAULT '0' COMMENT '是否具备高速领航辅助(完整版)功能（1=是，0=否）',
  `U_NOP` tinyint(1) DEFAULT '0' COMMENT '是否具备城市领航辅助功能（1=是，0=否）',
  `TJC` tinyint(1) DEFAULT '0' COMMENT '是否具备交通拥堵协同功能（1=是，0=否）',
  `D2D` tinyint(1) DEFAULT '0' COMMENT '是否具备车对车通信功能（1=是，0=否）',
  `system_solution_ID` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `system_solution_ID_UNIQUE` (`system_solution_ID`),
  KEY `fk_solution_euf_group_system_solution1_idx` (`system_solution_ID`),
  CONSTRAINT `fk_solution_euf_group_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ADAS功能配置表（标记功能是否具备）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution_euf_group`
--

LOCK TABLES `solution_euf_group` WRITE;
/*!40000 ALTER TABLE `solution_euf_group` DISABLE KEYS */;
INSERT INTO `solution_euf_group` VALUES (4,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,3),(5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,0,1,0,0,0,4);
/*!40000 ALTER TABLE `solution_euf_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution_interface`
--

DROP TABLE IF EXISTS `solution_interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solution_interface` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Interface_Number` int DEFAULT NULL,
  `Property` varchar(45) DEFAULT NULL,
  `Type` varchar(45) NOT NULL,
  `SubType` varchar(45) NOT NULL,
  `ecu_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_interface_interface_enum1_idx` (`Type`),
  KEY `fk_interface_interface_enum_sub1_idx` (`SubType`),
  KEY `fk_solution_interface_ecu1_idx` (`ecu_ID`),
  CONSTRAINT `fk_interface_interface_enum10` FOREIGN KEY (`Type`) REFERENCES `interface_enum` (`TYPE_VALUE`),
  CONSTRAINT `fk_interface_interface_enum_sub10` FOREIGN KEY (`SubType`) REFERENCES `interface_enum_sub` (`SUBTYPE_VALUE`),
  CONSTRAINT `fk_solution_interface_ecu1` FOREIGN KEY (`ecu_ID`) REFERENCES `ecu` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution_interface`
--

LOCK TABLES `solution_interface` WRITE;
/*!40000 ALTER TABLE `solution_interface` DISABLE KEYS */;
INSERT INTO `solution_interface` VALUES (59,8,'、、','CAN','CAN_FD',0),(60,2,'//','FLEXRAY','FLEXRAY',0),(61,4,'//','VIDEO','LVDS',0),(62,4,'///','CAN','CAN_FD',1),(63,1,'FLEXRAY','FLEXRAY','FLEXRAY',1),(64,4,'///','CAN','CAN_FD',3),(65,2,'///','FLEXRAY','FLEXRAY',3);
/*!40000 ALTER TABLE `solution_interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution_tags_input`
--

DROP TABLE IF EXISTS `solution_tags_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solution_tags_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `tags_Tag` varchar(45) NOT NULL,
  `system_solution_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_solution_tags_input_tags1_idx` (`tags_Tag`),
  KEY `fk_solution_tags_input_system_solution1_idx` (`system_solution_ID`),
  CONSTRAINT `fk_solution_tags_input_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`),
  CONSTRAINT `fk_solution_tags_input_tags1` FOREIGN KEY (`tags_Tag`) REFERENCES `techpoint` (`Tag`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution_tags_input`
--

LOCK TABLES `solution_tags_input` WRITE;
/*!40000 ALTER TABLE `solution_tags_input` DISABLE KEYS */;
INSERT INTO `solution_tags_input` VALUES (1,'行泊分体',3),(3,'行泊分体',4);
/*!40000 ALTER TABLE `solution_tags_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status_enum`
--

DROP TABLE IF EXISTS `status_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_enum` (
  `VALUE` varchar(45) NOT NULL,
  PRIMARY KEY (`VALUE`),
  UNIQUE KEY `STATUS_UNIQUE` (`VALUE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_enum`
--

LOCK TABLES `status_enum` WRITE;
/*!40000 ALTER TABLE `status_enum` DISABLE KEYS */;
INSERT INTO `status_enum` VALUES ('IN PLAN'),('IN SOP'),('UNDER DEV');
/*!40000 ALTER TABLE `status_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storage_unit`
--

DROP TABLE IF EXISTS `storage_unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `storage_unit` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Type` varchar(50) NOT NULL,
  `SubType` varchar(50) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Size` varchar(45) DEFAULT NULL,
  `Unit` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `uk_memory_unit_calculator` (`ID`,`SubType`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_Storage_Unit_suppliers1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_Storage_Unit_suppliers1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storage_unit`
--

LOCK TABLES `storage_unit` WRITE;
/*!40000 ALTER TABLE `storage_unit` DISABLE KEYS */;
INSERT INTO `storage_unit` VALUES (2,'Flash Memory','eMMC','Samsung KLM8G1GEME-B041','8','GB','Samsung'),(3,'Flash Memory','eMMC','Samsung KLM32G1GEME-B041','32','GB','Samsung'),(4,'Flash Memory','UFS 2.1','Samsung KLUCG4J1ED-B0C1','128','GB','Samsung'),(5,'Flash Memory','SPI NOR Flash','Samsung K8F1315UQC-BC00','16','MB','Samsung'),(6,'Flash Memory','eMMC','Kioxia THGBMFG9C1LBAIL','16','GB','Kioxia'),(7,'Flash Memory','eMMC','Kioxia THGBMHG8C4LBAIR','64','GB','Kioxia'),(8,'Flash Memory','SPI NAND Flash','Kioxia TC58NVG0S3HTA00','1','GB','Kioxia'),(9,'Flash Memory','UFS 3.1','Kioxia KLUFG8R1EA-B0E1','256','GB','Kioxia'),(10,'Flash Memory','SPI NOR Flash','Micron N25Q064A13ESF40F','8','MB','Micron'),(11,'Flash Memory','eMMC','Micron MTFC8GACAAAE-4M IT','8','GB','Micron'),(12,'Flash Memory','UFS 2.2','Micron MTFDKBA256TFS-1BC1ZABYY','256','GB','Micron');
/*!40000 ALTER TABLE `storage_unit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (4,'中间层软件'),(1,'产品定义'),(2,'功能设计'),(5,'应用层软件'),(3,'底层软件'),(6,'整车架构');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subobjects`
--

DROP TABLE IF EXISTS `subobjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subobjects` (
  `OBJECT` varchar(45) NOT NULL,
  `NAME` varchar(45) DEFAULT NULL,
  `ID` varchar(45) DEFAULT NULL,
  `CN` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`OBJECT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subobjects`
--

LOCK TABLES `subobjects` WRITE;
/*!40000 ALTER TABLE `subobjects` DISABLE KEYS */;
INSERT INTO `subobjects` VALUES ('app','Name','ID','应用层软件'),('country','Name','ID','国家列表'),('digitalmap','Name','ID','电子地图'),('ethernet_switch','Name','ID','交换机'),('function_features','Name','ID','子功能'),('image_sensors','Name','ID','图像传感器'),('lens','Name','ID','光学镜头'),('serializers','Name','ID','加串器'),('storage_unit','Name','ID','存储单元'),('usecases','Name','ID','使用场景'),('vehicle_mark','Name','ID','汽车品牌');
/*!40000 ALTER TABLE `subobjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `Name` varchar(45) NOT NULL,
  `CN_Name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES ('ADI','亚德诺'),('Aptiv','安波福'),('Audiowell','奥迪威'),('AutoNavi','高德'),('Baidu','百度'),('Blackberry','黑莓'),('Bosch','博世'),('Chuhang Technology','楚航科技'),('Continental','大陆'),('Daimler','戴姆勒'),('Denso','电装'),('Desay','德赛'),('GalaxyCore','格科微'),('GEELY','吉利'),('Google','谷歌'),('GreenHills','GreenHills'),('HERE','HERE'),('HESAI','禾赛'),('HorizonRobotics','地平线'),('Hsell','Hsell'),('HUAWEI','华为'),('Innovusion','图达通'),('Kioxia','铠侠'),('LiAuto','理想汽车'),('LimRadar','黎明瑞达'),('Longhorn','豪恩'),('Marvell','美满'),('Maxieye','智驾科技'),('Maxim Integrated','美信半导体'),('Maxintergrated','美信半导体'),('Micron','镁光'),('Minieye','佑驾创新'),('Mobileye','摩安视'),('Momenta','魔门塔'),('MuniuTech','木牛科技'),('Murata','村田'),('NanoRadar','纳雷科技'),('Navinfo','四维图新'),('Nikon','尼康'),('NIO','蔚来汽车'),('NVIDIA','英伟达'),('NXP','恩智浦'),('OmniVision','豪威'),('ON-Semi','安森美'),('OpenSource','开源'),('QualComm','高通'),('Renesas','瑞萨'),('Robosense','速腾聚创'),('Ronghua','荣华科技'),('Samsung','三星'),('SenseTime','商汤'),('SmartSens','思特威'),('Sony','索尼'),('ST','意法半导体'),('Stellantis','斯特兰提斯'),('Sunny','舜宇光学'),('Tecent','腾讯'),('Tesla','特斯拉'),('Tesoo Optical','特索光电'),('TI','德州仪器'),('TomTom','TomTom'),('TowinLens','拓唯电子'),('TRW','天合'),('Valeo','法雷奥'),('Vector','维克多汽车技术'),('Volvo','沃尔沃'),('Wide Area Radar','广域雷达'),('WintopLens','云泰光学'),('XAMV','维视智造'),('Yutong Jiuzhou','宇瞳玖洲'),('ZF','采埃孚');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supportobjects`
--

DROP TABLE IF EXISTS `supportobjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supportobjects` (
  `OBJECT` varchar(45) NOT NULL,
  `NAME` varchar(45) DEFAULT NULL,
  `ID` varchar(45) DEFAULT NULL,
  `CN` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`OBJECT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supportobjects`
--

LOCK TABLES `supportobjects` WRITE;
/*!40000 ALTER TABLE `supportobjects` DISABLE KEYS */;
INSERT INTO `supportobjects` VALUES ('country','Name','ID','国家列表'),('deliverable_content','Name','ID','产出物'),('knowledge_content','Name','ID','知识点'),('suppliers','Name','ID','厂商名称');
/*!40000 ALTER TABLE `supportobjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_solution`
--

DROP TABLE IF EXISTS `system_solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_solution` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) NOT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `STATUS` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_system_solution_suppliers1_idx` (`Supplier_Name`),
  KEY `fk_system_solution_status_enum1_idx` (`STATUS`),
  CONSTRAINT `fk_system_solution_status_enum1` FOREIGN KEY (`STATUS`) REFERENCES `status_enum` (`VALUE`),
  CONSTRAINT `fk_system_solution_suppliers1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_solution`
--

LOCK TABLES `system_solution` WRITE;
/*!40000 ALTER TABLE `system_solution` DISABLE KEYS */;
INSERT INTO `system_solution` VALUES (3,'VSS360','Valeo','IN SOP'),(4,'Valeo 2 Box','Valeo','IN SOP');
/*!40000 ALTER TABLE `system_solution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `techpoint`
--

DROP TABLE IF EXISTS `techpoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `techpoint` (
  `Tag` varchar(45) NOT NULL,
  PRIMARY KEY (`Tag`),
  UNIQUE KEY `Tag_UNIQUE` (`Tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `techpoint`
--

LOCK TABLES `techpoint` WRITE;
/*!40000 ALTER TABLE `techpoint` DISABLE KEYS */;
INSERT INTO `techpoint` VALUES ('两段式端到端'),('分体式'),('域控式'),('无图方案'),('智能前视'),('端到端'),('舱驾一体'),('舱驾泊一体'),('行泊一体'),('行泊分体');
/*!40000 ALTER TABLE `techpoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test_enum`
--

DROP TABLE IF EXISTS `test_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test_enum` (
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`Name`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test_enum`
--

LOCK TABLES `test_enum` WRITE;
/*!40000 ALTER TABLE `test_enum` DISABLE KEYS */;
INSERT INTO `test_enum` VALUES ('ANCAP'),('ASEAN NCAP'),('Bharat NCAP'),('C-IAC'),('C-NCAP'),('C_ICAP'),('Euro NCAP'),('i-VISTA'),('IHS'),('JNCAP'),('K-NCAP'),('Latin NCAP');
/*!40000 ALTER TABLE `test_enum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usecases`
--

DROP TABLE IF EXISTS `usecases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usecases` (
  `ID` int NOT NULL,
  `Definition` varchar(45) DEFAULT NULL,
  `Pre_Condition` varchar(45) DEFAULT NULL,
  `Trigger_condition` varchar(45) DEFAULT NULL,
  `function_features_ID` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_usecases_function_features1_idx` (`function_features_ID`),
  CONSTRAINT `fk_usecases_function_features1` FOREIGN KEY (`function_features_ID`) REFERENCES `function_features` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usecases`
--

LOCK TABLES `usecases` WRITE;
/*!40000 ALTER TABLE `usecases` DISABLE KEYS */;
/*!40000 ALTER TABLE `usecases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uss`
--

DROP TABLE IF EXISTS `uss`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uss` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Max_Detection_Range` float DEFAULT NULL,
  `Min_Detection_Range` float DEFAULT NULL,
  `Distance_Resolution` float DEFAULT NULL,
  `Distance_Precision` float DEFAULT NULL,
  `Horizontal_FOV` float DEFAULT NULL,
  `Vertical_FOV` float DEFAULT NULL,
  `Frequency` float DEFAULT NULL,
  `Sensor_diamter` float DEFAULT NULL,
  `Supplier_Name` varchar(45) DEFAULT NULL,
  `MAX_TEMP` float DEFAULT NULL,
  `MIN_TEMP` float DEFAULT NULL,
  `Working_Temperature` varchar(45) GENERATED ALWAYS AS (concat(`MIN_TEMP`,_utf8mb4'°~',`MAX_TEMP`,_utf8mb4'°')) VIRTUAL,
  `IP_Level` varchar(45) DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_uss_suppliers_enum1_idx` (`Supplier_Name`),
  KEY `fk_uss_ip_level_enum1_idx` (`IP_Level`),
  CONSTRAINT `fk_uss_ip_level_enum1` FOREIGN KEY (`IP_Level`) REFERENCES `ip_level_enum` (`LEVEL`),
  CONSTRAINT `fk_uss_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uss`
--

LOCK TABLES `uss` WRITE;
/*!40000 ALTER TABLE `uss` DISABLE KEYS */;
INSERT INTO `uss` (`ID`, `Name`, `Max_Detection_Range`, `Min_Detection_Range`, `Distance_Resolution`, `Distance_Precision`, `Horizontal_FOV`, `Vertical_FOV`, `Frequency`, `Sensor_diamter`, `Supplier_Name`, `MAX_TEMP`, `MIN_TEMP`, `IP_Level`, `Type`) VALUES (1,'UPA-362F',3.5,0.5,0.01,0.02,140,60,25,18,'Bosch',85,-40,'IP67','UPA'),(2,'U5-Serie',5.5,0.15,0.01,0.05,180,60,25,22,'Bosch',85,-40,'IP67','APA'),(3,'U6',6.5,0.15,0.01,0.05,180,60,25,20,'Bosch',85,-40,'IP67','APA'),(4,'UPA Gen3',2.5,0.15,0.005,0.005,140,60,25,16,'Valeo',85,-40,'IP67','UPA'),(5,'USV10',5,0.1,0.01,0.02,120,60,50,18,'Bosch',85,-40,'IP6K9K','APA'),(6,'AK2',7,0.1,0.01,0.02,120,80,25,22,'Longhorn',85,-40,'IP67','APA'),(7,'Standard-UPA',2.5,0.15,0.01,0.02,140,60,25,18,'Longhorn',85,-40,'IP67','UPA'),(8,'AK2-Audiowell',7,0.1,0.01,0.03,120,80,25,20,'Audiowell',85,-40,'IP67','UPA'),(9,'TC-Serie',5.2,0.15,0.02,0.01,140,60,25,20,'Murata',95,-40,'IP67','UPA');
/*!40000 ALTER TABLE `uss` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uss_input`
--

DROP TABLE IF EXISTS `uss_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uss_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `system_solution_ID` int NOT NULL,
  `Uss_Name` varchar(45) NOT NULL,
  `POSITION` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_uss_input_system_solution1_idx` (`system_solution_ID`),
  KEY `fk_uss_input_uss1_idx` (`Uss_Name`),
  KEY `fk_uss_input_position_enum1_idx` (`POSITION`),
  CONSTRAINT `fk_uss_input_position_enum1` FOREIGN KEY (`POSITION`) REFERENCES `position_enum` (`POSITION`),
  CONSTRAINT `fk_uss_input_system_solution1` FOREIGN KEY (`system_solution_ID`) REFERENCES `system_solution` (`ID`),
  CONSTRAINT `fk_uss_input_uss1` FOREIGN KEY (`Uss_Name`) REFERENCES `uss` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uss_input`
--

LOCK TABLES `uss_input` WRITE;
/*!40000 ALTER TABLE `uss_input` DISABLE KEYS */;
/*!40000 ALTER TABLE `uss_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_mark`
--

DROP TABLE IF EXISTS `vehicle_mark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_mark` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `CN_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_mark`
--

LOCK TABLES `vehicle_mark` WRITE;
/*!40000 ALTER TABLE `vehicle_mark` DISABLE KEYS */;
INSERT INTO `vehicle_mark` VALUES (1,'Alfa Romeo','阿尔法·罗密欧'),(2,'Aston Martin','阿斯顿·马丁'),(3,'Audi','奥迪'),(4,'AION','埃安'),(5,'Aiways','爱驰'),(6,'Avatr','阿维塔'),(7,'AITO','问界'),(8,'Alpine','阿尔卑斯'),(9,'Ankai','安凯客车'),(10,'Baojun','宝骏'),(11,'BMW','宝马'),(12,'Mercedes-Benz','奔驰'),(13,'BYD','比亚迪'),(14,'BAIC','北汽制造'),(15,'Beijing Auto Senova','北汽绅宝'),(16,'BAIC Huansu','北汽幻速'),(17,'BAIC Weifang','北汽威旺'),(18,'BAIC Changhe','北汽昌河'),(19,'BAIC New Energy','北汽新能源'),(20,'Borgward','宝沃'),(21,'Baizhi New Energy','百智新能源'),(22,'Bick Motor','比克汽车'),(23,'Borrego','博郡汽车'),(24,'Bugatti','布加迪'),(25,'Pininfarina','宾尼法利纳'),(26,'Proton','宝腾'),(27,'Bosch','博世'),(28,'Bentley','宾利'),(29,'Changan','长安'),(30,'NEVO','长安启源'),(31,'Chang\'an Oushang','长安欧尚'),(32,'Changan Kaicheng','长安凯程'),(33,'Great Wall','长城'),(34,'Great Wall Pao','长城炮'),(35,'Trumpchi','传祺'),(36,'Skyworth Auto','创维汽车'),(37,'Cao Cao','曹操汽车'),(38,'Changhe','昌河'),(39,'Volkswagen','大众'),(40,'Dodge','道奇'),(41,'Dongfeng Motor','东风'),(42,'Dongfeng Fengshen','东风风神'),(43,'Dongfeng Yipai','东风奕派'),(44,'Dongfeng Fukang','东风富康'),(45,'Dongfeng Fengxing','东风风行'),(46,'Dongfeng Xiaokang','东风小康'),(47,'Venucia','启辰'),(48,'Dongfeng Zhengzhou Nissan','东风郑州日产'),(49,'Dongfeng Fengguang','东风风光'),(50,'Dongfeng Fengdu','东风风度'),(51,'Soueast','东南'),(52,'Dika','电咖'),(53,'Ferrari','法拉利'),(54,'Fiat','菲亚特'),(55,'Ford','福特'),(56,'Foton','福田'),(57,'HiPhi','高合'),(58,'GAC','广汽'),(59,'Haval','哈弗'),(60,'Hongqi','红旗'),(61,'Huatai','华泰'),(62,'Haima','海马'),(63,'Hanma','汉腾'),(64,'Huanghai','黄海汽车'),(65,'Hafei','哈飞'),(66,'Hengchi','恒驰'),(67,'Infiniti','英菲尼迪'),(68,'Geely','吉利'),(69,'Zeekr','极氪'),(70,'Jiyue','极越'),(71,'Geometry','几何'),(72,'Jaguar','捷豹'),(73,'Genesis','捷尼赛思'),(74,'Jetta','捷达'),(75,'Jetour','捷途'),(76,'Jeep','吉普'),(77,'ARCFOX','极狐'),(78,'JAC','江淮'),(79,'JAC Yiwei','江淮钇为'),(80,'King Long','金龙'),(81,'Jinbei','金杯'),(82,'Jidu','集度'),(83,'Cadillac','凯迪拉克'),(84,'Chery Kairui','开瑞'),(85,'Chrysler','克莱斯勒'),(86,'Koenigsegg','科尼赛克'),(87,'Cayenne','凯翼'),(88,'Lamborghini','兰博基尼'),(89,'Lancia','蓝旗亚'),(90,'Lexus','雷克萨斯'),(91,'Lynk & Co','领克'),(92,'Lincoln','林肯'),(93,'Suzuki','铃木'),(94,'Li Auto','理想'),(95,'Land Rover','路虎'),(96,'Lotus','路特斯'),(97,'Lifan','力帆'),(98,'Landwind','陆风'),(99,'Renault','雷诺'),(100,'Rolls-Royce','劳斯莱斯'),(101,'Leding','雷丁'),(102,'Mazda','马自达'),(103,'Maserati','玛莎拉蒂'),(104,'Maybach','迈巴赫'),(105,'MG','名爵'),(106,'Morgan','摩根'),(107,'Mitsubishi','三菱'),(108,'Luxgen','纳智捷'),(109,'Nezha','哪吒'),(110,'Nissan','日产'),(111,'Opel','欧宝'),(112,'ORA','欧拉'),(113,'Pagani','保时捷'),(114,'Porsche','保时捷'),(115,'Peugeot','标致'),(116,'Chery','奇瑞'),(117,'Chery New Energy','奇瑞新能源'),(118,'KIA','起亚'),(119,'Roewe','荣威'),(120,'Ruichi New Energy','瑞驰新能源'),(121,'Saab','萨博'),(122,'SERES','赛力斯'),(123,'Skoda','斯柯达'),(124,'Subaru','斯巴鲁'),(125,'SAIC Maxus','上汽大通'),(126,'SRM Xinyuan','SRM鑫源'),(127,'Spyker','世爵'),(128,'SsangYong','双龙'),(129,'Startech','斯达泰克'),(130,'Steyr','斯太尔'),(131,'Tesla','特斯拉'),(132,'Denza','腾势'),(133,'Tank','坦克'),(134,'Yutong','宇通'),(135,'Volvo','沃尔沃'),(136,'Wuling','五菱'),(137,'Isuzu','五十铃'),(138,'WEY','魏牌'),(139,'WM Motor','威马'),(140,'NIO','蔚来'),(141,'Riich','威麟'),(142,'Weichai Yizhi','潍柴英致'),(143,'Xpeng','小鹏'),(144,'Chevrolet','雪佛兰'),(145,'Hyundai','现代'),(146,'Yunque','云雀'),(147,'Yuanhang','远航汽车'),(148,'Mustang','野马'),(149,'Jonway','永源'),(150,'Zotye','众泰'),(151,'Zhonghua','中华'),(152,'Zhongxing','中兴'),(153,'IM','智己'),(154,'Jishi','极石'),(155,'Oldsmobile','奥兹莫比尔'),(156,'Pontiac','庞蒂亚克'),(157,'Saturn','土星'),(158,'Mercury','水星'),(159,'Holden','霍顿'),(160,'Daihatsu','大发'),(161,'Shelby','西贝尔'),(162,'Dacia','达西亚'),(163,'Scion','赛恩'),(164,'Aspark','阿斯帕克'),(165,'Tata','塔塔'),(166,'Seat','西亚特'),(167,'Trabant','特拉贝特'),(168,'Volga','伏尔加'),(169,'GAZ','嘎斯'),(170,'Rover','罗孚'),(171,'Abarth','阿巴斯'),(172,'Wiesmann','威兹曼'),(173,'McLaren','迈凯伦'),(174,'Apollo','阿波罗'),(175,'Ducati','杜卡迪'),(176,'Renault Samsung','雷诺三星'),(177,'Lister','利斯特'),(178,'TVR','特威尔'),(179,'Vauxhall','沃克斯豪尔'),(180,'Smart','智马达');
/*!40000 ALTER TABLE `vehicle_mark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_test_input`
--

DROP TABLE IF EXISTS `vehicle_test_input`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_test_input` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Test_Name` varchar(45) NOT NULL,
  `vehiclemodel_ID` int NOT NULL,
  `Score` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_vehicle_test_input_vehiclemodel1_idx` (`vehiclemodel_ID`),
  KEY `fk_vehicle_test_input_test_enum1_idx` (`Test_Name`),
  CONSTRAINT `fk_vehicle_test_input_test_enum1` FOREIGN KEY (`Test_Name`) REFERENCES `test_enum` (`Name`),
  CONSTRAINT `fk_vehicle_test_input_vehiclemodel1` FOREIGN KEY (`vehiclemodel_ID`) REFERENCES `vehiclemodel` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_test_input`
--

LOCK TABLES `vehicle_test_input` WRITE;
/*!40000 ALTER TABLE `vehicle_test_input` DISABLE KEYS */;
INSERT INTO `vehicle_test_input` VALUES (1,'Euro NCAP',1,'5 Stars');
/*!40000 ALTER TABLE `vehicle_test_input` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_type`
--

DROP TABLE IF EXISTS `vehicle_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_type` (
  `Name` varchar(45) NOT NULL,
  `CN_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Name`),
  UNIQUE KEY `Type_UNIQUE` (`Name`),
  UNIQUE KEY `CN_Name_UNIQUE` (`CN_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_type`
--

LOCK TABLES `vehicle_type` WRITE;
/*!40000 ALTER TABLE `vehicle_type` DISABLE KEYS */;
INSERT INTO `vehicle_type` VALUES ('Sedan','三箱轿车'),('Hatchback','两项轿车'),('Truck','卡车'),('Van','厢型车'),('MPV','多用途汽车'),('Mini Car','微型车'),('Station Wagon','旅行车'),('Shooting Brake','猎装车'),('Pickup Truck','皮卡车'),('Off-road Vehicle','越野车'),('SUV','运动型多用途汽车');
/*!40000 ALTER TABLE `vehicle_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehiclemodel`
--

DROP TABLE IF EXISTS `vehiclemodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehiclemodel` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Brand` varchar(45) NOT NULL,
  `Adas_Solution` varchar(45) NOT NULL,
  `Variant_Name` varchar(45) NOT NULL,
  `FullDescription` varchar(45) GENERATED ALWAYS AS (concat(`Name`,`Adas_Solution`,`Variant_Name`)) VIRTUAL,
  `Project_Code` varchar(45) DEFAULT NULL,
  `EE_Archi` varchar(45) DEFAULT 'Null',
  `EPS_Supplier_Name` varchar(45) NOT NULL,
  `Power_Supplier_Name` varchar(45) NOT NULL,
  `Braking_Supplier_Name` varchar(45) NOT NULL,
  `Launch_Time` varchar(45) DEFAULT NULL,
  `CN_Name` varchar(45) DEFAULT NULL,
  `Vehicle_Seats_Number` int DEFAULT NULL,
  `Adas_Product_Name` varchar(100) NOT NULL,
  `PowerType` varchar(45) NOT NULL,
  `VehicleType` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `FullDescription_UNIQUE` (`FullDescription`),
  KEY `fk_VehicleModel_system_solution1_idx` (`Adas_Solution`),
  KEY `fk_vehiclemode_vehicle_mark_idx` (`Brand`),
  KEY `fk_vehiclemodel_suppliers1_idx` (`EPS_Supplier_Name`),
  KEY `fk_vehiclemodel_suppliers2_idx` (`Power_Supplier_Name`),
  KEY `fk_vehiclemodel_suppliers3_idx` (`Braking_Supplier_Name`),
  KEY `fk_vehiclemodel_adas_product_name1_idx` (`Adas_Product_Name`),
  KEY `fk_vehiclemodel_power_type1_idx` (`PowerType`),
  KEY `fk_vehiclemodel_vehicle_type1_idx` (`VehicleType`),
  CONSTRAINT `fk_vehiclemode_vehicle_mark` FOREIGN KEY (`Brand`) REFERENCES `vehicle_mark` (`Name`),
  CONSTRAINT `fk_vehiclemodel_adas_product_name1` FOREIGN KEY (`Adas_Product_Name`) REFERENCES `adas_product_name_enum` (`Type`),
  CONSTRAINT `fk_vehiclemodel_power_type1` FOREIGN KEY (`PowerType`) REFERENCES `power_type` (`Name`),
  CONSTRAINT `fk_vehiclemodel_suppliers1` FOREIGN KEY (`EPS_Supplier_Name`) REFERENCES `suppliers` (`Name`),
  CONSTRAINT `fk_vehiclemodel_suppliers2` FOREIGN KEY (`Power_Supplier_Name`) REFERENCES `suppliers` (`Name`),
  CONSTRAINT `fk_vehiclemodel_suppliers3` FOREIGN KEY (`Braking_Supplier_Name`) REFERENCES `suppliers` (`Name`),
  CONSTRAINT `fk_VehicleModel_system_solution1` FOREIGN KEY (`Adas_Solution`) REFERENCES `system_solution` (`Name`),
  CONSTRAINT `fk_vehiclemodel_vehicle_type1` FOREIGN KEY (`VehicleType`) REFERENCES `vehicle_type` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehiclemodel`
--

LOCK TABLES `vehiclemodel` WRITE;
/*!40000 ALTER TABLE `vehiclemodel` DISABLE KEYS */;
INSERT INTO `vehiclemodel` (`ID`, `Name`, `Brand`, `Adas_Solution`, `Variant_Name`, `Project_Code`, `EE_Archi`, `EPS_Supplier_Name`, `Power_Supplier_Name`, `Braking_Supplier_Name`, `Launch_Time`, `CN_Name`, `Vehicle_Seats_Number`, `Adas_Product_Name`, `PowerType`, `VehicleType`) VALUES (1,'Smart No.3','Smart','VSS360','/','HC11','GEA 2.0','ZF','Bosch','Bosch','2023','豪情精灵3号',5,'G-PILOT 3.0','BEV','Hatchback'),(2,'XC70','Volvo','Valeo 2 Box','/','V446K','GEA 2.0','ZF','Bosch','Bosch','2025','XC70',5,'G-PILOT 3.0','BEV','SUV');
/*!40000 ALTER TABLE `vehiclemodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `version_management`
--

DROP TABLE IF EXISTS `version_management`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `version_management` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Major_Version` varchar(45) NOT NULL,
  `Minor_Version_Year` int NOT NULL,
  `Temp_Version` int NOT NULL,
  `Version` varchar(45) GENERATED ALWAYS AS (concat(`Major_Version`,_utf8mb3'-',`Minor_Version_Year`,_utf8mb3'-',`Minor_Version_Month`,_utf8mb3'-',`Temp_Version`)) VIRTUAL,
  `Version_Time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Minor_Version_Month` int NOT NULL,
  `Release_Status` varchar(45) DEFAULT NULL,
  `BackEndToGit` varchar(45) DEFAULT NULL,
  `GitToServer` varchar(45) DEFAULT NULL,
  `DarkerToGit` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Version_UNIQUE` (`Version`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `version_management`
--

LOCK TABLES `version_management` WRITE;
/*!40000 ALTER TABLE `version_management` DISABLE KEYS */;
INSERT INTO `version_management` (`ID`, `Major_Version`, `Minor_Version_Year`, `Temp_Version`, `Version_Time`, `Minor_Version_Month`, `Release_Status`, `BackEndToGit`, `GitToServer`, `DarkerToGit`) VALUES (1,'ALPHA',25,1,'2025-12-06 15:52:29',11,'Done','Done','Done','Done'),(2,'Alpha',25,1,'2025-12-11 06:33:27',12,'Done','Done','Done','Done'),(90,'Alpha',25,2,'2025-12-11 06:48:08',12,'Done','Done','Done','Done'),(91,'Alpha',25,3,'2025-12-11 07:31:39',12,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `version_management` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work`
--

DROP TABLE IF EXISTS `work`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Description` text,
  `isPrimary` varchar(45) DEFAULT NULL,
  `Metiers` varchar(45) NOT NULL,
  `Subject` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `nameindex` (`Name`),
  KEY `fk_work_Metiers1_idx` (`Metiers`),
  KEY `fk_work_subject1_idx` (`Subject`),
  CONSTRAINT `fk_work_Metiers1` FOREIGN KEY (`Metiers`) REFERENCES `metiers` (`Name`),
  CONSTRAINT `fk_work_subject1` FOREIGN KEY (`Subject`) REFERENCES `subject` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work`
--

LOCK TABLES `work` WRITE;
/*!40000 ALTER TABLE `work` DISABLE KEYS */;
INSERT INTO `work` VALUES (1,'用户功能定义','明确用户功能是什么？这个功能是要做什么的？给出一个边界和框架为后续的开发做工起头。例如定义ACC功能,为辅助车辆进行车辆的纵向运动控制,只能进行缓加速缓减速的情况下保持车辆匀速行驶且能避免和前方车辆的碰撞','YES','产品工程师','产品定义'),(2,'行业对标','对市场上的ADAS产品针对不同的功能进行对标','NO','产品工程师','产品定义');
/*!40000 ALTER TABLE `work` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_from`
--

DROP TABLE IF EXISTS `work_from`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_from` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `work_ID` int NOT NULL,
  `isFROM` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_work_from_work1_idx` (`work_ID`),
  KEY `fk_work_from_work2_idx` (`isFROM`),
  CONSTRAINT `fk_work_from_work1` FOREIGN KEY (`work_ID`) REFERENCES `work` (`ID`),
  CONSTRAINT `fk_work_from_work2` FOREIGN KEY (`isFROM`) REFERENCES `work` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_from`
--

LOCK TABLES `work_from` WRITE;
/*!40000 ALTER TABLE `work_from` DISABLE KEYS */;
INSERT INTO `work_from` VALUES (2,2,'用户功能定义');
/*!40000 ALTER TABLE `work_from` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'darkerdatabase'
--

--
-- Dumping routines for database 'darkerdatabase'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-11 15:32:06
