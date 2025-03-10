#!/bin/bash

echo 'id,name,code,parent_id/id' > nhsa.consumables.category.csv
awk -F ',' 'NR>1 {print "nhsa_consumables_category_" substr($1,1,3) "," substr($2,4) "," substr($2,1,2) ","}' output.csv | uniq >> nhsa.consumables.category.csv
awk -F ',' 'NR>1 {print "nhsa_consumables_category_" substr($1,1,5) "," substr($3,4) "," substr($3,1,2) ",nhsa_consumables_category_" substr($1,1,3)}' output.csv | uniq >> nhsa.consumables.category.csv
awk -F ',' 'NR>1 {print "nhsa_consumables_category_" substr($1,1,7) "," substr($4,4) "," substr($4,1,2) ",nhsa_consumables_category_" substr($1,1,5)}' output.csv | uniq >> nhsa.consumables.category.csv
