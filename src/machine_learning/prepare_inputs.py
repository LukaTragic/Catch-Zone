import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")

def prepare_features(data):
    """
    Prepare features for XGBoost, handling categorical variables
    """
    # Define features to use for prediction
    input_features = [
        'pitch_type',  # categorical
        'release_speed',
        'release_pos_x',
        'release_pos_y',
        'release_pos_z',
        'pfx_x',
        'pfx_z',
        'api_break_z_with_gravity',
        'api_break_x_arm',
        'api_break_x_batter_in',
        'arm_angle',
        'release_extension'
    ]
    
    # Define target variables
    target_features = [
        'release_spin_rate',
        'launch_speed',
        'launch_angle',
        'spray_angle',
        'spin_axis',
        'plate_x',
        'plate_z'
    ]
    pitch_types = ['CH', 'CU', 'FC', 'EP', 'FO', 'FF', 'KN', 
               'KC', 'SC', 'SI', 'SL', 'SV', 'FS', 'ST']
    
    # Create copy of relevant features
    X = data[input_features].copy()
    y = data[target_features].copy()
    
    # Handle categorical variables
    label_encoders = {}
    categorical_features = X.select_dtypes(exclude=np.number).columns
    
    for col in categorical_features:
        if col == 'pitch_type':  # Ensure all pitch types are accounted for
            label_encoders[col] = LabelEncoder()
            label_encoders[col].fit(pitch_types)
            X[col] = label_encoders[col].transform(X[col])
        else:
            label_encoders[col] = LabelEncoder()
            X[col] = label_encoders[col].fit_transform(X[col])
    
    return X, y, label_encoders, input_features, target_features

