import joblib
import numpy as np
from xgboost import XGBClassifier


# --- LOAD THE SAVED MODEL AND ASSETS ---
model = XGBClassifier()
model.load_model('final_superlig_model.json')
assets = joblib.load('prediction_assets.joblib')

# Unpack the history dictionaries from the loaded assets
team_form_hist = assets['team_form_history']
h2h_hist = assets['h2h_history']
home_hist = assets['home_match_history']
away_hist = assets['away_match_history']


def prepare_match_features(home_team, away_team):
    """Calculates the features for a new match using the historical data."""
    
    # 1. Overall Form
    past_home_form = team_form_hist.get(home_team, [])
    past_away_form = team_form_hist.get(away_team, [])
    ht_form = sum(past_home_form[-5:]) / 5 if past_home_form else 0
    at_form = sum(past_away_form[-5:]) / 5 if past_away_form else 0

    # 2. Head-to-Head Form
    key_home = (home_team, away_team)
    key_away = (away_team, home_team)
    past_home_h2h = h2h_hist.get(key_home, [])
    past_away_h2h = h2h_hist.get(key_away, [])
    ht_h2h = sum(past_home_h2h[-5:]) / 5 if past_home_h2h else 0
    at_h2h = sum(past_away_h2h[-5:]) / 5 if past_away_h2h else 0

    # 3. Home/Away Specific Form
    past_home_matches = home_hist.get(home_team, [])
    past_away_matches = away_hist.get(away_team, [])
    ht_home_form = sum(past_home_matches[-5:]) / 5 if past_home_matches else 0
    at_away_form = sum(past_away_matches[-5:]) / 5 if past_away_matches else 0

    # Return the features in the correct order for the model
    return np.array([[ht_form, at_form, ht_h2h, at_h2h, ht_home_form, at_away_form]])

# --- MAKE A PREDICTION FOR AN UPCOMING MATCH ---
home = "Fenerebahce"
away = "Besiktas"

# Get the feature vector for this match
match_features = prepare_match_features(home, away)

# Predict the outcome and probabilities
prediction = model.predict(match_features)
probabilities = model.predict_proba(match_features)

# Map numeric prediction back to a meaningful label
mapping_inv = {1: "Home Win (H)", 2: "Away Win (A)", 0: "Draw (D)"}
predicted_outcome = mapping_inv[prediction[0]]

print(f"--- Prediction for {home} vs {away} ---")
print(f"Predicted Outcome: {predicted_outcome}")
print("\nProbabilities:")
print(f"  - Draw (D):     {probabilities[0][0]:.2%}")
print(f"  - Home Win (H): {probabilities[0][1]:.2%}")
print(f"  - Away Win (A): {probabilities[0][2]:.2%}")
print("---------------------------------------")