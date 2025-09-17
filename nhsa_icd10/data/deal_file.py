import csv

with open('/odoo/odoo-docker/17/addons/odoo-addons/nhsa_icd10/data/output.csv', 'r', encoding='utf-8') as infile, \
        open('icd10.code.csv', 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    # 写入标题行
    outfile.write('id,code,name,category_id/id\n')
    #writer.writerow(['id', 'code', 'name', 'category_id/id'])

    # 跳过标题行
    next(reader)

    seen_rows = set()

    for row in reader:
        if len(row) >= 11 and row[9] and row[10]:
            code = row[9]
            name = row[10]
            category = row[7]

            # 构造输出行
            output_row = [
                f"icd10_diagnostic_code_{code}",
                code,
                name,  # csv.writer会自动处理包含逗号的字段
                f"icd10_category_subcategory_{category}"
            ]

            # 去重
            row_key = tuple(output_row)
            if row_key not in seen_rows:
                seen_rows.add(row_key)
                #writer.writerow(output_row)
                # 手动写入行，用逗号连接并添加换行符
                outfile.write(','.join(output_row) + '\n')