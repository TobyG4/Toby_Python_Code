#!/bin/sh


HOST=localhost
DB_USERNAME=root
DB_PASSWORD=Crypto
DB_NAME="Crypto_Test"

BASE=`dirname "$0"`
echo $BASE

# Drop database
#mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME -e "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME character set utf8 collate utf8_unicode_ci;"

# create our tables
echo "Creating tables"
#mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/schema/tables/coin_exchange.sql
#mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/schema/tables/fees.sql
#mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/schema/tables/trades.sql

# create foreign keys
echo "Creating foreign keys"
mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/schema/foreign_key/coin_exchange_fk.sql
mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/schema/foreign_key/fees_fk.sql
mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/schema/foreign_key/trades_fk.sql



# load initial live data
echo "Loading initial live data"
# mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/livedata/table1.sql
# mysql -u$DB_USERNAME -h $HOST -p$DB_PASSWORD -D $DB_NAME < $BASE/livedata/table2.sql



echo "Done.";  

