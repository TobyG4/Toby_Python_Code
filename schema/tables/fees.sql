CREATE TABLE `trading_fees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_pairs_lookup_id` int(11) NOT NULL,
  `exchange_id` int(11) NOT NULL, 
  `trading_volume` int(11), 
  `maker_fee` decimal(3,2),
  `taker_fee` decimal(3,2),
  `fee_volume_currency_id` int(11) NOT NULL,
  `leverage_buy` boolean NULL,
  `leverage_sell` boolean NULL,
  `margin_call` int(11) NULL, 
  `margin_stop` int(11) NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY(`asset_pairs_lookup_id`,`exchange_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `withdrawal_fees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange_id` int(11) NOT NULL, 
  `crypto_currency_id` int(11) NOT NULL,
  `quantity` decimal(10,5) NOT NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY(`exchange_id`,`crypto_currency_id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `deposit_fees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exchange_id` int(11) NOT NULL, 
  `crypto_currency_id` int(11) NOT NULL,
  `quantity` decimal(10,5) NOT NULL,
  `block_confirmations` int(11),
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`),
   UNIQUE KEY(`exchange_id`,`crypto_currency_id`)

) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;


CREATE TABLE `fiat_exchange_rates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `crypto_currency_id` int(11) NOT NULL,
  `crypto_currency_id2` int(11) NOT NULL,
  `exchange_rate` decimal(10,5) NOT NULL,
  `source_id` int(11) NOT NULL,
  `server_time` datetime NOT NULL,
  `ut` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;