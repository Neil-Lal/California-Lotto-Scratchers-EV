import pyodbc
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sqlalchemy
from datetime import datetime
from time import sleep
from random import randint

## Variables
    # Webpage to scrape
#websites = ["http://www.calottery.com/Play/Scratchers-games/$30-Scratchers/bonus-play-millions-1313"]
websites = ["http://www.calottery.com/play/scratchers-games/$1-scratchers",
            "http://www.calottery.com/play/scratchers-games/$2-scratchers",
            "http://www.calottery.com/play/scratchers-games/$3-scratchers",
            "http://www.calottery.com/play/scratchers-games/$5-scratchers",
            "http://www.calottery.com/play/scratchers-games/$10-scratchers",
            "http://www.calottery.com/play/scratchers-games/$20-scratchers",
            "http://www.calottery.com/play/scratchers-games/$30-scratchers"]
PK_ID = 0
date = datetime.now().strftime("%Y-%m-%d %H:%M")

## Connect to MSSQL server and send data
    # Takes in list of pandas dataframes and table to insert into
    # No return; Adds data to table
def toSQL(frame,table_name):
    engine = sqlalchemy.create_engine('mssql+pyodbc://DESKTOP-L0JOFBL\TOPSDATA_ME/topsdata_CalLotto?driver=SQL+Server')
    for i in frame:
        i.to_sql(name=table_name,con=engine,if_exists='append', index=False)

## Grab highest PK ID
def grabPK():
    engine = sqlalchemy.create_engine('mssql+pyodbc://DESKTOP-L0JOFBL\TOPSDATA_ME/topsdata_CalLotto?driver=SQL+Server')
    con = engine.connect()
    r = con.execute('SELECT MAX(Ticket_ID)+1 FROM Scratchers_Prices')
    return r.fetchone()[0]
PK_ID = grabPK()

## Retrieve Data from Website
    # Takes in a list of webpages to scrape
    # Returns a list of pandas dataframes containing Scratcher data and prices
def scrapper(websites,PK_ID):
    PK_ID = PK_ID
    framesScratchers = []
    framesPrices = []
    urls = []
    keys = []
    for i in websites:
        tickets = []

        page = requests.get(i)
        soup = bs(page.text, 'html.parser')
        ticks = soup.find_all(class_='scratcher-small')

        # Add price data - applies to each ticket in website
        price = i.split('$')[1].split('-')[0]
        for row in ticks:
            tick_url = row.find_all('a',href=True)
            tick_img = row.find_all('img')

            if len(tick_url) > 0:
                url = "http://www.calottery.com" + tick_url[0]['href']
                urls.append(url)
            else:
                url = ''
                urls.append('')
            if len(tick_img) > 0:
                img = tick_img[0]['src']
            else:
                img = ''
               
            ticket_ID = PK_ID
            keys.append(ticket_ID)
            PK_ID += 1
            rows = {'price': price,'url': url, 'img' : img, 'Ticket_ID': ticket_ID}
            tickets.append(rows)
        sleep(randint(1,2))
        framesPrices.append(pd.DataFrame(tickets))
    for i in range(len(urls)):
        prizeList = []
        key = keys[i]
        page = requests.get(urls[i])
        soup = bs(page.text, 'html.parser')
        oddsAndPrizes = soup.select("table.draw_games.tag_even tr")
    
        title = soup.find(class_="heroContentBox")
        name = list(title.find("h1").stripped_strings)[0]

        for table_row in oddsAndPrizes:
            cells = table_row.findAll('td')

            if len(cells) > 0:
                
                prizes = list(cells[0].stripped_strings)[0].replace(',','') 
                odds = list(cells[1].stripped_strings)[0].replace(',','')
                totalWinners = list(cells[2].stripped_strings)[0].replace(',','')
                prizesClaimed = list(cells[3].stripped_strings)[0].replace(',','')
                prizesAvailable = list(cells[4].stripped_strings)[0].replace(',','')

                rows = {'Ticket_ID': key, 'Extract_Date': date,'Ticket_name': name, 'Prizes': prizes, 'Odds': odds, 'Total_winners': totalWinners, 'Prizes_claimed': prizesClaimed, 'Prizes_available': prizesAvailable}
                prizeList.append(rows)
        
        framesScratchers.append(pd.DataFrame(prizeList))
        sleep(randint(1,2))
    return [framesScratchers, framesPrices]
       

def main():
    f = scrapper(websites,PK_ID)
    toSQL(f[1],'Scratchers_Prices')
    toSQL(f[0],'Scratchers_Data')
    


main()