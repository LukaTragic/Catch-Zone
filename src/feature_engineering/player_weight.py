import pandas as pd
from typing import Dict

def calculate_appearance_weights(team_roster: Dict, pitches: pd.DataFrame, game_date: str):
    """
    Given a date, calculate the percentage of pitches each player on the roster was present at.
    
    Args:
        team_roster (Dict): team roster
        pitches (pd.DataFrame): database of all pitches of team
        game_date (str): current game examining
    Returns:
        pitch_weights (Dict): percentage of pitches each player appears in
    """

    recent_pitches = pitches[pd.to_datetime(pitches['game_date']) < pd.Timestamp(game_date)]
    
    pitch_weights = {}
    total_pitches = recent_pitches.shape[0]


    # Group by pitcher
    for pitcher_id, pitcher_name in team_roster.items():
        # Filter data for the specific pitcher
        pitcher_data = recent_pitches[recent_pitches['pitcher'] == pitcher_id]
        pitcher_pitches = pitcher_data.shape[0]


        if total_pitches > 0:  # To avoid division by zero
            pitch_probability  = pitcher_pitches / total_pitches
        else:
            pitch_probability = 0
        pitch_weights[pitcher_name] = pitch_probability

    return pitch_weights


def calculate_total_weights(team_roster: Dict, roster_positions: Dict, pitches: pd.DataFrame, game_date: str):    
    """
    Calculate weights based on position and appearence
    Args:
        team_roster (Dict): team roster
        roster_positions (Dict): positions of each player
        pitches (pd.DataFrame): database of all pitches of team
        game_date (str): current game examining
    Returns:
        combined_weights (Dict): adjusted probabilities of each player appearing in a game
    """


    combined_weights = {}
    total_weight = 0

    season_weights = calculate_appearance_weights(team_roster, pitches, game_date)

    role_weights = {'P': 0.6, 'RP': 0.2, 'CL': 0.2}
    
    for pitcher_id, pitcher_name in team_roster.items(): 
        if pitcher_name not in (roster_positions.keys()):
            continue
        position = roster_positions[pitcher_name]
        [role, priority] = position.split("-")
        priority = int(priority)
        
        weight = season_weights[pitcher_name] 

        if role == 'P':
            weight *= role_weights['P']
            if priority <= 3:
                weight *= (1.2 - (priority * 0.05))
            else:
                weight *= (0.95 - ((priority-3) * 0.1))
        elif role == 'RP':
            weight *= role_weights['RP']
            if priority <= 3:
                weight *= (1.1 - ((priority-1) * 0.05))
            else:
                weight *= (0.9 - ((priority-3) * 0.05))
        elif role == 'CL':
            weight *= role_weights['CL']
            if priority == 1:
                weight *= 1.3
            else:
                weight *= (0.9 - ((priority-1) * 0.15))
        combined_weights[pitcher_name] = max(weight, 0.01)
        total_weight += combined_weights[pitcher_name]

    for pitcher in combined_weights:
        combined_weights[pitcher] /= total_weight

    return combined_weights

