-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema tweetboard
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tweetboard
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tweetboard` DEFAULT CHARACTER SET latin1 ;
USE `tweetboard` ;

-- -----------------------------------------------------
-- Table `tweetboard`.`Players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tweetboard`.`Players` (
  `player_id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(256) NULL DEFAULT NULL,
  `last_name` VARCHAR(256) NULL DEFAULT NULL,
  `team` VARCHAR(256) NULL DEFAULT NULL,
  `scores` INT(11) NULL DEFAULT '0',
  `assists` INT(11) NULL DEFAULT '0',
  PRIMARY KEY (`player_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `tweetboard`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tweetboard`.`Users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(256) NULL DEFAULT NULL,
  `last_name` VARCHAR(256) NULL DEFAULT NULL,
  `email` VARCHAR(256) NULL DEFAULT NULL,
  `team` VARCHAR(256) NULL DEFAULT NULL,
  `password` VARCHAR(256) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `tweetboard`.`teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tweetboard`.`teams` (
  `teamID` INT(11) NOT NULL AUTO_INCREMENT,
  `wins` INT(11) NULL DEFAULT NULL,
  `losses` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`teamID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `tweetboard`.`tournament`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tweetboard`.`tournament` (
  `gameID` INT(11) NOT NULL AUTO_INCREMENT,
  `winner` VARCHAR(256) NULL DEFAULT NULL,
  `loser` VARCHAR(256) NULL DEFAULT NULL,
  `w_score` INT(11) NULL DEFAULT NULL,
  `l_score` INT(11) NULL DEFAULT NULL,
  `tournament` VARCHAR(256) NULL DEFAULT NULL,
  `dt` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`gameID`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
