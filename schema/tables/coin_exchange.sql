#export PATH=${PATH}:/usr/local/mysql/bin/

CREATE TABLE `crypto_currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `altname` varchar(150) NOT NULL,
  `fiat` boolean NULL,
  `ut` datetime NOT NULL,  
  PRIMARY KEY (`id`),
  UNIQUE KEY(`altname`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `exchange` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `crypto_currency_lookup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `crypto_currency_id` int(11) NULL,
  `exchange_id` int(11) NOT NULL, 
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `asset_pairs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `crypto_currency_id` int(11) NOT NULL,
  `crypto_currency_id2` int(11) NOT NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY(`crypto_currency_id`,`crypto_currency_id2`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;



CREATE TABLE `asset_pairs_lookup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `asset_pairs_id` int(11) NULL,
  `exchange_id` int(11) NOT NULL,
  `tradeable` boolean NOT NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
