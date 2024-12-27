import sys, os, importlib
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point

sys.path.append(os.path.abspath('..'))

import src
importlib.reload(src)
from src import *

HR_COOR = { 
    "V1": [-68.7511, 69.0903], "V2": [-68.7623, 71.1585], "V3": [-67.8291, 76.8619],  "V4": [-66.0082, 82.3547], "V5": [-63.3568, 87.5822],   
    "V6": [-41.2138, 109.356], "V7": [-37.1212, 113.44], "V8": [-25.6933, 120.451], "V9": [-17.3502, 123.117], "V10": [-8.66782, 124.526],  
    "V11": [0.124953, 124.523],  "V12": [8.25197, 123.229], "V13": [16.7201, 120.478],  "V14": [28.0759, 112.219], "V15": [63.8569, 76.3393], 
    "V16": [65.9228, 73.3136], "V17": [67.2493, 69.6967], "V18": [67.6961, 68.5969] 
}

polygon_vertices = [
    (-200, 200),
    (200, 200),
] + list(HR_COOR.values())

polygon = Polygon(polygon_vertices)

def simulate_home_runs(events: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate the trajectory of baseballs and determine proximity to HR_COORD segments

    Args:
        pitches (pd.DataFrame): DataFrame containing pitch data
    Returns:
        pd.DataFrame: Original DataFrame with added simulated_home_run column
    """
    # Create a copy of the DataFrame to avoid modifying the original
    events = events.copy()
    
    # Initialize the simulated_home_run column with False
    events['simulated_home_run'] = False
    
    # Create a mask for valid rows
    valid_rows = (
        events['events'].notna() &
        events['release_spin_rate'].notna() &
        events['launch_speed'].notna() &
        events['launch_angle'].notna() &
        events['spray_angle'].notna() &
        events['spin_axis'].notna() &
        events['plate_x'].notna() &
        events['plate_z'].notna()
    )
    
    # Process only valid rows
    for idx in events[valid_rows].index:
        try:
            row = events.loc[idx]
            trajectory = simulate_row(row)  # Simulate the trajectory
            
            # Get final position
            last_time = max(trajectory.keys())
            final_position = trajectory[last_time][0]
            final_point = Point(final_position[:2])
            
            # Check if point is inside polygon
            if polygon.contains(final_point):
                events.loc[idx, 'simulated_home_run'] = True
                
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            print(f"Values: release_spin_rate={row['release_spin_rate']}, "
                  f"launch_speed={row['launch_speed']}, "
                  f"launch_angle={row['launch_angle']}, "
                  f"spray_angle={row['spray_angle']}, "
                  f"spin_axis={row['spin_axis']}, "
                  f"plate_x={row['plate_x']}, "
                  f"plate_z={row['plate_z']}")
    
    return events