import xlwings as xw

# Open the Excel file
wb = xw.Book(r'Soil Springs_2024.xlsx')

# Prepare output file
with open('Soil_Springs_2024_Formulas.txt', 'w', encoding='utf-8') as f:
    for sheet in wb.sheets:
        f.write(f"Sheet: {sheet.name}\n")
        used_range = sheet.used_range
        rows = used_range.rows.count
        cols = used_range.columns.count
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                cell = sheet.cells(i, j)
                formula = cell.formula
                value = cell.value
                if formula:
                    f.write(f"Cell {cell.address}: Formula: {formula} | Value: {value}\n")
        f.write("---\n")

wb.close()
