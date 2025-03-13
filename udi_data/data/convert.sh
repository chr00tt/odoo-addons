#!/bin/bash

echo 'id,name,code,parent_id/id,cpms,yqyt,pmjl,gllb' > medical.device.category.csv
awk -F ',' 'NR>1 {print "medical_device_category_" substr($2, 1, 2) "," substr($2, 4) "," substr($2, 1, 2) ",medical_device_category_all,,,,"}' 医疗器械分类目录.csv | uniq >> medical.device.category.csv
awk -F ',' 'NR>1 {print "medical_device_category_" substr($2, 1, 2) "-" substr($3, 1, 2) "," substr($3, 4) "," substr($2, 1, 2) "-" substr($3, 1, 2) ",medical_device_category_" substr($2, 1, 2) ",,,,"}' 医疗器械分类目录.csv | uniq >> medical.device.category.csv
awk -F ',' 'NR>1 {print "medical_device_category_" substr($2, 1, 2) "-" substr($3, 1, 2) "-" substr($4, 1, 2) "," substr($4, 4) "," substr($2, 1, 2) "-" substr($3, 1, 2) "-" substr($4, 1, 2) ",medical_device_category_" substr($2, 1, 2) "-" substr($3, 1, 2) "-" substr($4, 1, 2) "," $5 "," $6 "," $7 "," $8}' 医疗器械分类目录.csv | uniq >> medical.device.category.csv
