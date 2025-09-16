import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
import numpy as np
import joblib

# replace the result with points
def result_to_points(ftr, team, home_team, away_team):
    if ftr == 'H':
        return 3 if team == home_team else 0
    elif ftr == 'A':
        return 3 if team == away_team else 0
    else: # Draw
        return 1

# Read the data
data = pd.read_csv('./superlig_data.csv')

# Calculate points (just putting points to the rows based on FTR, A, H, D)
data["HomePoints"] = data.apply(lambda row: result_to_points(row.FTR, row.HomeTeam, row.HomeTeam, row.AwayTeam), axis=1)
data["AwayPoints"] = data.apply(lambda row: result_to_points(row.FTR, row.AwayTeam, row.HomeTeam, row.AwayTeam), axis=1)

# string to datetime
data["Date"] = pd.to_datetime(data["Date"], dayfirst=True)

# we need to sort the date to get the last 5 matches (h2h, home-form, away-form) correctly
data = data.sort_values("Date").reset_index(drop=True) # sort by date just in case if it's not sorted
mapping = {"H": 1, "A": 2, "D": 0}
data["FTR_numerical"] = data["FTR"].map(mapping) # map the ftr to numerical values so model can understand

# --- FEATURE ENGINEERING ---
#  We need meaningful features from raw data
# 1. Last 5 matches, form points. Teams form in last 5 matches (average points in last 5 matches actually)
# 2. Last 5 head to head matches points this is the most important feature we need to provide that to the model 
#    how teams performed against each other ?
# 3. and the last one is how they perform in home and away matches separately (last 5 home matches for home team, last 5 away matches for away team)

team_form, h2h_history, h2h_combined = {}, {}, {}
HT_form_points, AT_form_points, HT_h2h_points_5, AT_h2h_points_5 = [], [], [], []
HT_h2h_combined_5, AT_h2h_combined_5 = [], []

# Overall team form last 5
for index, row in data.iterrows():
    home_team, away_team = row["HomeTeam"], row["AwayTeam"] # we get the teams
    
    # get the past form points
    past_home_form = team_form.get(home_team, [])
    past_away_form = team_form.get(away_team, [])

    # calculate average points in last 5 matches (3 + 1 + 0 + 3 + 3 = 10 / 5 = 2.0)
    HT_form_points.append(sum(past_home_form[-10:]) / 10 if past_home_form else 0)
    AT_form_points.append(sum(past_away_form[-10:]) / 10 if past_away_form else 0)

    # get the past h2h points
    key_home, key_away = (home_team, away_team), (away_team, home_team)
    past_home_h2h = h2h_history.get(key_home, [])
    past_away_h2h = h2h_history.get(key_away, [])
    HT_h2h_points_5.append(sum(past_home_h2h[-5:]) / len(past_home_h2h[-5:]) if past_home_h2h else 0)
    AT_h2h_points_5.append(sum(past_away_h2h[-5:]) / len(past_away_h2h[-5:]) if past_away_h2h else 0)

    combined_key = tuple(sorted([home_team, away_team]))
    past_combined_h2h = h2h_combined.get(combined_key, [])
    HT_h2h_combined_5.append(sum(past_combined_h2h[-5:]) / len(past_combined_h2h[-5:]) if past_combined_h2h else 0)
    AT_h2h_combined_5.append(sum(past_combined_h2h[-5:]) / len(past_combined_h2h[-5:]) if past_combined_h2h else 0)

    # we are adding this current matches points to the history for future matches
    team_form.setdefault(home_team, []).append(row["HomePoints"])
    team_form.setdefault(away_team, []).append(row["AwayPoints"])
    h2h_history.setdefault(key_home, []).append(row["HomePoints"])
    h2h_history.setdefault(key_away, []).append(row["AwayPoints"])
    h2h_combined.setdefault(combined_key, []).append(row["HomePoints"])
    h2h_combined.setdefault(combined_key, []).append(row["AwayPoints"])

# add new features..
data["HT_form_points_5"], data["AT_form_points_5"] = HT_form_points, AT_form_points
data["HT_h2h_points_5"], data["AT_h2h_points_5"] = HT_h2h_points_5, AT_h2h_points_5
data["HT_h2h_combined_5"], data["AT_h2h_combined_5"] = HT_h2h_combined_5, AT_h2h_combined_5

# Home and Away specific form (last 5 home matches for home team, last 5 away matches for away team)
home_history, away_history = {}, {}
HT_home_form_5, AT_away_form_5 = [], []

for index, row in data.iterrows():
    home_team, away_team = row["HomeTeam"], row["AwayTeam"] # get the teams

    # past home and away matches
    past_home_matches = home_history.get(home_team, []) 
    past_away_matches = away_history.get(away_team, [])

    # calculate average points in last 5 home/away matches
    HT_home_form_5.append(sum(past_home_matches[-5:]) / 5 if past_home_matches else 0)
    AT_away_form_5.append(sum(past_away_matches[-5:]) / 5 if past_away_matches else 0)

    # add current match points to history
    home_history.setdefault(home_team, []).append(row["HomePoints"])
    away_history.setdefault(away_team, []).append(row["AwayPoints"])

# new features..
data["HT_home_form_5"] = HT_home_form_5
data["AT_away_form_5"] = AT_away_form_5


# okay now we have all the features we need
# so we can prepare the data for the model
features = [
    "HT_form_points_5", "AT_form_points_5",
    "HT_h2h_points_5", "AT_h2h_points_5",
    "HT_h2h_combined_5", "AT_h2h_combined_5",
    "HT_home_form_5", "AT_away_form_5"
]
X = data[features]
y = data["FTR_numerical"]

