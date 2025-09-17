#!/bin/bash

echo 'id,name,code,parent_id/id' > icd10.category.csv
awk -v FPAT='([^,]+)|("[^"]+")' 'NR>1 {print "icd10_category_chapter_" $2 "," $3 "," $2 ",icd10_category_all"}' output.csv | uniq >> icd10.category.csv
awk -v FPAT='([^,]+)|("[^"]+")' 'NR>1 {print "icd10_category_block_" $4 "," $5 "," $4 ",icd10_category_chapter_" $2}' output.csv | uniq >> icd10.category.csv
awk -v FPAT='([^,]+)|("[^"]+")' 'NR>1 && $6!="" {print "icd10_category_category_" $6 "," $7 "," $6 ",icd10_category_block_" $4}' output.csv | uniq >> icd10.category.csv
awk -v FPAT='([^,]+)|("[^"]+")' 'NR>1 && $8!="" {print "icd10_category_subcategory_" $8 "," $9 "," $8 ",icd10_category_category_" $6}' output.csv | uniq >> icd10.category.csv

echo 'id,code,name,category_id/id' > icd10.code.csv
awk '
BEGIN {
    # FPAT定义字段模式：非逗号字符 或 被引号包围的字符
    FPAT="([^,]*)|(\"[^\"]+\")"
    OFS = ","
}
NR > 1 && $10 != "" {
    # 检查是否有足够的列且关键字段不为空
        code = $10
        name = $11
        category = $8
        if (category == "") {
            category = $6
            if (category == "") {
                category = $4
            }
        }
        # 删除多余的 fi 行

        # 构造输出行
        id_field = "icd10_diagnostic_code_" code
        category_field = "icd10_category_subcategory_" category

        # 输出行
        print id_field, code, name, category_field
}
' output.csv | uniq >> icd10.code.csv
