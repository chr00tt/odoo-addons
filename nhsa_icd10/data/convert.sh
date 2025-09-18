#!/bin/bash

echo 'id,name,code,parent_id/id' > icd10.category.csv
awk -v FPAT='([^,]*)|("[^"]*")' 'NR>1 {
print "icd10_category_chapter_" $2 "," $3 "," $2 ",nhsa_icd10.icd10_category_all"
}' output.csv | uniq >> icd10.category.csv
awk -v FPAT='([^,]*)|("[^"]*")' 'NR>1 {
print "icd10_category_block_" $4 "," $5 "," $4 ",icd10_category_chapter_" $2
}' output.csv | uniq >> icd10.category.csv
awk -v FPAT='([^,]*)|("[^"]*")' 'NR>1 && $6!="" {
print "icd10_category_category_" $6 "," $7 "," $6 ",icd10_category_block_" $4
}' output.csv | uniq >> icd10.category.csv
awk -v FPAT='([^,]*)|("[^"]*")' 'NR>1 && $8!="" {
print "icd10_category_subcategory_" $8 "," $9 "," $8 ",icd10_category_category_" $6
}' output.csv | uniq >> icd10.category.csv

echo 'id,code,name,category_id/id' > icd10.code.csv
awk -v FPAT='([^,]*)|("[^"]*")' 'NR>1 && $10!="" {
if ($8 != "") {
    category = "icd10_category_subcategory_" $8
} else if ($6 != "") {
    category = "icd10_category_category_" $6
} else {
    category = "icd10_category_block_" $4
}
print "icd10_code_" $10 "," $10 "," $11 "," category
}' output.csv | uniq >> icd10.code.csv
