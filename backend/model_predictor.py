from train_model import train_model
import numpy as np

model, feature_cols = train_model()

def predict_mood(input_dict):
    """
    Predict mood score based on input data.

    Parameters:
    - input_dict: A dictionary containing the feature values.

    Returns:
    - mood_score: The predicted mood score.
    """
    # Calculate water_effect nonlinearly from water_liters
    water_liters = input_dict.get("water_liters", 0)
    water_effect = -1 * (water_liters - 2.0) ** 2 + 1.0
    input_dict["water_effect"] = water_effect  # inject into feature set

    # Prepare input using only model feature columns (now includes water_effect)
    x = np.array([[input_dict[col] for col in feature_cols]])
    return float(model.predict(x)[0])


# Bridge between frontend and the model
# Gets the input values as a py dict (from the API)
# Canverts it to the format the model expects (numpy array)
# Calls the model predict and returns the result 