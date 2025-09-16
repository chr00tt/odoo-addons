#!/bin/bash

echo 'id,name,code,parent_id/id' > icd10.category.csv
awk -F ',' 'NR>1 {print "icd10_category_chapter_" $2 "," $3 "," $2 ",icd10_category_all"}' output.csv | uniq >> icd10.category.csv
awk -F ',' 'NR>1 {print "icd10_category_block_" $4 "," $5 "," $4 ",icd10_category_chapter_" $2}' output.csv | uniq >> icd10.category.csv
awk -F ',' 'NR>1 {print "icd10_category_category_" $6 "," $7 "," $6 ",icd10_category_block_" $4}' output.csv | uniq >> icd10.category.csv
awk -F ',' 'NR>1 {print "icd10_category_subcategory_" $8 "," $9 "," $8 ",icd10_category_category_" $6}' output.csv | uniq >> icd10.category.csv
