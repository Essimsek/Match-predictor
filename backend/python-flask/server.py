import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from predict import predict_match

app = Flask(__name__)

def get_standings() -> list:
    url = "https://www.transfermarkt.com.tr/super-lig/tabelle/wettbewerb/TR1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    standings = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    for row in soup.select("table.items tbody tr"):
        position = row.find("td", class_="rechts").text.strip()
        team = row.find("img")["alt"]
        points = row.find_all("td", class_="zentriert")[-1].text.strip()
        img = row.find("td", class_="no-border-rechts").find("img")["src"]
        standings.append({
            "position": position,
            "team": team,
            "points": points,
            "logo": img,
        })
    return standings

@app.route("/api-flask/standings", methods=["GET"])
def standings():
    standings = get_standings()
    return jsonify(standings)

@app.route("/api-flask/predict", methods=["GET"])
def predict_route():
    home_team = request.args.get("home")
    away_team = request.args.get("away")
    if not home_team or not away_team:
        return jsonify({"error": "Please provide home and away team names"}), 400

    prediction = predict_match(home_team, away_team)
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
