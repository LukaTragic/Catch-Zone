import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")


def predict_parameters(models, new_data, label_encoders, input_features):
    """
    Make predictions for new data and include a pitch-type-specific index for matching.
    
    Parameters:
    - models: Dictionary of trained XGBoost models, one for each target variable.
    - new_data: DataFrame containing new data for prediction.
    - label_encoders: Dictionary of label encoders for categorical variables.
    - input_features: List of input features to use for predictions.
    - pitch_type_col: Column name indicating the pitch type in new_data.
    
    Returns:
    - predictions_df: DataFrame with predictions and pitch-type-specific indices.
    """
    # Prepare new data
    pitch_type_col = "pitch_type"

    X_pred = new_data[input_features].copy()
    
    # Apply label encoding to categorical variables
    for col, encoder in label_encoders.items():
        if col in X_pred.columns:
            X_pred[col] = encoder.transform(X_pred[col])
    
    # Convert to DMatrix
    dpred = xgb.DMatrix(X_pred)
    
    # Make predictions for each target variable
    predictions = {}
    for target, model in models.items():
        predictions[target] = model.predict(dpred)
    
    # Convert predictions to DataFrame
    predictions_df = pd.DataFrame(predictions)
    
    # Add pitch type and pitch-type-specific index
    predictions_df[pitch_type_col] = new_data[pitch_type_col].values
    predictions_df["pitch_index"] = predictions_df.groupby(pitch_type_col).cumcount()
    
    return predictions_df
