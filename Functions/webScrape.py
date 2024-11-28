# Import libraries and functions
import requests
from bs4 import BeautifulSoup

team_dict = {
    "ARI": "dbacks", "ATL": "braves", "BAL": "orioles", "BOS": "redsox", "CHC": "cubs",
    "CHW": "whitesox", "CIN": "reds", "CLE": "guardians", "COL": "rockies", "DET": "tigers",
    "MIA": "marlins", "HOU": "astros", "KAN": "royals", "LAA": "angels", "LAD": "dodgers",
    "MIL": "brewers", "MIN": "twins", "NYM": "mets", "NYY": "yankees", "OAK": "athletics",
    "PHI": "phillies", "PIT": "pirates", "SDP": "padres", "SFG": "giants", "SEA": "mariners",
    "STL": "cardinals", "TBR": "rays", "TEX": "rangers", "TOR": "bluejays", "WAS": "nationals"
}

def getRoster(team_acronym):
    url = f"https://www.mlb.com/{team_dict[team_acronym]}/roster/40-man"    

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        player_table  = soup.find_all('tr')

        player_info = {}
        for row in player_table:
            line = row.find('a')
            if line:
                player_info[int(line['href'].split('/')[-1])] = line.text.strip() 
    return player_info


