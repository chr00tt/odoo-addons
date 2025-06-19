#!/bin/bash

echo 'id,name,primary_classification,secondary_classification,tertiary_classification,common_name,material,characteristics,payment_category,payment_standard,description' > gz.medical.consumables.csv
awk -F ',' '{print "gz_nhsa_consumables_" $2 "," $2 "," substr($3,4) "," substr($4,4) "," substr($5,4) "," substr($6,5) "," substr($7,4) "," substr($8,5) "," $9 "," $10 "," $11}' output.csv >> gz.medical.consumables.csv
