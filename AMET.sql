-- --------------------------------------------------------
-- Hôte:                         iteam-s.mg
-- Version du serveur:           10.3.31-MariaDB-0ubuntu0.20.04.1 - Ubuntu 20.04
-- SE du serveur:                debian-linux-gnu
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour AMET
CREATE DATABASE IF NOT EXISTS `AMET` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `AMET`;

-- Listage de la structure de la table AMET. AutreUtils
CREATE TABLE IF NOT EXISTS `AutreUtils` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fb_id` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `userMail` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mdp` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `actions` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temps` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `idLastConnect` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `fb_id` (`fb_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table AMET. categories
CREATE TABLE IF NOT EXISTS `categories` (
  `id_categ` int(11) NOT NULL AUTO_INCREMENT,
  `type_categ` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_categ`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table AMET. commande
CREATE TABLE IF NOT EXISTS `commande` (
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
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table AMET. galeries
CREATE TABLE IF NOT EXISTS `galeries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenu` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_prod` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `galeries_produits_FK` (`id_prod`),
  CONSTRAINT `galeries_produits_FK` FOREIGN KEY (`id_prod`) REFERENCES `produits` (`id_prod`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table AMET. informations
CREATE TABLE IF NOT EXISTS `informations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contenuInfo` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table AMET. partenaire
CREATE TABLE IF NOT EXISTS `partenaire` (
  `id_part` int(11) NOT NULL AUTO_INCREMENT,
  `dateAction` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `fb_idPart` varchar(250) DEFAULT NULL,
  `UserMail` varchar(250) DEFAULT NULL,
  `mdpPart` varchar(250) DEFAULT NULL,
  `FullName` varchar(250) DEFAULT NULL,
  `actions` varchar(50) DEFAULT NULL,
  `temp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `lastIdConnect` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_part`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table AMET. produits
CREATE TABLE IF NOT EXISTS `produits` (
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de l'évènement AMET. RUN_VERIF_ACTION_TIME
DELIMITER //
CREATE EVENT `RUN_VERIF_ACTION_TIME` ON SCHEDULE EVERY 5 MINUTE STARTS '2021-12-19 06:22:33' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
  CALL VERIF_ACTION_TIME(1800);
END//
DELIMITER ;

-- Listage de la structure de la table AMET. utilisateur
CREATE TABLE IF NOT EXISTS `utilisateur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fb_id` varchar(250) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_mp` datetime DEFAULT NULL,
  `action` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `temp` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `date_action` datetime DEFAULT current_timestamp(),
  `nom_user` varchar(250) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `fb_id` (`fb_id`),
  KEY `date_action` (`date_action`)
) ENGINE=InnoDB AUTO_INCREMENT=7232 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la procédure AMET. VERIF_ACTION_TIME
DELIMITER //
CREATE PROCEDURE `VERIF_ACTION_TIME`(
	IN `delai` INT
)
BEGIN

UPDATE utilisateur 
	SET `action` = NULL
WHERE TIMESTAMPDIFF(SECOND, date_action, NOW()) > delai AND `action` IS NOT NULL;

END//
DELIMITER ;

-- Listage de la structure de déclencheur AMET. BEFORE_UPDATE_ACTION
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `BEFORE_UPDATE_ACTION` BEFORE UPDATE ON `utilisateur` FOR EACH ROW BEGIN
  IF (NEW.action <> OLD.action) OR (NEW.action IS NOT NULL AND OLD.action IS NULL) OR (NEW.action IS NULL AND OLD.action IS NOT NULL) THEN
   	SET NEW.date_action = NOW();
  END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