# --- split the data into train and test sets --- 
split_percentage = 0.8
split_index = int(len(data) * split_percentage)
X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]


# ------------------- NEW STEP: HYPERPARAMETER TUNING -------------------
print("\n--- Finding Best Model Parameters using GridSearchCV ---")

# 1. Define the parameter grid to search
# I tried couple of values and these seems to be good enough
param_grid = {
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1, 0.02],
    'n_estimators': [100, 150, 200, 250],
    'subsample': [0.5, 0.6, 0.7, 0.8]
}
# {'learning_rate': 0.01, 'max_depth': 5, 'n_estimators': 100, 'subsample': 0.8} # this is the best grid found

# 2. Set up the time series cross-validator
# This ensures that we validate on "future" data relative to the training data in each fold
tscv = TimeSeriesSplit(n_splits=5)

# 3. Create the GridSearchCV object
# 4 x 4 x 4 x 4 = 256 combinations to try
xgb_estimator = XGBClassifier(eval_metric="mlogloss", random_state=42)
grid_search = GridSearchCV(
    estimator=xgb_estimator,
    param_grid=param_grid,
    scoring='accuracy',
    cv=tscv, # Use our time-series splitter
    verbose=1, # its for the processing output
    n_jobs=-1 # to be faster we give -1 (use all processors)
)

# 4. Run the search on the training data
grid_search.fit(X_train, y_train)

# 5. Get the best model and its parameters
print("\nBest Parameters Found:", grid_search.best_params_)
print(f"Best Accuracy during search: {grid_search.best_score_:.2f}")
best_model = grid_search.best_estimator_
# --------------------------------------------------------------------------


# --- EVALUATE THE BEST MODEL ON THE TEST DATA ---
print("\n--- Model Evaluation on Unseen Data (using the best model) ---")
y_pred_on_test = best_model.predict(X_test)
y_pred_prob_on_test = best_model.predict_proba(X_test)
accuracy = accuracy_score(y_test, y_pred_on_test)
report = classification_report(y_test, y_pred_on_test, target_names=["Draw", "Home Win", "Away Win"], zero_division=0)

print(f"Real Accuracy on the Test Set: {accuracy:.2f}")
print("Predicted Class Probabilities (first 5 rows):\n", y_pred_prob_on_test[:5])
print("Classification Report:\n", report)

# okay now we can train the final model on the entire dataset using the best parameters found
print("\n--- Training Final Model on Entire Dataset ---")
final_model = XGBClassifier(**grid_search.best_params_, eval_metric="mlogloss", random_state=42)
final_model.fit(X, y)

# --- SAVE THE FINAL MODEL AND NECESSARY ASSETS ---
# 1. Save the final trained model to a file
model_filename = 'final_superlig_model.json'
final_model.save_model(model_filename)
print(f"\nFinal model saved to {model_filename}")

# 2. Bundle all history dictionaries into a single object for convenience
prediction_assets = {
    'team_form_history': team_form,
    'h2h_history': h2h_history,
    'h2h_combined': h2h_combined,
    'home_match_history': home_history,
    'away_match_history': away_history
}

# 3. Save the assets object to a file
assets_filename = 'prediction_assets.joblib'
joblib.dump(prediction_assets, assets_filename)
print(f"Prediction assets saved to {assets_filename}")



# convert time to a format that can be used which is decimal hour here.
#data["HourDecimal"] = data["Time"].str.split(":", expand=True)[0].astype(int) + \
                      #data["Time"].str.split(":", expand=True)[1].astype(int) / 60

# drop time and date
#data.drop(columns=["Time", "Date"], inplace=True)

# map the FTR to numerical values
#mapping = {"H": 1, "A": -1, "D": 0}
#data["FTRC"] = data["FTR"].map(mapping)

# features and target
#features = ["HourDecimal", "HTC", "ATC"]
#X = data[features]
#y = data["FTRC"]

# get the train and val sets
#X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=.9, stratify=y, random_state=42)

# create and fit the data to the model
#model = XGBClassifier()
#model.fit(X, y) # fit with all the data

# accuracy
#print("Accuracy:", accuracy_score(y_valid, y_pred))
#print(classification_report(y_valid, y_pred))

# load and clear the data
#data = pd.read_csv('./superlig_2023_2025.csv')
## only get Date, time, HomeTeam AwayTeam and FTR
#data["HTC"] = pd.Categorical(data["HomeTeam"]).codes
#data["ATC"] = pd.Categorical(data["AwayTeam"]).codes
#data["FTRC"] = pd.Categorical(data["FTR"]).codes
#features = ["Date", "Time", "HomeTeam", "HTC", "AwayTeam", "ATC", "FTR", "FTRC"]

# Trabzonspor_matches = data[(data["HomeTeam"] == "Trabzonspor") | (data["AwayTeam"] == "Trabzonspor")] # get all the matches of Trabzonspor

# Print each row as a tuple
#for i in Trabzonspor_matches[features].itertuples():
    #print(i)

# get all the necessary features
#data = data[features]

# drop rows with missing values
#data = data.dropna()
# drop duplicates
#data = data.drop_duplicates()

# get the length of the data
# print(f"Length of the data: {len(data)}")

# create new csv file with the necessary features
#data.to_csv('./superlig_2023_2025_cleaned.csv', index=False)5