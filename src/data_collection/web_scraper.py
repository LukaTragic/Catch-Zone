import requests
from bs4 import BeautifulSoup
from typing import Dict

TEAM_DICT = {
    "ARI": "dbacks", "ATL": "braves", "BAL": "orioles", "BOS": "redsox", "CHC": "cubs",
    "CHW": "whitesox", "CIN": "reds", "CLE": "guardians", "COL": "rockies", "DET": "tigers",
    "MIA": "marlins", "HOU": "astros", "KAN": "royals", "LAA": "angels", "LAD": "dodgers",
    "MIL": "brewers", "MIN": "twins", "NYM": "mets", "NYY": "yankees", "OAK": "athletics",
    "PHI": "phillies", "PIT": "pirates", "SDP": "padres", "SFG": "giants", "SEA": "mariners",
    "STL": "cardinals", "TBR": "rays", "TEX": "rangers", "TOR": "bluejays", "WAS": "nationals"
}


def get_roster(team_acronym: str, current: bool) -> Dict[int, str]:
    """
    Retrieve MLB team roster from optional website.
    
    Args:
        team_acronym (str): Three-letter team acronym
        current (bool): If current roster should be used
    
    Returns:
        Dict[int, str]: Dictionary of player IDs and names
    """
    # default value is 2024 Yankees        
    if current:
        url = f"https://www.mlb.com/{TEAM_DICT[team_acronym]}/roster/40-man"    
    else:
        url = "https://web.archive.org/web/20241007121158/https://www.mlb.com/yankees/roster/40-man"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        player_table = soup.find_all('tr')

        player_info = {}
        for row in player_table:
            line = row.find('a')
            if line and line.get('href'):
                try:
                    player_id = int(line['href'].split('/')[-1])
                    player_info[player_id] = line.text.strip()
                except (ValueError, IndexError):
                    # Skip rows with invalid player links
                    continue
        
        return player_info
    
    except requests.RequestException as e:
        print(f"Error fetching roster: {e}")
        return {}