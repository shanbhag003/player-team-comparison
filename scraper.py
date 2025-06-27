import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

FBREF_PLAYER_INDEX = "https://fbref.com/en/players/"
FBREF_TEAM_INDEX = "https://fbref.com/en/squads/"

@st.cache_data(show_spinner=False)
def get_all_players():
    res = requests.get(FBREF_PLAYER_INDEX)
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.find("div", {"id": "div_players"})
    players = table.find_all("p")

    player_dict = {}
    for p in players:
        try:
            a = p.find("a")
            name = a.text.strip()
            href = a["href"]
            full_url = "https://fbref.com" + href
            player_dict[name] = full_url
        except:
            continue
    return player_dict

@st.cache_data(show_spinner=False)
def get_all_teams():
    res = requests.get(FBREF_TEAM_INDEX)
    soup = BeautifulSoup(res.text, "lxml")
    table = soup.find("div", {"id": "content"})
    teams = table.find_all("a", href=True)

    team_dict = {}
    for a in teams:
        name = a.text.strip()
        href = a["href"]
        if "/en/squads/" in href and "matchlogs" not in href:
            team_dict[name] = "https://fbref.com" + href
    return team_dict

@st.cache_data(show_spinner=False)
def get_player_stats(url):
    tables = pd.read_html(url)
    return tables[0]  # You can refine this index as needed

@st.cache_data(show_spinner=False)
def get_team_stats(url):
    tables = pd.read_html(url)
    return tables[0]  # You can refine this index as needed
