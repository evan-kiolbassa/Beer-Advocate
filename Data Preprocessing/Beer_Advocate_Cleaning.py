# Importing production data from directory
import glob
import os
import pandas as pd
import datetime
import re
def production_cleaning():
    path = r"C:\Users\mmotd\OneDrive\Documents\Boot Camp Files\Beer Production"
    all_files = glob.glob(path + "/*.xlsx")
    production = pd.DataFrame()
    for f in all_files:
        data = pd.read_excel(f)
        data = data[7:19]
        data = data[1:]
        date = re.findall('\d+', f)
        date = listToString(date)

        data['Year'] = date
        production = production.append(data)   
    production.columns = ['Barrels', 'Number of Breweries', 'Total Barrels', 'Taxable Removals', 'Total Exported', 'Year']
    production.index = range(0,132)

    production = production[production['Barrels'] != 'Barrels (31 gallons) (2)']
    production = production[production['Barrels'] != 'Total']
    production['Barrels'] = production['Barrels'].str.strip()
    
    cleaned_production = production.copy()
    
    return cleaned_production

def scraped_cleaning():
    beer_advocate = pd.read_csv("advocate_data.csv")
    beer_advocate = beer_advocate.dropna(subset = ['avg_rating'])
    beer_advocate = beer_advocate.apply(lambda x: x.str.replace(',',""))
    beer_advocate['total_rank'] = beer_advocate['total_rank'].filter(regex = '\d+')
    beer_advocate['total_rank'] = beer_advocate['total_rank'].str.replace('<a href="/beer/top-rated/" class="Tooltip" title="Ranking against all beers. Click to view the Top 250 Rated Beers.">Ranked #',"")
    beer_advocate['total_rank'] = beer_advocate['total_rank'].str.replace('</a>', '')
    beer_advocate['style_rank'] = beer_advocate['style_rank'].str.replace('Ranked #',"")
    beer_advocate.loc[:, ['total_rank', 'style_rank', 'num_ratings']] = beer_advocate.loc[:, ['total_rank', 'style_rank', 'num_ratings']].apply(lambda x: x.astype(float))
    beer_advocate['beer_desc'] = beer_advocate['beer_desc'].str.strip(',\n')
    
    return beer_advocate


