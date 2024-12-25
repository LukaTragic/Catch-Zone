import importlib
import pandas as pd, numpy as np


from . import trajectory_simulator
importlib.reload(trajectory_simulator)
from .trajectory_simulator import *
from typing import List, Dict

from shapely.geometry import Polygon, Point  # To handle geometric calculations



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

def simulate_home_runs(pitches: pd.DataFrame):
    """
    Simulate the trajectory of baseballs and determine proximity to HR_COORD segments

    Args:
        pitches (pd.DataFrame): DataFrame containing pitch data
    Returns:
    """

    results = []
    # Convert HR_COOR into a list of line segments
    for _, row in pitches.iterrows():
        try:
            if (row['events'] == None or np.isnan(row['release_spin_rate']) or np.isnan(row['launch_speed']) or np.isnan(row['launch_angle']) or 
            np.isnan(row['spray_angle']) or np.isnan(row['spin_axis']) or np.isnan(row['plate_x']) or np.isnan(row['plate_z'])
            ):
                continue
            trajectory = simulate_row(row)  # Simulate the trajectory
            last_time = max(trajectory.keys())
            final_position = trajectory[last_time][0]
            final_point = Point(final_position[:2])
            inside_polygon = polygon.contains(final_point)

            results.append({
                "last_time": last_time,
                "final_poistion": final_position,
                "inside_polygon": inside_polygon,
                "given_HR": row['events']
            })
        
        except Exception as e:
            print(f"Error processing row: {e}")
            print(row['release_spin_rate'])
            print(row['launch_speed'])
            print(row['launch_angle'])
            print(row['spray_angle'])
            print(row['spin_axis'])
            print(row['plate_x'])
            print(row['plate_z'])

    
    return  results