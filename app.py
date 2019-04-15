import dash
import dash_core_components as dcc 
import dash_html_components as html 
import pandas as pd 
import numpy as np 
import requests
import json
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Import all of our players that users will be able to select from.
player_list = pd.read_csv('player_list.csv')
# From the player list, we want to create a python dictionary. It should contain their values
# player_ID, and name. The name will be what is displayed, and the playerID will allow us to request the data.



# This will allow us to gather the shot chart data for the individual player.
def get_shot_data(player_id, season):
    url_start = f'https://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=33&CFPARAMS={season}&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID=&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID='
    url_end = f'&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&Season={season}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5=&VsTeamID='
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    full_url = url_start + str(player_id) + url_end
    json_dat = requests.get(full_url, headers=headers).json()
    return(json_dat)

player_id=2544
season='2017-18'

# Gather the data for the player and season you are interested in.
json_dat = get_shot_data(player_id=player_id, season=season)

# Reduce our data to only have the columns that we are looking for.
data = json_dat['resultSets'][0]['rowSet']
cols = json_dat['resultSets'][0]['headers']

# For ease of use, we will put our data in a pandas dataframe.
df = pd.DataFrame.from_records(data, columns=cols)

df = df.drop(columns=['GRID_TYPE'])

colors = {
	'background': '#111111',
	'text': '#7FDBFF'
}

# Create the scatters for the missed shots and the made shots.

missed_shot_trace = go.Scatter(
    x = df[df['EVENT_TYPE'] == 'Missed Shot']['LOC_X'],
    y = df[df['EVENT_TYPE'] == 'Missed Shot']['LOC_Y'],
    mode = 'markers',
    name = 'Miss',
    marker = {'color':'blue', 'size':5}
)

made_shot_trace = go.Scatter(
    x = df[df['EVENT_TYPE'] == 'Made Shot']['LOC_X'],
    y = df[df['EVENT_TYPE'] == 'Made Shot']['LOC_Y'],
    mode = 'markers',
    name = 'Make',
    marker = {'color':'red', 'size':5}
)

# Organized these scatters and combine them together. 
data = [missed_shot_trace, made_shot_trace]

app.layout = html.Div(children=[
    html.H1(
    	children='Player Shot Chart',
    	style={
    		'textAlign': 'center',
    		'color': colors['text']
    	}
    ),

    html.Div(children='''
        NBA Player Shot Chart
    ''',
    style={
        'textAlign': 'center'
        # 'color': colors['text']
    }),

    dcc.Dropdown(
            options=(
            	player_list.reindex(['Name', 'PlayerID'], axis=1)
			   .set_axis(['label', 'value'], axis=1, inplace=False)
			   .to_dict('r')),
            value=(list(map(str, player_list['PlayerID']))),
            placeholder="Select a Player",
            multi=False,
            searchable=True,
            className='six columns',
            id='item-selector'),

 #    dcc.Dropdown(
	#     options=[
	#         {'label': 'New York City', 'value': 'NYC'},
	#         {'label': 'Montreal', 'value': 'MTL'},
	#         {'label': 'San Francisco', 'value': 'SF'}
 #    ],
	#     value=['MTL', 'NYC'],
	#     multi=False
	# ),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [missed_shot_trace, made_shot_trace],
            'layout':
                go.Layout(
				    title = 'Player Shot Chart',
				    showlegend = True,
				    xaxis = {'showgrid':False, 'range':[-300, 300]},
				    yaxis = {'showgrid':False, 'range':[-100, 500]},
				    height = 600,
				    width = 650#,
				    #shapes = court_shapes
				),
        },
        style={'display': 'inline-block', 'horizontal-align': 'center'}
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)