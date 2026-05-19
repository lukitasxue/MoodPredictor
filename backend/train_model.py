from model import MultVarLinearRegressionModel, train_test_split
import pandas as pd

def train_model():
    df = pd.read_csv('mood_data.csv')
    # Nonlinear transformation: water effect
    df["water_effect"] = -1 * (df["water_liters"] - 2.0) ** 2 + 1.0


    feature_cols = [
    'sleep_hours', 'stress_level',
    'nutrition_quality', 'social_minutes', 'water_effect'
    ]
    target_col = 'mood_score'

    X = df[feature_cols].values   # shape (n_samples, n_features)
    y = df[target_col].values     # shape (n_samples,)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = MultVarLinearRegressionModel()
    model.fit(X_train, y_train)

    return model, feature_cols

# Load mood dataset from mood_data.csv
# Extracts feature columns like sleep_hours, etc
# Trains the model 
# Returns both trained model and the list of feature columns

# Each time backend start, the model is trained once again with the mood dataset


