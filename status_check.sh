#!/bin/bash

echo "--- १. हालको फोल्डर ---"
pwd

echo -e "\n--- २. प्रोजेक्ट फोल्डर र फाइलहरू ---"
ls -l ~/omega-prime-v2-soul/

echo -e "\n--- ३. Python को संस्करण ---"
python3 --version

echo -e "\n--- ४. Conda को अवस्था ---"
conda info | grep 'active environment'

echo -e "\n--- ५. अन्तिम लग गतिविधि ---"
tail -n 5 ~/omega-prime-v2-soul/omega_prime.log
