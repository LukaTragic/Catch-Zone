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

FULL_TEAM_DICT = {
    "ARI": "Arizona Diamondbacks", "ATL": "Atlanta Braves", "BAL": "Baltimore Orioles", "BOS": "Boston Red Sox", "CHC": "Chicago Cubs",
    "CHW": "Chicago White Sox", "CIN": "Cincinnati Reds", "CLE": "Cleveland Guardians", "COL": "Colorado Rockies", "DET": "Detroit Tigers",
    "MIA": "Miami Marlins", "HOU": "Houston Astros", "KAN": "Kansas City Royals", "LAA": "Los Angeles Angels", "LAD": "Los Angeles Dodgers",
    "MIL": "Milwaukee Brewers", "MIN": "Minnesota Twins", "NYM": "New York Mets", "NYY": "New York Yankees", "OAK": "Oakland Athletics",
    "PHI": "Philadelphia Phillies", "PIT": "Pittsburgh Pirates", "SDP": "San Diego Padres", "SFG": "San Francisco Giants", "SEA": "Seattle Mariners",
    "STL": "St. Louis Cardinals", "TBR": "Tampa Bay Rays", "TEX": "Texas Rangers", "TOR": "Toronto Blue Jays", "WAS": "Washington Nationals"
}

POISTION_DICT = {
    "RP": "Relief Pitcher", "P": "Pitcher", "C": "Catcher", "1B": "First Baseman",
    "2B": "Second Baseman", "3B": "Third Baseman", "SS": "Shortstop", "LF": "Left Fielder",
    "CF": "Center Fielder", "RF": "Right Fielder", "DH": "Designated Hitter", "CL": "Closer"
}

def get_roster(team_acronym: str) -> Dict[int, str]:
    """
    Retrieve MLB team roster from optional website.
    
    Args:
        team_acronym (str): Three-letter team acronym
        current (bool): If current roster should be used
    Returns:
        Dict[int, str]: Dictionary of player IDs and names
    """
    url = f"https://www.mlb.com/{TEAM_DICT[team_acronym]}/roster"    
    
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
    



'''
def get_roster_depth_chart(team_acronym: str, current: int) -> Dict[str, str]:
    """
    Retrieve MLB team roster from optional website.
    
    Args:
        team_acronym (str): Three-letter team acronym
        current (bool): If current roster should be used
    Returns:
        Dict[str, str]: Dictionary of player names and roles
    """
    # default value is 2024 Yankees        
    if current == 0:
        url = f"https://www.espn.com/mlb/team/depth/_/name/{team_acronym}/{'-'.join(FULL_TEAM_DICT[team_acronym].split())}"
    elif current == 1:
        url = "https://web.archive.org/web/20240923015011/https://www.espn.com/mlb/team/depth/_/name/nyy/new-york-yankees"
    elif current == 2:
        url = "https://web.archive.org/web/20241003070726/https://www.espn.co.uk/mlb/team/depth/_/name/lad/los-angeles-dodgers"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        player_positions = {}
        position_count = {}  # Keeps track of the order for each position

        left_table_rows = soup.select('.ResponsiveTable--fixed-left .Table__TBODY .Table__TR')
        right_table_rows = soup.select('.Table__Scroller .Table__TBODY .Table__TR')

        for index, left_row in enumerate(left_table_rows):
            # Get the position text (e.g., "P", "RP")
            position_cell = left_row.select_one('.Table__TD span')
            position = position_cell.text.strip() if position_cell else None

            if position and index < len(right_table_rows):
                # Initialize position count if not already done
                if position not in position_count:
                    position_count[position] = 0

                # Get the corresponding player cells from the right-hand table
                player_cells = right_table_rows[index].select('.Table__TD span a')

                for player_cell in player_cells:
                    player_name = player_cell.text.strip()

                    position_count[position] += 1  # Increment the count for this position
                    order = position_count[position]

                    # Add to the player_positions dictionary
                    player_positions[player_name] = f"{position}-{order}"

        return player_positions

    except requests.RequestException as e:
        print(f"Error fetching roster: {e}")
        return {}


'''