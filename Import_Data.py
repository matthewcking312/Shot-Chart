%matplotlib inline
import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json


url_start = 'https://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=33&CFPARAMS=2017-18&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID=&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID='
url_end = '&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&PlayerPosition=&PointDiff=&Position=&RangeType=0&RookieYear=&Season=2017-18&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StartPeriod=1&StartRange=0&StarterBench=&TeamID=0&VsConference=&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5=&VsTeamID='
headers = {"headers":["GRID_TYPE","GAME_ID","GAME_EVENT_ID","PLAYER_ID","PLAYER_NAME","TEAM_ID","TEAM_NAME","PERIOD","MINUTES_REMAINING","SECONDS_REMAINING","EVENT_TYPE","ACTION_TYPE","SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA","SHOT_ZONE_RANGE","SHOT_DISTANCE","LOC_X","LOC_Y","SHOT_ATTEMPTED_FLAG","SHOT_MADE_FLAG","GAME_DATE","HTM","VTM"]}
# player_id = 204001

def get_shot_data(player_id):
    full_url = url_start + str(player_id) + url_end
    json = requests.get(full_url, headers=headers).json()
    return(json)
get_shot_data(204001)