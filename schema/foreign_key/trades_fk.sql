ALTER TABLE `order_book`
    ADD CONSTRAINT `ob_order_type_id_FK`
    FOREIGN KEY (`order_type_id`)
    REFERENCES `order_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
    
    
ALTER TABLE `order_book`
    ADD CONSTRAINT `ob_asset_pairs_lookup_id_FK`
    FOREIGN KEY (`asset_pairs_lookup_id`)
    REFERENCES `asset_pairs_lookup` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

ALTER TABLE `order_book_live`
    ADD CONSTRAINT `obl_order_book_id_FK`
    FOREIGN KEY (`order_book_id`)
    REFERENCES `order_book` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;
