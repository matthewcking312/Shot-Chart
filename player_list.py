import requests
import json
import pandas as pd 
import numpy as np

players_url = 'https://stats.nba.com/players/list/?Historic=Y'

# We will collect the data by pulling it directly from the JS script.
# We will collect: PlayerID, Players Name, First Season, Last Season, and Current Player

r = requests.get('https://stats.nba.com/js/data/ptsd/stats_ptsd.js')
s = str(r.text).replace('var stats_ptsd = ','').replace('};','}')
list_data = json.loads(s)['data']['players']

# Column Names for the data. We will eventually drop the last two columns
col_names = ['PlayerID', 'Name', 'Current Player', 'First Season', 'Last Season', 'Notsure', 'Notsure2']

# Storing the list in a pandas data frame. 
data = pd.DataFrame(list_data, columns=col_names)

# Dropping the two columns that we do not need.
data = data.drop(columns = ['Notsure', 'Notsure2'])
data.to_csv('player_list.csv')