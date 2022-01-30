-- MySQL dump 10.19  Distrib 10.3.31-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: AMET
-- ------------------------------------------------------
-- Server version	10.3.31-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `AutreUtils`
--

DROP TABLE IF EXISTS `AutreUtils`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AutreUtils` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fb_id` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `userMail` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mdp` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `actions` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temps` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `idLastConnect` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nameUserLastConnect` varchar(205) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `fb_id` (`fb_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `id_categ` int(11) NOT NULL AUTO_INCREMENT,
  `type_categ` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_categ`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `commande`
--

DROP TABLE IF EXISTS `commande`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commande` (
  `id_cmd` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) DEFAULT NULL,
  `id_part` int(11) DEFAULT NULL,
  `date_cmd` datetime NOT NULL,
  `dateAlaTerrain` date DEFAULT NULL,
  `heureDebutCmd` time DEFAULT NULL,
  `heureFinCmd` time DEFAULT NULL,
  `id_prod` int(11) DEFAULT NULL,
  `statut` enum('CONFIRMÉ','NON CONFIRMÉ') COLLATE utf8mb4_unicode_ci DEFAULT 'NON CONFIRMÉ',
  `refMobilMoney` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dataQrCode` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_cmd`),
  KEY `commande_utilisateur_FK` (`id`),
  KEY `commande_produits0_FK` (`id_prod`),
  KEY `id_part` (`id_part`),
  CONSTRAINT `commande_produits0_FK` FOREIGN KEY (`id_prod`) REFERENCES `produits` (`id_prod`),
  CONSTRAINT `commande_utilisateur_FK` FOREIGN KEY (`id`) REFERENCES `utilisateur` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `galeries`
--

DROP TABLE IF EXISTS `galeries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `galeries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenu` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_prod` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `galeries_produits_FK` (`id_prod`),
  CONSTRAINT `galeries_produits_FK` FOREIGN KEY (`id_prod`) REFERENCES `produits` (`id_prod`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partenaire`
--

DROP TABLE IF EXISTS `partenaire`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partenaire` (
  `id_part` int(11) NOT NULL AUTO_INCREMENT,
  `dateAction` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `fb_idPart` varchar(250) DEFAULT NULL,
  `UserMail` varchar(250) DEFAULT NULL,
  `mdpPart` varchar(250) DEFAULT NULL,
  `FullName` varchar(250) DEFAULT NULL,
  `UserNameFbPart` varchar(250) DEFAULT NULL,
  `actions` varchar(50) DEFAULT NULL,
  `temp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `lastIdConnect` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_part`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `produits`
--

DROP TABLE IF EXISTS `produits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produits` (
  `id_prod` int(11) NOT NULL AUTO_INCREMENT,
  `nom_prod` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `details` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reference` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `prix` int(11) NOT NULL,
  `photo_couverture` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_categ` int(11) NOT NULL,
  `date_create` datetime DEFAULT current_timestamp(),
  `id_part` int(11) DEFAULT NULL,
  `heureDouv` int(11) DEFAULT 6,
  `heureFerm` int(11) DEFAULT 20,
  PRIMARY KEY (`id_prod`),
  KEY `produits_categories_FK` (`id_categ`) USING BTREE,
  CONSTRAINT `produits_categories_FK` FOREIGN KEY (`id_categ`) REFERENCES `categories` (`id_categ`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `statistiques`
--

DROP TABLE IF EXISTS `statistiques`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistiques` (
  `id_stat` int(11) NOT NULL AUTO_INCREMENT,
  `date_stat` datetime NOT NULL,
  `date_cmd` datetime NOT NULL,
  `prixstat` int(11) NOT NULL,
  `id_cmd` int(11) NOT NULL,
  PRIMARY KEY (`id_stat`),
  KEY `statistiques_commande_FK` (`id_cmd`),
  CONSTRAINT `statistiques_commande_FK` FOREIGN KEY (`id_cmd`) REFERENCES `commande` (`id_cmd`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `utilisateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fb_id` varchar(250) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_mp` datetime DEFAULT NULL,
  `type_user` enum('CLIENT','ADMIN','PART') COLLATE utf8mb4_unicode_ci DEFAULT 'CLIENT',
  `action` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `date_action` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `fb_id` (`fb_id`),
  KEY `date_action` (`date_action`)
) ENGINE=InnoDB AUTO_INCREMENT=5876 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`gaetan`@`%`*/ /*!50003 TRIGGER `BEFORE_UPDATE_ACTION` BEFORE UPDATE ON `utilisateur` FOR EACH ROW BEGIN
  IF (NEW.action <> OLD.action) OR (NEW.action IS NOT NULL AND OLD.action IS NULL) OR (NEW.action IS NULL AND OLD.action IS NOT NULL) THEN
   	SET NEW.date_action = NOW();
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-18 12:29:43
