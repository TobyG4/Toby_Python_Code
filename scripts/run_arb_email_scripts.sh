PATH='/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin'

cd /crypto_arbing/scripts/arb_check/

echo "Updating exchange_rates.py "

/root/anaconda3/bin/python /crypto_arbing/scripts/arb_check/update_exchange_rates.py

echo "Running xrp_arb_check.py "

/root/anaconda3/bin/python /crypto_arbing/scripts/arb_check/xrp_arb_check.py