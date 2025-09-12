from flask import Flask, jsonify, request
from predict import predict_match
from utils import get_standings, get_next_fixtures

app = Flask(__name__)
@app.route("/api-flask/standings", methods=["GET"])
def standings():
    standings = get_standings()
    return jsonify(standings)

@app.route("/api-flask/fixtures", methods=["GET"])
def fixtures():
    fixtures = get_next_fixtures()
    return jsonify(fixtures)

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
