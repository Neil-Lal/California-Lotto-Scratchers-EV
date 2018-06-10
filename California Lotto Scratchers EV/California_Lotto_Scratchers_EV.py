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
    page = requests.get(i)
    soup = bs(page.text, 'html.parser')
    oddsAndPrizes = soup.find(class_='table.draw_games')
    
    df = pd.DataFrame(oddsAndPrizes)
    
    print(oddsAndPrizes)
    print(df.head())
    


##