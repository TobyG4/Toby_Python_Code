

ALTER TABLE `asset_pairs` 
    ADD CONSTRAINT `ap_crypto_currency_id_FK`
    FOREIGN KEY (`crypto_currency_id`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
    
ALTER TABLE `asset_pairs` 
    ADD CONSTRAINT `ap_crypto_currency_id2_FK`
    FOREIGN KEY (`crypto_currency_id2`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
 
ALTER TABLE `asset_pairs_lookup` 
    ADD CONSTRAINT `apl_asset_pairs_FK`
    FOREIGN KEY (`asset_pairs_id`)
    REFERENCES `asset_pairs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
    
ALTER TABLE `asset_pairs_lookup` 
    ADD CONSTRAINT `apl_exchange_FK`
    FOREIGN KEY (`exchange_id`)
    REFERENCES `exchange` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `crypto_currency_lookup`
    ADD CONSTRAINT `ccl_exchange_id_FK`
    FOREIGN KEY (`exchange_id`)
    REFERENCES `exchange` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
    
ALTER TABLE `crypto_currency_lookup`
    ADD CONSTRAINT `ccl_crypto_currency_id_FK`
    FOREIGN KEY (`crypto_currency_id`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

