#!/bin/bash

echo 'id,name,code,parent_id/id' > nhsa.consumables.category.csv
awk -F ',' 'NR>1 {print "nhsa_consumables_category_" substr($1,1,3) $2 "," $4}' output.csv >> nhsa.consumables.category.csv
