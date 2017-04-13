CREATE TABLE IF NOT EXISTS `golinks`.`UserTable` (
  `id` INT NOT NULL,
  `username` VARCHAR(45) NULL,
  `userid` BIGINT NULL,
  `shortlink` VARCHAR(45) NULL,
  `longlink` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `shortlink_UNIQUE` (`shortlink` ASC))
ENGINE = InnoDB
