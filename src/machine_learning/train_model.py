import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings("ignore")

def train_xgboost_model(X, y):
    """
    Train separate XGBoost models for each target variable
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize models dictionary
    models = {}
    scores = {}
    
    # Base parameters
    params = {
        "objective": "reg:squarederror",
        "tree_method": "gpu_hist",  # Use "hist" if GPU not available
        "max_depth": 6,
        "learning_rate": 0.1,
        "n_estimators": 5000,
        "early_stopping_rounds": 50
    }
    
    # Train a model for each target variable
    for column in y.columns:
        print(f"\nTraining model for {column}")
        
        # Create DMatrix for current target
        dtrain = xgb.DMatrix(X_train, y_train[column])
        dtest = xgb.DMatrix(X_test, y_test[column])
        
        # Train model
        model = xgb.train(
            params,
            dtrain,
            num_boost_round=params["n_estimators"],
            evals=[(dtrain, "train"), (dtest, "eval")],
            early_stopping_rounds=params["early_stopping_rounds"],
            verbose_eval=100
        )
        
        # Store model
        models[column] = model
        
        # Calculate and store score
        predictions = model.predict(dtest)
        rmse = np.sqrt(mean_squared_error(y_test[column], predictions))
        scores[column] = rmse
        print(f"RMSE for {column}: {rmse:.3f}")
    
    return models, scores
