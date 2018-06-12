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
websites = ["http://www.calottery.com/Play/Scratchers-games/$30-Scratchers/bonus-play-millions-1313"]


## Retrieve Data from Website
    # Start with one game then later on add the rest of the variations
    # http://www.calottery.com/play/scratchers-games
    # http://www.calottery.com/play/scratchers-games/$1-scratchers
    # http://www.calottery.com/play/scratchers-games/$2-scratchers
    # http://www.calottery.com/play/scratchers-games/$3-scratchers
    # http://www.calottery.com/play/scratchers-games/$5-scratchers
    # http://www.calottery.com/play/scratchers-games/$10-scratchers
    # http://www.calottery.com/play/scratchers-games/$20-scratchers
    # http://www.calottery.com/play/scratchers-games/$30-scratchers
    # Takes in a list of webpages to scrape
    # Returns a list of pandas dataframes containing prize data
def scrapper(websites):
    frames = []
    for i in websites:
        prizeList = []
        page = requests.get(i)
        soup = bs(page.text, 'html.parser')
        oddsAndPrizes = soup.select("table.draw_games.tag_even tr")
    
        title = soup.find(class_="heroContentBox")
        name = list(title.find("h1").stripped_strings)[0]

        for table_row in oddsAndPrizes:
            cells = table_row.findAll('td')

            if len(cells) > 0:
                date = datetime.now().strftime("%Y-%m-%d %H:%M")
                prizes = list(cells[0].stripped_strings)[0].replace(',','') 
                odds = list(cells[1].stripped_strings)[0].replace(',','')
                totalWinners = list(cells[2].stripped_strings)[0].replace(',','')
                prizesClaimed = list(cells[3].stripped_strings)[0].replace(',','')
                prizesAvailable = list(cells[4].stripped_strings)[0].replace(',','')

                rows = {'Extract_Date': date,'Ticket_name': name, 'Prizes': prizes, 'Odds': odds, 'Total_winners': totalWinners, 'Prizes_claimed': prizesClaimed, 'Prizes_available': prizesAvailable}
                prizeList.append(rows)

        frames.append(pd.DataFrame(prizeList))
        sleep(randint(1,4))
    return frames
       
## Connect to MSSQL server
    # Takes in list of pandas dataframes
    # No return; Adds data to Scratchers table
def SQL(frames):
    engine = sqlalchemy.create_engine('mssql+pyodbc://DESKTOP-L0JOFBL\TOPSDATA_ME/topsdata_CalLotto?driver=SQL+Server')
    for i in frames:
        i.to_sql(name="Scratchers",con=engine,if_exists='append', index=False)




def main():
    f = scrapper(websites)
    print(f[0].head(10))
    SQL(f)




main()