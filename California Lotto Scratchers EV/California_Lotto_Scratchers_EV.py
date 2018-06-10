import pypyodbc
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

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

websites = ["http://www.calottery.com/Play/Scratchers-games/$30-Scratchers/bonus-play-millions-1313"]
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
            prizes = list(cells[0].stripped_strings)[0] 
            odds = list(cells[1].stripped_strings)[0]
            totalWinners = list(cells[2].stripped_strings)[0]
            prizesClaimed = list(cells[3].stripped_strings)[0]
            prizesAvailable = list(cells[4].stripped_strings)[0]

            rows = {'name': name, 'prizes': prizes, 'odds': odds, 'totalWinners': totalWinners, 'prizesClaimed': prizesClaimed, 'prizesAvailable': prizesAvailable}
            prizeList.append(rows)

    df = pd.DataFrame(prizeList)

##

## Connect to MSSQL server


##