CREATE TABLE IF NOT EXISTS `LinksTable` (
  `id` INT,
  `username` VARCHAR(45) NULL,
  `userid` BIGINT NULL,
  `name` VARCHAR(45) NULL,
  `url` VARCHAR(450) NULL,
  `hits` BIGINT DEFAULT 0,
  `created_at` DATETIME DEFAULT  CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
UNIQUE (`name` ASC))
