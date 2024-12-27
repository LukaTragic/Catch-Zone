import sys, os, importlib, IPython
sys.path.append(os.path.abspath('..'))

import matplotlib.pyplot as plt

import src
importlib.reload(src)
from src import *

def run_the_program(input_params):

    [HT_roster, HT_hits, HT_HR_hits] = fetch_store_team_data(input_params['HITS_TEAM_CODE'], input_params['HITS_WEBSCRAPE_ID'], input_params['DB_NAME'], 'hits')
    [PT_roster, PT_pitches, PT_HR_pitches] = fetch_store_team_data(input_params['PITCH_TEAM_CODE'], input_params['PITCH_WEBSCRAPE_ID'], input_params['DB_NAME'], 'pitches')

    HT_simulated_hits = simulate_home_runs(HT_hits)
    HT_simulated_HR = HT_simulated_hits[HT_simulated_hits['simulated_home_run'] == True]
    PT_simulated_pitches = simulate_home_runs(PT_pitches)
    PT_simulated_HR = PT_simulated_pitches[PT_simulated_pitches['simulated_home_run'] == True]
    PT_pitch_distribution = fetch_pitch_distribution(input_params['PITCH_TEAM_CODE'], PT_roster, input_params['PITCH_WEBSCRAPE_ID'], PT_pitches, PT_simulated_HR, input_params['GAME_DATE'])

    IPython.display.clear_output()

    X, y, label_encoders, input_features, target_features = prepare_features(HT_simulated_HR)
    models, scores = train_xgboost_model(X, y)

    IPython.display.clear_output()


    predictions = predict_parameters(models, PT_simulated_HR, label_encoders, input_features)
    
    return [predictions, scores]


def get_locations(predictions):
    positions = []

    for _, row in predictions.iterrows():
        trajectory = simulate_row(row)  # Simulate the trajectory
                
        # Get final position
        last_time = max(trajectory.keys())
        final_position = trajectory[last_time][0]
        positions.append(final_position)

    return positions

def plot_locations(positions):

    # Extract the x and y coordinates
    x_coords = [pos[0] for pos in positions]
    y_coords = [pos[1] for pos in positions]

    # Plotting the x and y coordinates
    plt.scatter(x_coords, y_coords)
    plt.title("Scatter plot of the first two values from positions")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()
    
