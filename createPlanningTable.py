import mysql.connector
import config
import openpyxl
import openpyxl.styles
import pandas as pd
from datetime import datetime, timedelta, date
from openpyxl.styles import numbers, Alignment, Border, Side


def get_all_dates():

    # start and end date of the current planning period
    start_date = config.start
    end_date = config.end

    # Initialize an empty list to store the dates
    all_dates = []

    # Iterate over the range of dates between start and end dates
    current_date = start_date
    while current_date <= end_date:
        # Append the current date to the list
        all_dates.append(current_date.strftime("%Y-%m-%d"))

        # Increment the current date by one day
        current_date += timedelta(days=1)

    return all_dates


if __name__ == "__main__":

    lut_teamTags = {
                    "Platzhalter 1": "PH",
                    "Platzhalter 2": "PH",
                    "Platzhalter 3": "PH",
                    "Platzhalter 4": "PH",
                    "SV Althegnenberg":	"AHB",
                    "Ackermannbogen e.V.": "AKB",
                    "Ackermannbogen e.V. 1": "AKB",
                    "Ackermannbogen": "AKB",
                    "Ackermannbogen 2": "AKB",
                    "AK Tigers München": "AKTM",
                    "AK Tigers München 2": "AKTM",
                    "AK Tigers München 3": "AKTM",
                    "ASV Cham (AUF)": "CAM",
                    "ASV Rott": "ROTT",
                    "ASV Rott am Inn": "ROTT",
                    "ASV Rott am Inn 2": "ROTT",
                    "Baskets Vilsbiburg": "VIL",
                    "Baskets Vilsbiburg 3": "VIL",
                    "Baunach Young Pikes": "BAU",
                    "FC Baunach 1911": "BAU",
                    "BBC Bayreuth 2": "BAY",
                    "BC Erfurt": "ERF",
                    "BC Hellenen München": "HEL",
                    "BC Hellenen München 2": "HEL",
                    "BC Hellenen München 3": "HEL",
                    "BC Hellenen München 4": "HEL",
                    "BG Leitershofen/Stadtb. 2": "LEI",
                    "BG Litzendorf": "LIZ",
                    "BIG Basketball in Gotha": "GOT",
                    "Chinesischer SV München": "CSVM",
                    "Dachau Spurs": "DAC",
                    "DJK Eggolsheim": "EGG",
                    "DJK Landsberg": "LAB",
                    "DJK Landsberg 2": "LAB",
                    "DJK München Ost": "DJK",
                    "DJK München-Ost": "DJK",
                    "DJK Neustadt a. d. Waldnaab": "NST",
                    "DJK Pressath": "PRE",
                    "DJK SB München": "DJK",
                    "DJK SB München 2": "DJK",
                    "Dresden Titans 2": "DRE",
                    "Dresden Titans 3": "DRE",
                    "Dukes TV Dingolfing": "DIN",
                    "Dukes Dingolfing": "DIN",
                    "ESV Ingolstadt-Ringsee (AUF)": "ING",
                    "ESV Staffelsee": "STS",
                    "ESV Staffelsee 2": "STS",
                    "FC Aschheim": "ASC",
                    "FC Bayern München 1": "FCB",
                    "FC Bayern München 3": "FCB",
                    "FC Bayern München 4": "FCB",
                    "FC Bayern München Basketball 3": "FCB",
                    "FC Tegernheim": "TEG",
                    "FC Türk Sport Garching": "GAR",
                    "Fibalon Baskets Neumarkt": "NEU",
                    "Gautinger Sportclub e.V.": "GAU",
                    "Green Devils Schrobenhausen": "SOB",
                    "Haching Baskets": "UHA",
                    "Haching Baskets 2": "UHA",
                    "Haching Foxes": "UHA",
                    "MIL Baskets Milbertshofen": "MIL",
                    "MSG DJK SB Straubing/TSV Plattling": "MSG",
                    "MTSV Schwabing": "SWA",
                    "MTSV Schwabing (u19)": "SWA",
                    "MTSV Schwabing 2": "SWA",
                    "MTSV Schwabing 3": "SWA",
                    "MTSV Schwabing 4": "SWA",
                    "MTSV Schwabing 5": "SWA",
                    "MTV 1879 München": "MTV",
                    "MTV 1879 München 2": "MTV",
                    "MTV Baskets Ingolstadt": "ING",
                    "MTV München": "MTV",
                    "MTV München 1": "MTV",
                    "MTV München 2": "MTV",
                    "MTV München 3": "MTV",
                    "MTV Pfaffenhofen": "PAF",
                    "MTV Pfaffenhofen 2": "PAF",
                    "München Basket": "MB",
                    "München Basket 2": "MB",
                    "München Basket 3": "MB",
                    "MÜNCHEN BASKET 3": "MB",
                    "München Basket 4": "MB",
                    "Munich Fusion": "MFU",
                    "NaN": "NaN",
                    "NINERS Chemnitz e.V": "CHE",
                    "NINERS Chemnitz 2": "CHE",
                    "Nürnberger Basketball Club": "NBC",
                    "Ost Youngstars": "OST",
                    "Post SV Nürnberg": "PSV",
                    "PSV Ingolstadt": "PSVI",
                    "Regnitztal Baskets": "RET",
                    "Regensburg Baskets": "REG",
                    "SB DJK Rosenheim": "ROS",
                    "Science City Jena 3": "JEN",
                    "SC Wörnsmühl": "WÖR",
                    "SG Poing": "POI",
                    "SG Poing 2": "POI",
                    "Slama Jama Gröbenzell": "GRÖ",
                    "SpVgg Altenerding": "ERD",
                    "SpVgg Altenerding 2": "ERD",
                    "SpVgg Höhenkirchen": "HÖK",
                    "SpVgg Höhenkirchen 2": "HÖK",
                    "SV Allianz München": "SVA",
                    "SV Bad Tölz": "TÖL",
                    "SV Bad Tölz 2": "TÖL",
                    "SV Germering": "GER",
                    "SV Mammendorf": "MAM",
                    "SV Seeon": "SEE",
                    "SVN München": "SVN",
                    "SVN München e.V.": "SVN",
                    "SV Wacker Burghausen": "WAB",
                    "TB 1888 Erlangen": "ERL",
                    "TB Weiden": "WEI",
                    "TG Landshut": "LAN",
                    "TG Landshut 2": "LAN",
                    "TG TROPICS Würzburg": "WÜB",
                    "TS Jahn München": "JAN",
                    "TS Jahn München 2": "JAN",
                    "TS Jahn München 3": "JAN",
                    "TS Jahn München 4": "JAN",
                    "TS Regensburg": "REG",
                    "TV Feldkirchen": "FEL",
                    "TSV 1860 Rosenheim": "ROS",
                    "TSV 1860 München": "1860",
                    "TSV 1861 Nördlingen": "NÖR",
                    "TSV 1865 Dachau": "DAC",
                    "TSV 1865 Dachau 2": "DAC",
                    "TSV 1880 Schwandorf": "SWD",
                    "TSV 1884 Wolnzach": "WOZ",
                    "TSV 1884 Wolnzach 2": "WOZ",
                    "TSV 1884 Wolnzach 3": "WOZ",
                    "TSV 1884 Wolnzach 4": "WOZ",
                    "TSV Bad Reichenhall": "BRH",
                    "TSV Dorfen": "DOR",
                    "TSV 1864 Grafing": "GRA",
                    "TSV Grünwald": "GRÜ",
                    "TSV Haar": "HAR",
                    "TSV Ismaning": "ISM",
                    "TSV Ismaning 2": "ISM",
                    "TSV Jahn Freising": "FRE",
                    "TSV Jahn Freising 2": "FRE",
                    "TSV Jahn Freising 3": "FRE",
                    "TSV Jahn Freising 4": "FRE",
                    "TSV Jahn Freising 5": "FRE",
                    "TSV Milbertshofen": "MIL",
                    "TSV Milbertshofen 2": "MIL",
                    "TSV München Ost": "OST",
                    "TSV München Ost 1": "OST",
                    "TSV München Ost 2": "OST",
                    "TSV München Ost 3": "OST",
                    "TSV München Ost 4": "OST",
                    "TSV München-Forstenried": "FOR",
                    "TSV Neuötting": "NÖT",
                    "TSV Neuötting 2": "NÖT",
                    "TSV Oberhaching": "OHA",
                    "TSV Oberhaching 2": "OHA",
                    "TSV Olching": "OLC",
                    "TSV Ottobrunn": "OTT",
                    "TSV Ottobrunn 2": "OTT",
                    "TSV Ottobrunn (a.K)": "OTT",
                    "TSV Peiting": "PET",
                    "TSV Plattling": "PLA",
                    "TSV Schleißheim": "SLE",
                    "TSV Schleißheim 2": "SLE",
                    "TSV Schwaben Augsburg (AB)": "AUG",
                    "TSV Trudering": "TRU",
                    "TSV Trudering 2": "TRU",
                    "TSV Trudering Basketball": "TRU",
                    "TSV Trudering Basketball 2": "TRU",
                    "TSV Unterhaching": "UHA",
                    "TSV Unterhaching 2": "UHA",
                    "TSV Utting": "UTT",
                    "TSV Vaterstetten": "VAT",
                    "TSV Vaterstetten 2": "VAT",
                    "TSV Vilsbiburg 2": "VIB",
                    "TSV Weilheim": "WEH",
                    "TSV Wolnzach": "WOZ",
                    "TSV Wolnzach 2": "WOZ",
                    "TuS Bad Aibling": "AIB",
                    "TuS Bad Aibling 2": "AIB",
                    "TuS Bad Aibling Fireballs 2": "AIB",
                    "TuS Fürstenfeldbruck": "FFB",
                    "TuS Fürstenfeldbruck 2": "FFB",
                    "TuS Holzkirchen": "HOL",
                    "TuS Holzkirchen 2": "HOL",
                    "TuS Mitterfelden": "MIF",
                    "TuS 1860 Pfarrkirchen": "PFA",
                    "TuS Prien a. Chiemsee 1878": "PRI",
                    "TuS Traunreut": "TRAU",
                    "TuSpo Heroldsberg": "HER",
                    "TV 1847 Augsburg": "AUG",
                    "TV 1862 Passau": "PAS",
                    "TV 1862 Passau 2": "PAS",
                    "TV 1863 Miesbach": "MIS",
                    "TV 1881 Altdorf": "ALT",
                    "TSV 1864 Haag": "HAA",
                    "TV 1868 Burghausen e.V.": "BUR",
                    "TV Dingolfing 1868 (AUF)": "DIN",
                    "TV Dingolfing 1868": "DIN",
                    "TV Goldbach 1897": "GOL",
                    "TV Markt Schwaben": "MSW",
                    "TV Miesbach": "MIS",
                    "TV Traunstein": "TRA",
                    "TV von 1895 Markt Schwaben": "MSW",
                    "USC Leipzig 2": "LPZ",
                    "VfL Treuchtlingen 2": "TRE",
                    "VfL Waldkraiburg": "WAK",
                    "VfR Garching": "GAR",
                    "VfR Garching 2": "GAR",
                    "WSV Glonn": "GLO",
                    "TSV 1880 Wasserburg": "WAS",
                    "TSV 1880 Wasserburg 2": "WAS",
                    "TSV 1880 Wasserburg 3": "WAS",
                    "ONLINEPRINTERS Neustadt a.d. Aisch": "NAA",
                    "Schanzer Baskets Ingolstadt": "ING",
                    "ASV Cham": "CHA",
                    "DJK Don Bosco Bamberg": "BAM",
                    "Puchheim 46ers": "PUC",
                    "Basketballclub Zwickau": "ZWI",
                    "GGZ Baskets Zwickau": "ZWI"
                    }

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
        'u121',
        'u122',
        'u10'
    ]

    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sqlServerPW1312",
        database="spielplanung"
    )

    # Create a cursor
    cursor = cnx.cursor()

    # Fetch data from each table
    results = []

    for table in table_names:
        # Execute the SELECT query
        query = f"SELECT * FROM {table}"
        cursor.execute(query)

        # Fetch all the results
        results.extend(cursor.fetchall())
    
    dates = [i[4] for i in results]
    team = [i[2] for i in results]
    gametime = [i[5] for i in results]
    hometeam = [i[6] for i in results]
    awayteam = [i[7] for i in results]
    days = get_all_dates()

    # Create a DataFrame from the data
    df = pd.DataFrame(index=days, columns=table_names)

    # loop through all games one by one
    for index in range(0, len(dates)):
        if hometeam[index] in ['TSV 1884 Wolnzach', 'TSV 1884 Wolnzach 1', 'TSV 1884 Wolnzach 2', 'TSV Wolnzach', 'TSV Wolnzach 2']:
            df.loc[dates[index].__str__(), team[index]] = str(gametime[index])[:-3] + " vs " + str(lut_teamTags[awayteam[index]])
        else:
            df.loc[dates[index].__str__(), team[index]] = str(gametime[index])[:-3] + " @ " + str(lut_teamTags[hometeam[index]])

    # Save the pivot table to an Excel file
    df.to_excel("planningTable.xlsx")

    # create beautiful excel table
    workbook = openpyxl.load_workbook("planningTable.xlsx")
    sheet = workbook.active

    # Define border style
    border = Border(
        left=Side(border_style='thin', color='000000'),
        right=Side(border_style='thin', color='000000'),
        top=Side(border_style='thin', color='000000'),
        bottom=Side(border_style='thin', color='000000')
    )

    # color first column
    first_column = sheet["A"]
    bold_font = openpyxl.styles.Font(bold=True, size=15)
    weekendGray = openpyxl.styles.colors.Color(rgb='969696')
    ferienYellow = openpyxl.styles.colors.Color(rgb='CCFFCC')
    blockedRed = openpyxl.styles.colors.Color(rgb='993300')
    headingGray = openpyxl.styles.colors.Color(rgb='CCCCFF')

    weekend_fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=weekendGray)
    ferien_fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=ferienYellow)
    blocked_fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=blockedRed)
    heading_fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=headingGray)

    # loop all cells
    for row in sheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal='right')
            cell.border = border

    # color all weekends
    for row_index in range(2, 250, 7):
        for cell in sheet[row_index]:
            cell.fill = weekend_fill
        for cell in sheet[row_index + 1]:
            cell.fill = weekend_fill

    # color public holidays
    for Ferien_date in config.Holidays:
        for row_ind, rowC in enumerate(sheet.iter_rows(values_only=True), start=1):
            if Ferien_date in rowC:
                cell_coord = "N" + str(row_ind)
                sheet[cell_coord] = "Schulferien"
                for blockRow in range(row_ind, row_ind + 2):
                    for cell in sheet[blockRow]:
                        if cell.column_letter == "N":
                            cell.font = bold_font
                            break
                        cell.fill = ferien_fill
                break

    # color additional events (clean this mess up pls lol)
    for item in config.additional_events.items():
        for row_ind, rowC in enumerate(sheet.iter_rows(values_only=True), start=1):
            if item[1][0] in rowC:
                if type(item[1][1]) == int:
                    blockedDays = item[1][1]
                    cell_coord = "N" + str(row_ind)
                    sheet[cell_coord] = item[0]
                    for blockRow in range(row_ind, row_ind + blockedDays):
                        for cell in sheet[blockRow]:
                            if cell.column_letter == "N":
                                cell.font = bold_font
                                break
                            cell.fill = blocked_fill
                    break

                if type(item[1][1]) == str:
                    cell_coord = "N" + str(row_ind)
                    sheet[cell_coord] = item[0] + " um " + item[1][1]
                    for cell in sheet[row_ind]:
                        if cell.column_letter == "N":
                            cell.font = bold_font
                            break
                        cell.fill = blocked_fill
                    break

    # loop first column
    for cell in first_column:
        cell.font = bold_font
        cell.fill = heading_fill

    # loop first row
    for cell in sheet[1]:
        cell.font = bold_font
        cell.fill = heading_fill
        cell.alignment = Alignment(horizontal='centerContinuous')

    col_List = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    width = 20
    for column in col_List:
        sheet.column_dimensions[column].width = width

    # Save the modified workbook
    workbook.save('G:\\My Drive\\Spielplanung\\planningTable.xlsx')
    print("\n\n--------------------------------------")
    print("\nPlanning Table generation - Done!")
    print("\n--------------------------------------")
    print("\n\nIch bin ein kranker Hacker :D\n\n")

