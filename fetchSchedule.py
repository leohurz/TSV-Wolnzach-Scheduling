"""
This is a script used to fetch basketball schedules from TeamSL Website for TSV Wolnzach. It is run in combination with
mySql private Server.

Created for the Season 23/24

Author: Leo Hurzlmeier

"""
import mysql.connector
import time
import config
from selenium import webdriver
from bs4 import BeautifulSoup, Tag
import datetime
from selenium.webdriver.chrome.options import Options
import logging
import os
import bs4


def retrieve_schedule_data(username, password, login_url, data_url, team_tag, liga):
    """
    retrieves schedule data of all teams from teamSL website and saves it to a dictionnary.

    :param username: teamSL username
    :param password: teamSL password
    :param login_url: teamSL login url
    :param data_url: teamSL url with schedule
    :param team_tag: lol
    :param liga: lol
    :return:
        gamedict: dictionnary containing each matchup as one item
    """

    # set chrome driver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--silent')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Launch a web browser
    driver = webdriver.Chrome(options=chrome_options)

    # Access the login page
    driver.get(login_url)

    # Fill in the login form
    username_input = driver.find_element_by_name("username")  # Update the name attribute here
    password_input = driver.find_element_by_name("password")  # Update the name attribute here
    username_input.send_keys(username)
    password_input.send_keys(password)

    # Submit the login form
    button = driver.find_element_by_css_selector('a.button[title="klicken Sie hier, um Sich anzumelden!"]')
    button.click()

    # Access the target page after successful login
    driver.get(data_url)

    # Get the HTML content of the target page
    html_content = driver.page_source

    # prettify
    soup = BeautifulSoup(html_content, 'html.parser')

    # select the tables containing the games
    planTab = soup.select("table.sportView")[2]

    # select all rows containing game information
    allCols = planTab.select("tr")

    # check whether bearbeiten is there or not
    if 'Bearbeiten' in planTab.select("tr")[8].text:
        allCols = allCols[9:]
    else:
        allCols = allCols[8:]

    # inits
    gamedict = {}

    # write game info to dictionary
    for index, row in enumerate(allCols):
        elements = row.select("nobr")
        templist = []

        for elIndex in range(0, 6):
            try:
                templist.append(elements[elIndex].contents[0])
            except IndexError:
                templist.append("NaN")

        # catches exceptions when Referees are set. These happen, because the referee field actually has multiple
        # elements in contrary to normal game information fields
        if type(templist[0]) != bs4.element.NavigableString:
            continue

        gamedict[index] = templist

    driver.quit()

    # key removal list
    keysToRemove = []

    # clean dict
    for key, value in gamedict.items():

        # check whether the game was cancelled by checking for <strike> datatype
        if type(value[2]) == Tag:
            keysToRemove.append(key)
            continue

        strings = value[2].split()
        value[2] = strings[0]
        value.insert(3, strings[1])
        value.insert(2, team_tag)
        value.insert(3, liga)
        value[4] = value[4].replace('.', '-')
        value[5] = value[5] + ':00'
        value[4] = datetime.datetime.strptime(value[4], "%d-%m-%Y").strftime("%Y-%m-%d")
        value.append(str(value[0]) + value[2])  # generate unique game identifier

    # remove games that were cancelled from dict
    for key in keysToRemove:
        gamedict.pop(key)

    return gamedict


def send_data_to_mysql(inputDict, team_tag):
    """
    connects to local mySQL server, prepares data and transmits it to sql database

    :param inputDict: schedule information for the current team in dictionary form
    :param team_tag: lol
    :return: nothing :D
    """

    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sqlServerPW1312",
        database="spielplanung"
    )

    # Define the table name
    table_name = team_tag

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # clear all table data
    clear_query = f'DELETE FROM {table_name}'
    cursor.execute(clear_query)

    columns = ['spnr', 'spt', 'team', 'liga', 'datum', 'uhrzeit', 'heim', 'gast', 'halle', 'id']

    for index, item in enumerate(inputDict.values()):

        values = item

        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Execute the query with the dictionary values
        cursor.execute(query, values)

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and database connection
    cursor.close()
    cnx.close()


if __name__ == "__main__":

    team_tags = [
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

    ligen = [
             'ByLHM',
             'bzld',
             'MI-KLHB',
             'MI-BK18M-N',
             'kü-kl18w',
             'MI-KL16M-N',
             'we-kl16w-a',
             'BZL14M',
             'MI-KL14M-N',
             'KK14M',
             'kl14w-b'
             'MI-BK12M-N',
             'u12KK-N',
             'MI-KL10M-N'
             ]

    liga_urls = {
        'h1': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=52531&mmb=1&mannschaft_liga_id=437195",
        'd1': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53876&mmb=1&mannschaft_liga_id=447108",
        'h2': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53736&mmb=1&mannschaft_liga_id=454722",
        'u18': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53747&mmb=1&mannschaft_liga_id=446106",
        'u18w': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53755&mmb=1&mannschaft_liga_id=460836",
        'u16': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53778&mmb=1&mannschaft_liga_id=456441",
        'u16w': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53782&mmb=1&mannschaft_liga_id=460029",
        'u141': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53792&mmb=1&mannschaft_liga_id=460198",
        'u142': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53798&mmb=1&mannschaft_liga_id=456434",
        'u121': "https://www.basketball-bund.net/index.jsp?Action=8200&liga_id=53813&mmb=1&mannschaft_liga_id=446693",
        'u122': "",
        'u10': ""
    }

    for index, item in enumerate(liga_urls.items()):

        if item[1] != "":
            gameDict = retrieve_schedule_data(config.username, config.password, config.login_url, item[1], item[0], ligen[index])
            send_data_to_mysql(gameDict, item[0])
            print(f'\n{item[0]} done!')

        else:
            print(f'\n{item[0]} not found :(')
            continue
    print("\n\n--------------------------------------")
    print("\nRetrieve Data - Done!")
    print("\n--------------------------------------")