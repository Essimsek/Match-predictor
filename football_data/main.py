import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Read the data
data = pd.read_csv('./superlig_2023_2025_cleaned.csv')

# convert time to a format that can be used which is decimal hour here.
data["HourDecimal"] = data["Time"].str.split(":", expand=True)[0].astype(int) + \
                      data["Time"].str.split(":", expand=True)[1].astype(int) / 60

# drop time and date
data.drop(columns=["Time", "Date"], inplace=True)

# features and target
features = ["HourDecimal", "HTC", "ATC"]
X = data[features]
y = data["FTRC"]

# get the train and val sets
#X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=.9, stratify=y, random_state=42)

# create and fit the data to the model
model = XGBClassifier()
model.fit(X, y) # fit with all the data
#model.fit(X_train, y_train) this was for testing

# 3️⃣ Takım dictionary
team_dict = {
 'Trabzonspor': 24, 'Kasimpasa': 16, 'Konyaspor': 19, 'Kayserispor': 17,
 'Pendikspor': 20, 'Sivasspor': 23, 'Ad. Demirspor': 0, 'Fenerbahce': 8,
 'Alanyaspor': 1, 'Karagumruk': 15, 'Antalyaspor': 3, 'Istanbulspor': 14,
 'Rizespor': 21, 'Galatasaray': 9, 'Hatayspor': 13, 'Buyuksehyr': 6,
 'Besiktas': 4, 'Gaziantep': 10, 'Ankaragucu': 2, 'Samsunspor': 22,
 'Bodrumspor': 5, 'Goztep': 12, 'Eyupspor': 7, 'Kocaelispor': 18,
 'Genclerbirligi': 11
}

# ----------------------
# 4️⃣ Fonksiyon: son 5 maç stats
def last5_stats(team_last5, team_name):
    wins = 0
    draws = 0
    losses = 0

    # Eğer gol kolonu yoksa sadece sonucu kullan
    for _, match in team_last5.iterrows():
        if match['HomeTeam'] == team_name:
            result = match['FTR']
            if result == 'H': wins +=1
            elif result == 'D': draws +=1
            else: losses +=1
        else:
            result = match['FTR']
            if result == 'A': wins +=1
            elif result == 'D': draws +=1
            else: losses +=1
    return wins, draws, losses

# ----------------------
# 5️⃣ Tahmin yapmak istediğimiz maç
home = "Fenerbahce"
away = "Galatasaray"
hour = 19.0

# Son 5 maçları al
gal_last5 = data[(data['HomeTeam']==home) | (data['AwayTeam']==home)].tail(5)
fen_last5 = data[(data['HomeTeam']==away) | (data['AwayTeam']==away)].tail(5)

gal_w, gal_d, gal_l = last5_stats(gal_last5, home)
fen_w, fen_d, fen_l = last5_stats(fen_last5, away)
print(f"{home} last 5 - Wins: {gal_w}, Draws: {gal_d}, Losses: {gal_l}")
print(f"{away} last 5 - Wins: {fen_w}, Draws: {fen_d}, Losses: {fen_l}")
# ----------------------
# 6️⃣ Yeni prediction row
X_new = pd.DataFrame([{
    "HourDecimal": hour,
    "HTC": team_dict[home],
    "ATC": team_dict[away],
    "HT_last5_wins": gal_w,
    "HT_last5_draws": gal_d,
    "HT_last5_losses": gal_l,
    "AT_last5_wins": fen_w,
    "AT_last5_draws": fen_d,
    "AT_last5_losses": fen_l
}])

# ----------------------
# 7️⃣ Tahmin
# Not: Modeli başta sadece HTC, ATC, HourDecimal ile eğittik
# Ekstra son5 feature’ları kullanmak için tekrar fit etmelisin
# Şimdilik sadece temel tahmin:
y_proba = model.predict_proba(X_new[["HourDecimal","HTC","ATC"]])[0]

print(f"{home} Win: {y_proba[2]*100:.1f}%")
print(f"Draw: {y_proba[1]*100:.1f}%")
print(f"{away} Win: {y_proba[0]*100:.1f}%")

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
