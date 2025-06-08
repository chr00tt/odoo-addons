#!/bin/bash

echo 'id,code,master_code,name,category' > nhsa.jbzd.csv
awk -v FPAT='([^,]*)|("[^"]*")' -v OFS=, 'NR>1 {code = $1 ? $1 : $2; id = code; gsub(/\./, "_", id); gsub(/"/, "", id); master = $1 ? "True" : "False"; print "nhsa_jbzd_" id "," code "," master "," $3 "," $4}' 手术操作分类代码国家临床版3.0.csv >> nhsa.jbzd.csv
