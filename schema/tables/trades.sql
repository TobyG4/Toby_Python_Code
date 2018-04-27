

CREATE TABLE `order_type` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(150) NOT NULL,
    `ut` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `order_book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_pairs_lookup_id` int(11) NOT NULL,
  `order_type_id` int(11) NOT NULL,
  `price` decimal(20,10) NOT NULL,
  `quantity` decimal(20,10) NOT NULL,
  `order_time` datetime NOT NULL,
  `server_time` datetime NOT NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `exchange_rates` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `exchange_rate` decimal(20,10) NOT NULL,
    `crypto_currency_id` int(11) NOT NULL,
    `crypto_currency_id2` int(11) NOT NULL,
    `ut` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `order_book_live` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_book_id` int(11) NOT NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;