import pandas as pd

def get_player_stats(url):
    tables = pd.read_html(url)
    return tables[0]  # You can change index based on structure

def get_team_stats(url):
    tables = pd.read_html(url)
    return tables[0]  # You can change index based on structure
