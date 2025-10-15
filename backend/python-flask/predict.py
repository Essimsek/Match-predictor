import joblib
import numpy as np
from xgboost import XGBClassifier

def normalize_team_name(name: str) -> str:
    name = name.strip().lower()

    replacements = {
        "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u"
    }
    for tr_char, en_char in replacements.items():
        name = name.replace(tr_char, en_char)
    mapping = {
        "c. rizespor": "rizespor",
        "gaziantep fk": "gaziantep",
    }
    return mapping.get(name, name)

model = XGBClassifier()
model.load_model('./pred-model/final_superlig_model.json')
assets = joblib.load('./pred-model/prediction_assets.joblib')

# Unpack the history dictionaries from the loaded assets
team_form_hist = assets['team_form_history']
h2h_hist = assets['h2h_history']
h2h_combined = assets['h2h_combined']
home_hist = assets['home_match_history']
away_hist = assets['away_match_history']

def prepare_match_features(home_team, away_team):
    """Calculates the features for a new match using the historical data."""
    print(f"Preparing features for match: {home_team} vs {away_team}", flush=True)  # Debugging line 
    # 1. Overall Form
    past_home_form = team_form_hist.get(home_team, [])
    past_away_form = team_form_hist.get(away_team, [])
    ht_form = sum(past_home_form[-10:]) / 10 if past_home_form else 0
    at_form = sum(past_away_form[-10:]) / 10 if past_away_form else 0

    # 2. Head-to-Head Form
    key_home = (home_team, away_team)
    key_away = (away_team, home_team)
    past_home_h2h = h2h_hist.get(key_home, [])
    past_away_h2h = h2h_hist.get(key_away, [])
    ht_h2h = sum(past_home_h2h[-5:]) / len(past_home_h2h[-5:]) if past_home_h2h else 0
    at_h2h = sum(past_away_h2h[-5:]) / len(past_away_h2h[-5:]) if past_away_h2h else 0

    combined_key = tuple(sorted([home_team, away_team]))
    past_combined_h2h = h2h_combined.get(combined_key, [])
    ht_h2h_combined = sum(past_combined_h2h[-5:]) / len(past_combined_h2h[-5:]) if past_combined_h2h else 0
    at_h2h_combined = sum(past_combined_h2h[-5:]) / len(past_combined_h2h[-5:]) if past_combined_h2h else 0

    # 3. Home/Away Specific Form
    past_home_matches = home_hist.get(home_team, [])
    past_away_matches = away_hist.get(away_team, [])
    ht_home_form = sum(past_home_matches[-5:]) / 5 if past_home_matches else 0
    at_away_form = sum(past_away_matches[-5:]) / 5 if past_away_matches else 0

    # Return the features in the correct order for the model
    return np.array([[ht_form, at_form, ht_h2h, at_h2h, ht_h2h_combined, at_h2h_combined, ht_home_form, at_away_form]])

def predict_match(home_team, away_team):

    print(f"before norimize: {home_team} vs {away_team}", flush=True)
    home_team = normalize_team_name(home_team)
    away_team = normalize_team_name(away_team)

    features = prepare_match_features(home_team, away_team)
    pred = model.predict(features)[0]
    probs = model.predict_proba(features)

    mapping_inv = {1: "Home Win (H)", 2: "Away Win (A)", 0: "Draw (D)"}
    predicted_outcome = mapping_inv[pred]

    prediction = {
        "home_team": home_team,
        "away_team": away_team,
        "predicted_outcome": predicted_outcome,
        "probabilities": {
            "draw": float(probs[0][0]),
            "home_win": float(probs[0][1]),
            "away_win": float(probs[0][2]),
        }
    }
    
    return prediction
