
cd /crypto_arbing/scripts/populate_database/

#echo "Running populate_kraken"
#/root/anaconda3/bin/python /crypto_arbing/scripts/populate_database/populate_kraken.py

echo "Running populate_coinone"
/root/anaconda3/bin/python /crypto_arbing/scripts/populate_database/populate_coinone.py

echo "Running populate_bitstamp"
/root/anaconda3/bin/python /crypto_arbing/scripts/populate_database/populate_bitstamp.py
