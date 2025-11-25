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
  `Domain` varchar(45) NOT NULL,
  `Fusa_Level` varchar(45) NOT NULL,
  `Type` varchar(45) NOT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
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
  CONSTRAINT `fk_calculator_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers_enum` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calculator`
--

LOCK TABLES `calculator` WRITE;
/*!40000 ALTER TABLE `calculator` DISABLE KEYS */;
INSERT INTO `calculator` VALUES (1,'TDA4-VM-PLUS','The TDA4VM processor family targeted at ADAS and Autonomous Vehicle (AV) applications and built on extensive market knowledge accumulated over a decade of TI’s leadership in the ADAS processor market. The unique combination high-performance compute, deep-learning engine, dedicated accelerators for signal and image processing in a functional safety compliant targeted architecture make the TDA4VM devices a great fit for several industrial applications, such as: Robotics, Machine Vision, Radar, and so on. ',0,105,-40,'ADAS','ASIL_D','SoC','TI'),(2,'QC8650P-AAAA','[QAM8650P is the next generation Qualcomm® Snapdragon®\nadvanced driver-assistance systems (ADAS) module designed\nfor superior performance and power efficiency.\nIt has been developed as a Safety Element out of\nContext (SEooC). The key components of the QAM8650P\nmodule include the SA8650P SoC, PMM8650AU (×4) power\nmanagement IC, third party power management]',1,105,-40,'ADAS','ASIL_D','SoC','QualComm'),(3,'RH850-U2A16','The RH850/U2A MCU is the first member of Renesas’ cross-domain MCUs, a new generation of automotive-control devices, designed to address the growing need to integrate multiple applications into a single chip to realize unified electronic control units (ECUs) for the evolving electrical/electronic architecture (E/E architecture). Based on 28 nanometer (nm) process technology, the 32-bit RH850/U2A automotive MCU builds on key functions from Renesas’ RH850/Px Series for chassis control and RH850/Fx Series for body control to deliver improved performance.',1,105,-40,'ADAS','ASIL_B','MCU','Renesas'),(4,'QC8620P','This the description for the 8620P chipset product',0,105,-40,'ADAS','ASIL_D','SoC','QualComm'),(5,'QC8775-AAAA','////',0,105,-40,'ADAS','ASIL_D','SIP','QualComm'),(6,'J2','///',0,105,-40,'ADAS','ASIL_B','SoC','HorizonRobotics'),(7,'J6E','///',0,105,-40,'ADAS','ASIL_D','SoC','HorizonRobotics'),(8,'EQ4M','///',0,105,-40,'ADAS','ASIL_D','SoC','Mobileye'),(9,'8888','',1,1,1,'IVI','ASIL_C','MCU','APTIV');
/*!40000 ALTER TABLE `calculator` ENABLE KEYS */;
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
  KEY `fk_camera_Image_sensors1_idx` (`Image_Sensor`),
  KEY `fk_camera_lens1_idx` (`Lens`),
  KEY `fk_camera_serializers1_idx` (`Serializer`),
  KEY `fk_camera_suppliers_enum1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_camera_Image_sensors1` FOREIGN KEY (`Image_Sensor`) REFERENCES `image_sensors` (`Name`),
  CONSTRAINT `fk_camera_lens1` FOREIGN KEY (`Lens`) REFERENCES `lens` (`Name`),
  CONSTRAINT `fk_camera_serializers1` FOREIGN KEY (`Serializer`) REFERENCES `serializers` (`Name`),
  CONSTRAINT `fk_camera_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers_enum` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `camera`
--

LOCK TABLES `camera` WRITE;
/*!40000 ALTER TABLE `camera` DISABLE KEYS */;
INSERT INTO `camera` VALUES (1,'CAM1','FISHEYE','IMX728','SF816WN','MAX96717F','Desay'),(5,'CAM 222','3','IMX728','SF816WN','MAX96717F','Valeo'),(6,'CAM SURRONG','PIN HOLE','IMX623','YTOT-MCP308','DS90UB971','Bosch');
/*!40000 ALTER TABLE `camera` ENABLE KEYS */;
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
-- Table structure for table `euf`
--

DROP TABLE IF EXISTS `euf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `euf` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Description` text,
  `fusa_enum_LEVEL` varchar(45) NOT NULL,
  `sae_enum_LEVEL` varchar(45) NOT NULL,
  `Full_Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `EUF_ID_UNIQUE` (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_euf_fusa_enum1_idx` (`fusa_enum_LEVEL`),
  KEY `fk_euf_sae_enum1_idx` (`sae_enum_LEVEL`),
  CONSTRAINT `fk_euf_fusa_enum1` FOREIGN KEY (`fusa_enum_LEVEL`) REFERENCES `fusa_enum` (`LEVEL`),
  CONSTRAINT `fk_euf_sae_enum1` FOREIGN KEY (`sae_enum_LEVEL`) REFERENCES `sae_enum` (`LEVEL`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `euf`
--

LOCK TABLES `euf` WRITE;
/*!40000 ALTER TABLE `euf` DISABLE KEYS */;
INSERT INTO `euf` VALUES (1,'ACC','This is the Adaptive Cruise Control Functinonality','ASIL_B','L1','Adaptive Cruise Control'),(2,'LKA','This is a user function which actively control the vehicle\'s lateral motion to avoide vechile from driving out of lane','ASIL_B','L0','Lane Keep Assist'),(3,'TSR','As a core ADAS feature, TSR uses a front-facing camera and AI algorithms to real-time detect traffic signs (e.g., speed limits, prohibitions, warnings) per traffic standards. It displays recognized info on the dashboard or HUD, alerts drivers to overspeeding, and collaborates with ACC/ISA for smarter cruising. While enhancing driving safety and compliance by reducing distractions, TSR is auxiliary—drivers must remain attentive, as harsh weather or obscured signs may affect accuracy.','ASIL_A','L0','Traffic Sign Recognition'),(4,'TLR','TLR is an ADAS feature using onboard cameras and AI algorithms to detect and interpret traffic light signals in real-time. The system identifies red, yellow, and green lights, displays their status on the dashboard/HUD, and provides visual/auditory alerts. It enhances safety by reducing driver distraction and enables smarter decisions at intersections. TLR also integrates with ACC and navigation for optimal speed adjustments and green wave predictions. Note: performance may degrade in poor weather or with obstructed lights—always remain attentive while driving.','ASIL_A','L0','Traffic Light Recognition'),(5,'ISA','XXXXXXX','ASIL_A','L0','Intelligent Speed Assist'),(6,'AHB','AHB is an ADAS feature that automatically switches between high and low beams to maximize visibility while preventing glare for other road users. Using a windshield-mounted camera, it detects oncoming vehicles\' headlights or preceding vehicles\' taillights and intelligently toggles between beam modes at speeds above 30km/h.','ASIL_A','L0','Adaptive High Beam'),(8,'EDR','Known as a car’s \"black box,\" EDR is an in-vehicle system that monitors and records critical vehicle data before, during, and after a collision or severe event (e.g., hard braking). Triggered by sudden acceleration changes, it captures speed, brake application, airbag deployment, throttle position, and steering angle for 5–20 seconds pre-event. Mandated in most regions (China, EU, US), the data aids accident investigation, liability determination, and vehicle safety improvements. It’s non-volatile, ensuring data retention even after power loss—purely objective for post-incident analysis.','QM','L0','Event Data Recorder'),(9,'ADB','ADB is an advanced ADAS lighting feature using matrix LED headlights and camera-based detection. It intelligently dims specific light segments to avoid dazzling oncoming/preceding vehicles, while keeping other areas illuminated with high beams. This maintains optimal nighttime visibility without compromising other road users’ safety, eliminating the \"on-off\" gap of basic AHB. ADB enhances driving comfort and reduces fatigue, typically available on mid-to-high-end vehicles. Note: It’s a driver aid—remain attentive to weather and road conditions.','ASIL_A','L0','Adaptive Driving Beam'),(10,'FCW','Automatic Emergency Braking (AEB) employs radar, lidar, and cameras to detect potential collisions. When it senses a threat and the driver doesn\'t respond, it first warns via visual and auditory signals. If there\'s no action, AEB automatically applies brakes, reducing collision severity or preventing crashes, thus enhancing road safety.','ASIL_B','L0','Front Collision Warning'),(11,'LDW','Lane Departure Warning function is to provide alert information to the driver while the vehicle is crossing the lane markers unintentionally','QM','L0','Lane Departure Warning'),(12,'SLCA','The ADAS system controls the vehicle\'s longitudianl motion and lateral motion to perform lane change manouver under driver\'s triggering','ASIL_A','L0','Semi Automatic Lane Change Assist'),(13,'H-NOP_Lite','NOP(Navigation on Pilot) is a integrated L2+ function which could provide Automated Driving Assist Under driver’s supervision (Hands On + Eyes On) within the Structural Road (Highway or Urban Express) from point A and point B (start point and destination defined by user) at full speed range (0-130 kph).\n\nNOP function including longitudinal, lateral control of the vehicle, and lane change assist (Full automatic, driver triggered and system suggested), which helps the driver to perform Automatic overtaking, Highway connections on top of the HWA functions today.','QM','L2+','Highway Navigation On Pilot Lite'),(14,'H-NOP_Full','NOP(Navigation on Pilot) is a integrated L2+ function which could provide Automated Driving Assist Under driver’s supervision (Hands On + Eyes On) within the Structural Road (Highway or Urban Express) from point A and point B (start point and destination defined by user) at full speed range (0-130 kph).\n\nNOP function including longitudinal, lateral control of the vehicle, and lane change assist (Full automatic, driver triggered and system suggested), which helps the driver to perform Automatic overtaking, Highway connections on top of the HWA functions today.','ASIL_B','L2+','Highway Navigation On Pilot Full.'),(15,'U-NOP','As an advanced ADAS feature, Urban NOP enables semi-autonomous driving in urban scenarios via navigation integration and sensor fusion. It autonomously handles following, lane-keeping, turns, and obstacle avoidance on urban arterials, adapting to traffic lights and congestion. Drivers remain responsible—must take over promptly when prompted. It enhances driving convenience while reducing urban commuting fatigue.','ASIL_B','L2++','Urban Navigation On Pilot'),(16,'TJC','TJC is a Level 3 autonomous driving feature designed for highway and motorway traffic jams, operating at speeds up to 60-80 km/h. As a \"Conditional Automation\" system, it allows drivers to fully disengage from driving tasks (both hands off the wheel and eyes off the road) while the vehicle autonomously handles acceleration, braking, lane keeping, and obstacle avoidance in congested conditions.','ASIL_B','L3','Traffic Jam Chauffeur'),(17,'D2D','This is a integrated functionality which allows the vehicle to driver from point A to point B without differentiating the scenarios, wheather is parking scenarsio or driving scenarios, whether is in public road or in parking garage.','ASIL_B','L2++','Door-to-Door');
/*!40000 ALTER TABLE `euf` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `function_features`
--

LOCK TABLES `function_features` WRITE;
/*!40000 ALTER TABLE `function_features` DISABLE KEYS */;
INSERT INTO `function_features` VALUES (1,'ACC_Basic','This the Basic feature of ACC function that controls the vehicle\'s longitudinal motion status according to the driver\'s input of set speed or the distance between ego vehicle and target vehicle.',1),(2,'ACC_Stop&Go','This feautre belongs to ACC functionality which enables the system to control the vehicle\'s dynamic motion status to stop and hold standstill then enables the vehicle to start.',1),(3,'TSR-Basic','This the basci feature of TSR function which captured and recognized the traffic signs and provide speed limit informations to the driver',3),(4,'TLR-Basic','This the main feature of TLF funationly which capture and recognize the traffic light and provides its semantic information.',4),(5,'ISA-Basic','This the main feature of the ISA functionality',5),(6,'AHB-Basic','This is the main feature of AHB functionality',6),(8,'EDR-Basic','This the main feature for EDR functionality',8),(9,'ADB-Basic','This is the main feature of ADB functionality',9),(10,'FCW-Basic','This is the main feature of FCW functionality',10),(11,'LDW-Basic','This is the main featrue for LDW funcationality',11),(12,'SLCA-Basic','This is the main feature for SLCA functionality',12),(13,'H-NOP_Lite-Basic','placeholders',13),(14,'H-NOP_Lite-MRM - SIL','placeholders',13),(15,'H-NOP_Full-MRM - SIL','XXXXXXX',14),(16,'H-NOP_Full-MRM - SST','XXXXX',14),(17,'U-NOP-Basic','XXXXXXXXXXXXXXX',15),(18,'TJC-Basic','This is the main fucntion for TJC functionality',16),(19,'D2D-Basic','This the only feature for D2D functionality',17),(20,'H-NOP_Full-MRM - AOT','This the automatic overtaking feature from function NOP which the system detecte the travel efficiency of different lanes and the surrongding environment situation to determine wether a lane change is needed to gain higher traval efficiency and wether the envinroment allows a safe lane change and eventually propose and execute a lane change manouver.',14);
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
  `Resolution` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `NAME_INDEX` (`Name`),
  KEY `fk_Image_sensors_suppliers_enum1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_Image_sensors_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers_enum` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_sensors`
--

LOCK TABLES `image_sensors` WRITE;
/*!40000 ALTER TABLE `image_sensors` DISABLE KEYS */;
INSERT INTO `image_sensors` VALUES (1,'1H1','8','QualComm'),(2,'IMX728','8','Sony'),(3,'ISX031','3','Sony'),(4,'IMX623','3','Sony');
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
  `Number` int DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface`
--

LOCK TABLES `interface` WRITE;
/*!40000 ALTER TABLE `interface` DISABLE KEYS */;
INSERT INTO `interface` VALUES (11,1,'///',1,'USB','USB 3.1'),(12,3,'4 Lanes',1,'VIDEO','MIPI CSI-2(C-PHY)'),(13,1,'4 Lane DSI',1,'VIDEO','MIPI DSI-2'),(14,1,' ',1,'VIDEO','DP'),(15,20,'CAN FD',1,'CAN','CAN_FD'),(16,2,'100Mbps',1,'ETHERNET','RGMII'),(17,11,'Normal SPI',1,'SPI','Dual-SPI'),(18,1,'///',1,'GENERAL','I2C'),(19,1,'///',1,'GENERAL','GPIO'),(20,1,'eMMC 5.1',1,'STORAGE','eMMC'),(21,12,'//',1,'GENERAL','UART'),(22,1,'???',2,'USB','USB 3.1'),(23,1,'???',2,'USB','USB 2.0'),(24,4,'???',2,'VIDEO','MIPI CSI-2(C-PHY)'),(25,8,'CAN FD',2,'CAN','CAN_FD'),(26,1,'100',2,'ETHERNET','RGMII'),(27,1,'???',2,'ETHERNET','SGMII'),(28,1,'SPI',2,'SPI','Octal-SPI'),(29,1,'???',2,'GENERAL','I2C'),(30,2,'UFS 3.1 gear 4',2,'STORAGE','UFS'),(31,1,'eMMC 5.1',2,'STORAGE','eMMC'),(32,1,'64B FIFO',2,'GENERAL','UART'),(33,16,'//',3,'USB','USB 2.0'),(34,1,'1000Mbps',3,'ETHERNET','SGMII'),(35,1,'100Mbps',3,'ETHERNET','HSGMII'),(36,2,'//',3,'FLEXRAY','FLEXRAY'),(37,12,'/',3,'LIN','LIN2.1'),(38,1,'/',3,'SPI','Dual-SPI'),(39,6,'MSPI',3,'SPI','Multi-Master SPI'),(40,1,'YES',3,'GENERAL','I2C'),(41,1,'32ch DMA',3,'STORAGE','DMA'),(42,0,'//',4,'AUDIO','USB 3.1'),(43,0,'D-PHYv1.2',4,'AUDIO','MIPI CSI-2 (D-PHY)'),(44,0,'/',4,'AUDIO','CAN_FD'),(45,0,'//',4,'AUDIO','RGMII'),(46,0,'//',4,'AUDIO','SGMII'),(47,0,'//',4,'AUDIO','Octal-SPI'),(48,10,' ',4,'GENERAL','I2C'),(49,2,'UFS3.1 gear 4',4,'STORAGE','eMMC'),(50,1,'eMMC5.1',4,'STORAGE','eMMC'),(51,1,'////',8,'SPI','Dual-SPI'),(52,3,'///',6,'VIDEO','MIPI CSI-2 (D-PHY)'),(53,2,'///',6,'CAN','CAN_FD'),(54,3,'///',7,'ETHERNET','GMII'),(55,0,'///',5,'VIDEO','MIPI CSI-2 (D-PHY)'),(57,2,'llll',5,'USB','USB 3.1'),(58,10,'////',6,'GENERAL','GPIO');
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
INSERT INTO `interface_enum_sub` VALUES ('I2S','AUDIO'),('CAN_FD','CAN'),('CAN_HS','CAN'),('CAN_LS','CAN'),('GMII','ETHERNET'),('HSGMII','ETHERNET'),('MII','ETHERNET'),('RGMII','ETHERNET'),('RMII','ETHERNET'),('SGMII','ETHERNET'),('TBI','ETHERNET'),('USXGMII','ETHERNET'),('FLEXRAY','FLEXRAY'),('GPIO','GENERAL'),('I2C','GENERAL'),('JTAG','GENERAL'),('UART','GENERAL'),('LIN SBC','LIN'),('LIN2.1','LIN'),('LIN2.2','LIN'),('Multi-Channel LIN','LIN'),('Dual-SPI','SPI'),('Multi-Master SPI','SPI'),('Octal-SPI','SPI'),('Quad-SPI','SPI'),('DDR','STORAGE'),('DMA','STORAGE'),('eMMC','STORAGE'),('LPDDR','STORAGE'),('SPI NAND Flash','STORAGE'),('UFS','STORAGE'),('USB 2.0','USB'),('USB 3.0','USB'),('USB 3.1','USB'),('CoaxPress','VIDEO'),('DP','VIDEO'),('eDP','VIDEO'),('FPD_LINK III','VIDEO'),('GMSL','VIDEO'),('LVDS','VIDEO'),('MIPI CSI-2 (D-PHY)','VIDEO'),('MIPI CSI-2(C-PHY)','VIDEO'),('MIPI CSI-3','VIDEO'),('MIPI DSI-2','VIDEO');
/*!40000 ALTER TABLE `interface_enum_sub` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issuesandadvice`
--

LOCK TABLES `issuesandadvice` WRITE;
/*!40000 ALTER TABLE `issuesandadvice` DISABLE KEYS */;
INSERT INTO `issuesandadvice` VALUES (17,'我就试试，嘿嘿','2025-11-21 09:45:47','woshishuanghe@qq.com','suggestion','处理中','YANG YUQI','general','2025-11-21 16:01:39'),(20,'Hello,大佬。我想看市面上关于域控的主流的系统芯片方案有哪些？要去哪里找','2025-11-21 13:04:21','xiaolan@outlook.com','suggestion','待处理','xiaolan','general',NULL),(21,'1. 初始化页面无法选中和移动传感器 2. 保存的2D图，车模位置不正确','2025-11-21 13:05:12','1273880613@qq.com','issue','待处理','Jiawei_SONG','fov_builder','2025-11-21 16:01:47'),(22,'我试一下第六个你会怎么处理呢？','2025-11-21 14:01:23','xiaolan@outlook.com','suggestion','待处理','xiaolan','general',NULL);
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
  `ID` int NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `HFOV` float DEFAULT NULL,
  `VFOV` float DEFAULT NULL,
  `STACK` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `NAMEINDEX` (`Name`),
  KEY `fk_lens_suppliers_enum1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_lens_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers_enum` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lens`
--

LOCK TABLES `lens` WRITE;
/*!40000 ALTER TABLE `lens` DISABLE KEYS */;
INSERT INTO `lens` VALUES (1,'SF811ZG',120,60,'5G2GM,IRF','Sunny'),(2,'SF816WN',30,60,'5G2GM,IRF','Sunny'),(3,'YTOT-MCP308',100,60,'5G2GM,IRF','宇瞳玖洲'),(4,'JZ-M8356',200,200,'5G2GM,IRF','宇瞳玖洲');
/*!40000 ALTER TABLE `lens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lidar`
--

DROP TABLE IF EXISTS `lidar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lidar` (
  `ID` int NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lidar`
--

LOCK TABLES `lidar` WRITE;
/*!40000 ALTER TABLE `lidar` DISABLE KEYS */;
/*!40000 ALTER TABLE `lidar` ENABLE KEYS */;
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
  `isChecking` tinyint DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager_account`
--

LOCK TABLES `manager_account` WRITE;
/*!40000 ALTER TABLE `manager_account` DISABLE KEYS */;
INSERT INTO `manager_account` VALUES (1,'Admin','1234',1,1,1),(2,'Xinyu','dtsite2025',0,1,1),(3,'Jiahua','dtsite2025',0,1,1);
/*!40000 ALTER TABLE `manager_account` ENABLE KEYS */;
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
INSERT INTO `objects` VALUES ('calculator','Name','ID','计算芯片'),('camera','Name','ID','摄像头'),('euf','Name','ID','用户功能'),('function_features','Name','ID','子功能'),('image_sensors','Name','ID','图像传感器'),('lens','Name','ID','镜头'),('lidar','Name','ID','激光雷达'),('radar','Name','ID','毫米波雷达'),('regulation','Name','ID','法律法规'),('user','Name','ID','用户名单'),('work','Name','ID','任务列表');
/*!40000 ALTER TABLE `objects` ENABLE KEYS */;
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
  `Unit` varchar(45) GENERATED ALWAYS AS ((case when (`Type` = _utf8mb3'ASIC') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'BPU') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'CODEC') then _utf8mb4'/' when (`Type` = _utf8mb3'CPU') then _utf8mb4'KDMIPS' when (`Type` = _utf8mb3'DECODE') then _utf8mb4'FPS' when (`Type` = _utf8mb3'DOF') then _utf8mb4'MP/s' when (`Type` = _utf8mb3'DSP') then _utf8mb4'GFLOPS' when (`Type` = _utf8mb3'ENCODE') then _utf8mb4'FPS' when (`Type` = _utf8mb3'FPGA') then _utf8mb4'LUTs' when (`Type` = _utf8mb3'GPU') then _utf8mb4'GFLOPS' when (`Type` = _utf8mb3'ISP') then _utf8mb4'MP/s' when (`Type` = _utf8mb3'MMA') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'NPU') then _utf8mb4'TOPS' when (`Type` = _utf8mb3'RPU') then _utf8mb4'KDMIPS' when (`Type` = _utf8mb3'TPU') then _utf8mb4'TOPS' else _utf8mb4'UNIT' end)) STORED,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `PROCESSOR_ID_UNIQUE` (`ID`),
  KEY `fk_processor_calculator1_idx` (`calculator_ID`),
  KEY `fk_processor_processor_enum1_idx` (`Type`),
  CONSTRAINT `fk_processor_calculator1` FOREIGN KEY (`calculator_ID`) REFERENCES `calculator` (`ID`),
  CONSTRAINT `fk_processor_processor_enum1` FOREIGN KEY (`Type`) REFERENCES `processor_enum` (`Type`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processor`
--

LOCK TABLES `processor` WRITE;
/*!40000 ALTER TABLE `processor` DISABLE KEYS */;
INSERT INTO `processor` (`ID`, `Number`, `Name`, `Power`, `Lockstep`, `calculator_ID`, `Type`) VALUES (16,2,'Matrix Multiply Accelerator',16,0,1,'MMA'),(17,3,'Dual Cortex R5F',12,1,1,'RPU'),(18,1,'BXS-64-4',50,0,1,'GPU'),(23,3,'C7x',240,0,1,'DSP'),(24,1,'VPACv3',720,0,1,'ISP'),(25,2,'Cortex-A72@2Ghz',50,0,1,'CPU'),(26,2,'HTP',100,0,2,'NPU'),(27,4,'Cortex-R52',18,1,2,'RPU'),(28,1,'ADRENO_663',15000,0,2,'GPU'),(29,8,'Hexagon Vector eXtensions',100,0,2,'DSP'),(30,1,'Spectra 690 camera ISP',2.4,0,2,'ISP'),(31,1,'Adreno 765 VPU',10000,0,2,'CODEC'),(32,1,'???',240,0,2,'DOF'),(34,8,'Kyro Gen 6',245,0,2,'CPU'),(35,4,'RH850G4MH@400MHz',6.32,1,3,'CPU'),(36,1,'HTP',36,0,4,'NPU'),(37,4,'Cortex-R52',4,1,4,'RPU'),(38,1,'ADRENO',400,0,4,'GPU'),(39,4,'Hexagon Vector eXtension',1,0,4,'DSP'),(40,1,'Spectra 690 camera ISP',2457,0,4,'ISP'),(41,4,'Kryo Gold cores@21.GHz',100,0,4,'CPU'),(42,1,'////',3,0,8,'FPGA'),(43,1,'///',8,0,6,'BPU'),(44,3,'AAAA',30,0,7,'BPU'),(47,1,'NSP',96,0,5,'NPU');
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
INSERT INTO `processor_enum` VALUES ('ASIC','TOPS'),('BPU','TOPS'),('CODEC','/'),('CPU','KDMIPS'),('DECODE','FPS'),('DOF','MP/s'),('DSP','GFLOPS'),('ENCODE','FPS'),('FPGA','LUTs'),('GPU','GFLOPS'),('ISP','MP/s'),('MMA','TOPS'),('NPU','TOPS'),('RPU','KDMIPS'),('TPU','TOPS');
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
-- Table structure for table `radar`
--

DROP TABLE IF EXISTS `radar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `radar` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  `Calculator` varchar(45) NOT NULL,
  `Maximum_Instrument_Range` float DEFAULT NULL,
  `Azimuth_FOV_min` float DEFAULT NULL,
  `Azimuth_FOV_max` float DEFAULT NULL,
  `Elevation_FOV_min` float DEFAULT NULL,
  `Elevation_FOV_max` float DEFAULT NULL,
  `Type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_radar_suppliers_enum1_idx` (`Supplier_Name`),
  KEY `fk_radar_calculator1_idx` (`Calculator`),
  CONSTRAINT `fk_radar_calculator1` FOREIGN KEY (`Calculator`) REFERENCES `calculator` (`Name`),
  CONSTRAINT `fk_radar_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers_enum` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radar`
--

LOCK TABLES `radar` WRITE;
/*!40000 ALTER TABLE `radar` DISABLE KEYS */;
INSERT INTO `radar` VALUES (1,'MCR1.2','Valeo','RH850-U2A16',NULL,NULL,NULL,NULL,NULL,'3D'),(2,'GEN5','Bosch','RH850-U2A16',NULL,NULL,NULL,NULL,NULL,'3D');
/*!40000 ALTER TABLE `radar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regulation`
--

DROP TABLE IF EXISTS `regulation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regulation` (
  `REGULATION_NAME` varchar(45) NOT NULL,
  `REGULATION_ID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`REGULATION_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regulation`
--

LOCK TABLES `regulation` WRITE;
/*!40000 ALTER TABLE `regulation` DISABLE KEYS */;
INSERT INTO `regulation` VALUES ('REG_EXAMPLE',1);
/*!40000 ALTER TABLE `regulation` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensors_equipement`
--

LOCK TABLES `sensors_equipement` WRITE;
/*!40000 ALTER TABLE `sensors_equipement` DISABLE KEYS */;
INSERT INTO `sensors_equipement` VALUES (1,1,'Front_Center','Camera_PH','General',1),(2,1,'Front_Center','Radar','3D',0),(3,2,'Front_Center','Camera_PH','General',1),(4,2,'Front_Center','Radar','3D',1),(5,11,'Front_Center','Camera_PH','General',1),(6,20,'Front_Center','Camera_PH','WIDE',1),(7,20,'Rear_Center','Camera_PH','MIDDLE',1),(8,20,'Left','Camera_FE','FISHEYE',1),(9,20,'Right','Camera_FE','FISHEYE',0),(10,20,'Front_Center','Radar','3D',1),(11,20,'Front_Left_Corner','Radar','3D',1),(12,20,'Front_Right_Corner','Radar','3D',1),(13,20,'Rear_Left_Corner','Radar','3D',1),(14,20,'Rear_Right_Corner','Radar','3D',1);
/*!40000 ALTER TABLE `sensors_equipement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serializers`
--

DROP TABLE IF EXISTS `serializers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serializers` (
  `ID` int NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Supplier_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `NAMEINDEX` (`Name`) /*!80000 INVISIBLE */,
  KEY `fk_serializers_suppliers_enum1_idx` (`Supplier_Name`),
  CONSTRAINT `fk_serializers_suppliers_enum1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers_enum` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serializers`
--

LOCK TABLES `serializers` WRITE;
/*!40000 ALTER TABLE `serializers` DISABLE KEYS */;
INSERT INTO `serializers` VALUES (1,'MAX96717','Maxintergrated'),(2,'MAX96717F','Maxintergrated'),(3,'DS90UB971','TI');
/*!40000 ALTER TABLE `serializers` ENABLE KEYS */;
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
-- Table structure for table `suppliers_enum`
--

DROP TABLE IF EXISTS `suppliers_enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers_enum` (
  `Name` varchar(45) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers_enum`
--

LOCK TABLES `suppliers_enum` WRITE;
/*!40000 ALTER TABLE `suppliers_enum` DISABLE KEYS */;
INSERT INTO `suppliers_enum` VALUES ('APTIV'),('Bosch'),('Continental'),('Desay'),('GalaxyCore'),('HorizonRobotics'),('Maxieye'),('Maxintergrated'),('Minieye'),('Mobileye'),('NXP'),('OmniVision'),('ON-Semi'),('QualComm'),('Renesas'),('Samsung'),('SenseTime'),('SmartSens'),('Sony'),('Sunny'),('TI'),('TRW'),('Valeo'),('ZF'),('宇瞳玖洲');
/*!40000 ALTER TABLE `suppliers_enum` ENABLE KEYS */;
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
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(16) NOT NULL,
  `email` varchar(255) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `isSubscribe` tinyint NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Jiawei SONG','song-jiawei@outlook.com','2025-11-21 06:26:35',1),(44,'xiaoxie','xjiejyjy@163.com','2025-11-21 09:31:17',1),(46,'Jiawei SONG_1','1273880613@qq.com','2025-11-21 09:46:47',1),(47,'缪可言','378060679@qq.com','2025-11-21 13:02:56',1),(48,'朱信宇','875361542@qq.com','2025-11-21 13:03:13',1),(49,'xiaolan','xiaolan@outlook.com','2025-11-21 13:04:21',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visit`
--

DROP TABLE IF EXISTS `visit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visit` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `page_url` varchar(45) DEFAULT NULL,
  `user_ad` varchar(45) DEFAULT NULL,
  `session` varchar(45) DEFAULT NULL,
  `visit_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `from_page` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visit`
--

LOCK TABLES `visit` WRITE;
/*!40000 ALTER TABLE `visit` DISABLE KEYS */;
INSERT INTO `visit` VALUES (1,'/index.html','user_199q5eo5x2vmi2tlnvp','session_xdx6rv3m7bqmi8775ds','2025-11-22 00:59:26','http://127.0.0.1:5501/index.html'),(2,'/index.html','user_199q5eo5x2vmi2tlnvp','session_xdx6rv3m7bqmi8775ds','2025-11-22 00:59:45','http://127.0.0.1:5501/index.html'),(3,'/Pages/KnowledgeNet.html','user_199q5eo5x2vmi2tlnvp','session_xdx6rv3m7bqmi8775ds','2025-11-22 00:59:50','http://127.0.0.1:5501/index.html'),(4,'/Pages/AdasBenchmark.html','user_199q5eo5x2vmi2tlnvp','session_xdx6rv3m7bqmi8775ds','2025-11-22 01:00:09','http://127.0.0.1:5501/Pages/KnowledgeNet.html'),(5,'/Pages/KnowledgeNet.html','user_199q5eo5x2vmi2tlnvp','session_xdx6rv3m7bqmi8775ds','2025-11-22 15:11:05','http://127.0.0.1:5501/index.html'),(6,'/Pages/AdasBenchmark.html','user_199q5eo5x2vmi2tlnvp','session_xdx6rv3m7bqmi8775ds','2025-11-22 15:11:07','http://127.0.0.1:5501/Pages/KnowledgeNet.html'),(7,'/Pages/KnowledgeNet.html','user_199q5eo5x2vmi2tlnvp','session_xdx6rv3m7bqmi8775ds','2025-11-22 15:16:53','http://127.0.0.1:5501/index.html'),(8,'/index.html','user_199q5eo5x2vmi2tlnvp','session_nds4l8f8f7miahjipg','2025-11-22 16:10:18','');
/*!40000 ALTER TABLE `visit` ENABLE KEYS */;
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

-- Dump completed on 2025-11-24 17:09:29
