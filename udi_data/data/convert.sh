#!/bin/bash

echo 'id,name,code,parent_id/id,cpms,yqyt,pmjl,gllb' > medical.device.category.csv

# 医疗器械分类目录
sed -i 's/,I$/,Ⅰ/g' 医疗器械分类目录.csv
sed -i 's/,II$/,Ⅱ/g' 医疗器械分类目录.csv
sed -i 's/,III$/,Ⅲ/g' 医疗器械分类目录.csv
awk -F ',' 'NR>1 {print "medical_device_category_" substr($2, 1, 2) "," substr($2, 4) "," substr($2, 1, 2) ",medical_device_category_all,,,,"}' 医疗器械分类目录.csv | uniq >> medical.device.category.csv
awk -F ',' 'NR>1 {print "medical_device_category_" substr($2, 1, 2) "-" substr($3, 1, 2) "," substr($3, 4) "," substr($2, 1, 2) "-" substr($3, 1, 2) ",medical_device_category_" substr($2, 1, 2) ",,,,"}' 医疗器械分类目录.csv | uniq >> medical.device.category.csv
awk -F ',' 'NR>1 {print "medical_device_category_" substr($2, 1, 2) "-" substr($3, 1, 2) "-" substr($4, 1, 2) "," substr($4, 4) "," substr($2, 1, 2) "-" substr($3, 1, 2) "-" substr($4, 1, 2) ",medical_device_category_" substr($2, 1, 2) "-" substr($3, 1, 2) "," $5 "," $6 "," $7 "," substr($8, 1, 1)}' 医疗器械分类目录.csv >> medical.device.category.csv

# 体外诊断试剂分类目录(老目录)
sed -i 's/,"I-/,"Ⅰ-/g' 体外诊断试剂分类目录\(6840-2013\).csv
sed -i 's/,"I"$/,Ⅰ/g' 体外诊断试剂分类目录\(6840-2013\).csv
awk -F ',' 'NR>4 {gsub(/^"|"$/, "", $2); split($2, lb, " "); print "medical_device_category_6840_old_" lb[1] "," lb[2] ",6840-" lb[1] ",medical_device_category_6840_old,,,," substr(lb[1], 1, 1)}' 体外诊断试剂分类目录\(6840-2013\).csv | uniq >> medical.device.category.csv
awk -v FPAT='([^,]+)|("[^"]+")' 'NR>4 {gsub(/^"|"$/, "", $1); gsub(/^"|"$/, "", $2); split($2, lb, " "); print "medical_device_category_6840_old_" $1 "," $3 ",6840-" $1 ",medical_device_category_6840_old_" lb[1] ",," $4 ",," $5}' 体外诊断试剂分类目录\(6840-2013\).csv >> medical.device.category.csv

# 体外诊断试剂分类目录
awk -v FPAT='([^,]*)|("[^"]*")' -v OFS=, 'NR>1 {f2 = sprintf("%02d", $2); print "medical_device_category_6840_" $2 "," $3 ",6840-" f2 ",medical_device_category_6840,,,," $7}' 体外诊断试剂分类目录.csv | uniq >> medical.device.category.csv
awk -v FPAT='([^,]*)|("[^"]*")' -v OFS=, 'NR>1 {f2 = sprintf("%02d", $2); f4 = sprintf("%05d", $4); print "medical_device_category_6840_" $2 "-" $4 "," $5 ",6840-" f2 "-" f4 ",medical_device_category_6840_" $2 ",," $6 ",," $7}' 体外诊断试剂分类目录.csv >> medical.device.category.csv
