import mysql.connector
import pandas as pd
import openpyxl.styles
from openpyxl.styles import numbers, Alignment, Border, Side
import KampfgerichtZuteilung


# Connect to the MySQL database
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sqlServerPW1312",
    database="spielplanung"
)

# Create a cursor
cursor = cnx.cursor()

# Define the table names
table_names = [
    'h1',
    'd1',
    'h2',
    'u18',
    'u18w',
    'u16',
    'u16w',
    'u141',
    'u142',
    'u14w',
    'u121',
    'u122',
    'u10'
]

# Fetch data from each table
results = []
for table in table_names:
    # Execute the SELECT query
    query = f"SELECT * FROM {table}"
    cursor.execute(query)

    # Fetch all the results
    results.extend(cursor.fetchall())

# column names
mycolumns = ['spnr', 'spt', 'team', 'liga', 'datum', 'uhrzeit', 'heim', 'gast', 'halle']

# Convert results to a DataFrame
df = pd.DataFrame(results, columns=cursor.column_names)

# insert column for Kampfgericht
df.insert(12, "KG", "")

# loop all unique game ids and allocate responsible Kampfgericht
for key, value in KampfgerichtZuteilung.kg.items():
    df.loc[df['id'] == key, 'KG'] = value

# Save DataFrame to Excel
excel_file = 'G:\\My Drive\\Spielplanung\\GSP.xlsx'  # Specify the desired output file name
df.to_excel(excel_file, index=False)

# color each teams gamestack in its respective color
colorDict = {
    'h1': '969696',
    'd1': '00FFFF',
    'h2': 'FFFFCC',
    'u18': '008080',
    'u18w': '008080',
    'u16': 'FF8080',
    'u16w': '99CC00',
    'u141': 'FF9900',
    'u142': 'FF9900',
    'u14w': '99CC00',
    'u121': '339966',
    'u122': 'CCCCFF',
    'u10': '00FF00'
}

col_List = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# Define border style
border = Border(
    left=Side(border_style='thin', color='000000'),
    right=Side(border_style='thin', color='000000'),
    top=Side(border_style='thin', color='000000'),
    bottom=Side(border_style='thin', color='000000')
)

workbook = openpyxl.load_workbook("G:\\My Drive\\Spielplanung\\GSP.xlsx")
sheet = workbook.active
rowNum = sheet.max_row

# Define the column letter you want to format (e.g., column A)
column_letter = 'F'

# Define the time format string you want to apply (e.g., "hh:mm:ss")
time_format = "hh:mm"

# define fonts
bold_font = openpyxl.styles.Font(bold=True, size=14)
weekendGray = openpyxl.styles.colors.Color(rgb='969696')
headingGray = openpyxl.styles.colors.Color(rgb='CCCCFF')
gray_fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=weekendGray)
heading_fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=headingGray)

width = 30
for column in col_List:
    sheet.column_dimensions[column].width = width

# Iterate over the cells in the specified column and apply the time format
for cell in sheet[column_letter]:
    cell.number_format = numbers.FORMAT_DATE_TIME3

# Iterate over all cells in each sheet
for row in sheet.iter_rows():
    for cell in row:
        cell.alignment = Alignment(horizontal='right')
        cell.border = border

# loop first row
for cell in sheet[1]:
    cell.font = bold_font
    cell.fill = gray_fill
    cell.alignment = Alignment(horizontal='center')

# Enable filters
sheet.auto_filter.ref = sheet.dimensions

# loop excel rows
for row in range(2, rowNum + 1, 1):

    # loop row cells
    for cell in sheet[row]:

        # select teamtag, create colorcode and color all cells
        teamtag = sheet[row][2].value
        colorcode = openpyxl.styles.colors.Color(rgb=colorDict[teamtag])
        cell.fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=colorcode)

# save beautiful workbook
workbook.save('G:\\My Drive\\Spielplanung\\GSP.xlsx')

# generate KG view

# create deep copy of GSP dataframe
df4KG = df.copy()

# remove unwanted columns
df4KG = df4KG.drop(columns=["gast_kurz", "heim_kurz", "liga", "spnr", "spt"])

# loop through all games one by one
for key, value in KampfgerichtZuteilung.kg.items():
    # write the responsible KG Team to the KG column of the row of the current unique game ID
    df4KG.loc[df4KG["id"] == key, "KG"] = value

df4KG = df4KG.sort_values(by="datum", ascending=True)
# write dataframe to excel
df4KG.to_excel("G:/My Drive/Spielplanung/KG.xlsx", index=False)

KG_workbook = openpyxl.load_workbook("G:\\My Drive\\Spielplanung\\KG.xlsx")
KG_sheet = KG_workbook.active
rowNum = KG_sheet.max_row

# Define the column letter you want to format (e.g., column A)
column_letter = 'C'

# set column width
width = 30
for column in col_List:
    KG_sheet.column_dimensions[column].width = width

# Iterate over the cells in the specified column and apply the time format
for cell in KG_sheet[column_letter]:
    cell.number_format = numbers.FORMAT_DATE_TIME3

# Iterate over all cells in each sheet
for row in KG_sheet.iter_rows():
    for cell in row:
        cell.alignment = Alignment(horizontal='right')
        cell.border = border

# loop first row
for cell in KG_sheet[1]:
    cell.font = bold_font
    cell.fill = gray_fill
    cell.alignment = Alignment(horizontal='center')

# Enable filters
KG_sheet.auto_filter.ref = KG_sheet.dimensions

# loop excel rows
for row in range(2, rowNum + 1, 1):

    # set blue color for homegames and gray for away
    if KG_sheet[row][3].value in ['TSV Wolnzach', 'TSV 1884 Wolnzach', 'TSV 1884 Wolnzach 2', 'TSV Wolnzach 2']:
        colorcode = openpyxl.styles.colors.Color(rgb="BDD7EE")
    else:
        colorcode = openpyxl.styles.colors.Color(rgb="BFBFBF")

    # loop row cells and color cells of individual rows in the same color
    for cell in KG_sheet[row]:

        # select teamtag, create colorcode and color all cells
        cell.fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=colorcode)

# save workbook
KG_workbook.save('G:\\My Drive\\Spielplanung\\KG.xlsx')

# Close the cursor and database connection
cursor.close()
cnx.close()

print("\n\n--------------------------------------")
print("\nGSP generation - Done!")
print("\n--------------------------------------")