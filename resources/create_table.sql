CREATE TABLE IF NOT EXISTS `golinks`.`LinksTable` (
  `id` INT NOT NULL,
  `username` VARCHAR(45) NULL,
  `userid` BIGINT NULL,
  `shortlink` VARCHAR(45) NULL,
  `longlink` VARCHAR(45) NULL,
  `hits` BIGINT DEFAULT 0,
  `created` DATETIME DEFAULT  CURRENT_TIMESTAMP,
  `updated` DATETIME ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `shortlink_UNIQUE` (`shortlink` ASC))
ENGINE = InnoDB
