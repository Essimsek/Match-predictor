import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

def result_to_points(result, team, home, away) -> int:
    if result == "H":
        return 3 if team == home else 0
    elif result == "A":
        return 3 if team == away else 0
    else:
        return 1


# Read the data
data = pd.read_csv('./superlig_data.csv')

data["HomePoints"] = data.apply(lambda row: result_to_points(row.FTR, row.HomeTeam, row.HomeTeam, row.AwayTeam), axis=1)
data["AwayPoints"] = data.apply(lambda row: result_to_points(row.FTR, row.AwayTeam, row.HomeTeam, row.AwayTeam), axis=1)

# lets sort the data by date
data["Date"] = pd.to_datetime(data["Date"], dayfirst=True)
data = data.sort_values("Date")

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
print(HT_form_points)

print(AT_form_points)

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
