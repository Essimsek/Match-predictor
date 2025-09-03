import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
from utils import result_to_points
from sklearn.model_selection import train_test_split
import numpy as np

def get_h2h_points(home, away, home_points, away_points):
    # Home -> Away
    key_home = (home, away)
    key_away = (away, home)

    past_home = h2h_history.get(key_home, [])
    past_away = h2h_history.get(key_away, [])

    # avg of last 5 --- normilize by 5
    home_h2h = sum(past_home[-5:]) / 5 if past_home else 0
    away_h2h = sum(past_away[-5:]) / 5 if past_away else 0

    # add to the history
    h2h_history.setdefault(key_home, []).append(home_points)
    h2h_history.setdefault(key_away, []).append(away_points)

    return home_h2h, away_h2h

# Read the data
data = pd.read_csv('./superlig_data.csv')

# if win home -> HomeTeam gets 3 points, AwayTeam gets 0 points etc etc 
data["HomePoints"] = data.apply(lambda row: result_to_points(row.FTR, row.HomeTeam, row.HomeTeam, row.AwayTeam), axis=1)
data["AwayPoints"] = data.apply(lambda row: result_to_points(row.FTR, row.AwayTeam, row.HomeTeam, row.AwayTeam), axis=1)

# lets sort the data by date
data["Date"] = pd.to_datetime(data["Date"], dayfirst=True)
data = data.sort_values("Date")

# convert FTR to numerical values
mapping = {"H": 1, "A": 2, "D": 0}
data["FTR_numerical"] = data["FTR"].map(mapping)

team_form = {}

HT_form_points = []
AT_form_points = []

for _, row in data.iterrows():
    home, away, date = row["HomeTeam"], row["AwayTeam"], row["Date"]
    
    # home form
    past_home = team_form.get(home, [])
    HT_form_points.append(sum(past_home[-5:]) / 5 if past_home else 0)
    
    # away form
    past_away = team_form.get(away, [])
    AT_form_points.append(sum(past_away[-5:]) / 5 if past_away else 0)
    
    # update history
    team_form.setdefault(home, []).append(row["HomePoints"])
    team_form.setdefault(away, []).append(row["AwayPoints"])

data["HT_form_points_5"] = HT_form_points
data["AT_form_points_5"] = AT_form_points


# head to head
h2h_history = {}
HT_h2h_points_5 = []
AT_h2h_points_5 = []


for _, row in data.iterrows():
    home = row["HomeTeam"]
    away = row["AwayTeam"]
    home_points = row["HomePoints"]
    away_points = row["AwayPoints"]

    home_h2h, away_h2h = get_h2h_points(home, away, home_points, away_points)

    HT_h2h_points_5.append(home_h2h)
    AT_h2h_points_5.append(away_h2h)

data["HT_h2h_points_5"] = HT_h2h_points_5
data["AT_h2h_points_5"] = AT_h2h_points_5


# features and target
features = ["HT_form_points_5", "AT_form_points_5", "HT_h2h_points_5", "AT_h2h_points_5"]
X = data[features]
y = data["FTR_numerical"]


# get the train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42, stratify=y
)

# fit the model
model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.02,
    subsample=0.6,
    colsample_bytree=0.6,
    eval_metric="mlogloss",
    random_state=42
)
model.fit(X, y)

# last 5 head to head
def prepare_match_features(home, away, team_form, h2h_history):
    past_home = team_form.get(home, [])
    past_away = team_form.get(away, [])
    HT_form_points = sum(past_home[-5:]) / 5 if past_home else 0
    AT_form_points = sum(past_away[-5:]) / 5 if past_away else 0

    # head to head
    key_home = (home, away)
    key_away = (away, home)
    past_home_h2h = h2h_history.get(key_home, [])
    past_away_h2h = h2h_history.get(key_away, [])
    HT_h2h_points_5 = sum(past_home_h2h[-5:]) / 5 if past_home_h2h else 0
    AT_h2h_points_5 = sum(past_away_h2h[-5:]) / 5 if past_away_h2h else 0

    return np.array([[HT_form_points, AT_form_points, HT_h2h_points_5, AT_h2h_points_5]])

# example: pretty good actually 42% pred accuray
home_team = "Galatasaray"
away_team = "Besiktas"

X_new = prepare_match_features(home_team, away_team, team_form, h2h_history)

y_pred = model.predict(X_new)
y_prob = model.predict_proba(X_new)

mapping_inv = {1: "Home Win", 2: "Away Win", 0: "Draw"}

print(f"{home_team} vs {away_team}")
print("Prediction:", mapping_inv[int(y_pred[0])])
print("Probs (Draw, Home Win, Away Win):", y_prob[0])


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
#data.to_csv('./superlig_2023_2025_cleaned.csv', index=False)
