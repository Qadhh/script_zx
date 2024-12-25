from openpyxl import Workbook
# 创建一个新的Workbook
wb = Workbook()
ws = wb.active

# 定义要写入的值
values = [25, 30, 35, 40]

# 写入值到第一行的不同列
for col_num, value in enumerate(values, start=1):
    ws.cell(row=1, column=col_num, value=value)

# 保存Workbook到Excel文件
excel_file = 'output.xlsx'
wb.save(excel_file)

print(f"Values {values} written to the first row of {excel_file}.")