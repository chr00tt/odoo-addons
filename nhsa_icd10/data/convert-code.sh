#!/bin/bash

#echo 'id,code,name,category_id/id' > icd10.code.csv
#awk -F ',' 'NR>1 && $10 != "" && $11 != "" {print "icd10_diagnostic_code_" $10 "," $10 "," $11 ",icd10_category_subcategory_" $8}' output.csv | uniq >> icd10.code.csv
#echo 'id,code,name,category_id/id' > icd10.code.csv
echo 'id,code,name,category_id/id' > icd10.code.csv
awk '
BEGIN {
    # FPAT定义字段模式：非逗号字符 或 被引号包围的字符
    FPAT="([^,]*)|(\"[^\"]+\")"
    OFS = ","
}
NR > 1 {
    # 检查是否有足够的列且关键字段不为空
    if (NF >= 11 && $10 != "" && $11 != "") {
        code = $10
        name = $11
        category = $8

        # 去除字段可能包含的引号
        gsub(/^"|"$/, "", code)
        gsub(/^"|"$/, "", name)
        gsub(/^"|"$/, "", category)

        # 构造输出行
        id_field = "icd10_diagnostic_code_" code
        category_field = "icd10_category_subcategory_" category

        # 输出行
        print id_field, code, name, category_field
    }
}
' output.csv | uniq >> icd10.code.csv
