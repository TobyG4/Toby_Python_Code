ALTER TABLE `withdrawal_fees`
    ADD CONSTRAINT `wf_exchange_id_FK`
    FOREIGN KEY (`exchange_id`)
    REFERENCES `exchange` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `withdrawal_fees`
    ADD CONSTRAINT `wf_crypto_currency_id_FK`
    FOREIGN KEY (`crypto_currency_id`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
    
ALTER TABLE `trading_fees`
    ADD CONSTRAINT `tf_exchange_id_FK`
    FOREIGN KEY (`exchange_id`)
    REFERENCES `exchange` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `trading_fees`
    ADD CONSTRAINT `tf_asset_pairs_lookup_id_FK`
    FOREIGN KEY (`asset_pairs_lookup_id`)
    REFERENCES `asset_pairs_lookup` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `trading_fees`
    ADD CONSTRAINT `tf_crypto_currency_id2_FK`
    FOREIGN KEY (`fee_volume_currency_id`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `deposit_fees`
    ADD CONSTRAINT `df_exchange_id_FK`
    FOREIGN KEY (`exchange_id`)
    REFERENCES `exchange` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `deposit_fees`
    ADD CONSTRAINT `df_crypto_currency_id_FK`
    FOREIGN KEY (`crypto_currency_id`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `fiat_exchange_rates`
    ADD CONSTRAINT `fer_crypto_currency_id_FK`
    FOREIGN KEY (`crypto_currency_id`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `fiat_exchange_rates`
    ADD CONSTRAINT `fer_crypto_currency_id2_FK`
    FOREIGN KEY (`crypto_currency_id2`)
    REFERENCES `crypto_currency` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `fiat_exchange_rates`
    ADD CONSTRAINT `fer_source_id_FK`
    FOREIGN KEY (`source_id`)
    REFERENCES `exchange` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;