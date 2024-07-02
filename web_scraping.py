import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import random
from selenium import webdriver
import time


def main():
    #parse_team_rankings()
    print('main')

#######################################  MVP  #######################################

def scrape_mvps():
    url_start = 'https://www.basketball-reference.com/awards/awards_{}.html'
    headers = {
        'User-agent':"Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/113.0",
    }
    years = list(range(1991,2025))

    for year in years:
        url = url_start.format(year)
        response = requests.get(url,headers=headers,verify=False)
        sleep(random.randrange(5,10))#Website blocks 20 requests wtihin a minute

        with open('mvp/{}.html'.format(year), 'w+',encoding='utf-8') as f:
            f.write(response.text)

def parse_mvp_data():
    years = list(range(1991,2025))
    dfs = []

    for year in years:
        with open("mvp/{}.html".format(year),encoding='utf-8') as f:
            page = f.read()
        soup = BeautifulSoup(page, 'html.parser')
        soup.find('tr', class_ = "over_header").decompose()
        mvp_table = soup.find_all(id='mvp')
        mvp = pd.read_html(str(mvp_table))[0]
        mvp["Year"] = year

        dfs.append(mvp)

    mvps = pd.concat(dfs)
    mvps.to_csv('mvps.csv')

#######################################  Player Stats  #######################################

def scrape_player_stats():
    url_start = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'

    driver = webdriver.Chrome(executable_path='/path/to/executable')
    years = list(range(1991,2025))

    for year in years:
        url = url_start.format(year)
        driver.get(url)
        driver.execute_script("window.scrollTo(1,100000)")
        time.sleep(2)
        
        html = driver.page_source

        with open('player_stats/{}.html'.format(year), 'w+',encoding='utf-8') as f:
            f.write(html)

def parse_player_stats():
    dfs = []
    years = list(range(1991,2025))
    for year in years:
        with open('player_stats/{}.html'.format(year), 'w+',encoding='utf-8') as f:
            page = f.read()
        soup = BeautifulSoup(page,'html.parser')
        soup.find('tr',class_='thead').decompose()
        player_stats_table = soup.find(id='per_game_stats')
        player_stats = pd.read_html(str(player_stats_table))[0]
        player_stats['Year'] = year

        dfs.append(player_stats)

    players = pd.concat(dfs)
    players.to_csv('players.csv')

#######################################  Team Data  #######################################
        
def scrape_team_rankings():
    url_start = 'https://www.basketball-reference.com/leagues/NBA_{}_standings.html'
    headers = {
        'User-agent':"Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/113.0",
    }
    years = list(range(1991,2025))
    for year in years:
        url = url_start.format(year)
        response = requests.get(url,headers=headers,verify=False)
        sleep(random.randrange(5,10))

        with open('team_rankings/{}.html'.format(year), 'w+',encoding='utf-8') as f:
            f.write(response.text)

def parse_team_rankings():
    dfs = []
    years = list(range(1991,2025))

    for year in years:
        with open('team_rankings/{}.html'.format(year),encoding='utf-8') as f:
            page = f.read()

        soup = BeautifulSoup(page, 'html.parser')
        soup.find('tr', class_ = "thead").decompose()
        team_table = soup.find_all(id='divs_standings_E')
        team = pd.read_html(str(team_table))[0]
        team["Year"] = year
        team['Team'] = team['Eastern Conference']  
        del team['Eastern Conference'] 
        dfs.append(team)

        soup = BeautifulSoup(page, 'html.parser')
        soup.find('tr', class_ = "thead").decompose()
        team_table = soup.find_all(id='divs_standings_W')
        team = pd.read_html(str(team_table))[0]
        team["Year"] = year
        team['Team'] = team['Western Conference']  
        del team['Western Conference'] 
        dfs.append(team)   

    teams = pd.concat(dfs)
    teams.to_csv('teams.csv')   




if __name__ == "__main__":
    main() 