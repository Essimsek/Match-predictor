# Süper Lig Match Predictor

Machine learning–based match predictions for the Turkish Süper Lig. 
A React frontend shows fixtures & standings, a Node/Express API proxies requests, and a Python/Flask ML service generates predictions. The full stack is runnable in development with Docker Compose.
---

## What it does

- Shows standings (scraped from Transfermarkt) and upcoming fixtures in the frontend.  
- For each fixture you can request predicted probabilities: **Home / Draw / Away**.  
- Frontend → Node/Express → Flask(ML & scraping). Flask loads a saved XGBoost model and small history assets to compute features on-the-fly.

---

## Tech stack (brief)

- Frontend: React + Vite + Tailwind (UI & pages for standings/fixtures).  
- API: Node.js + Express — proxies requests to Flask.  
- ML service: Python + Flask — feature engineering, prediction endpoints, scraping with BeautifulSoup.  
- Orchestration: Docker Compose for consistent cross-OS dev.
---

## ✅ Done

**Features**
- Standings scraping endpoint (Transfermarkt) in Flask.  
- Fixtures endpoint and prediction endpoint in Flask.  
- Node/Express proxy endpoints that the React frontend calls (`/api/standings`, `/api/fixtures`, `/api/predict`).  
- Docker Compose setup so frontend, backend and Flask run together in dev.

**ML & data**
- Training pipeline that:
  - Builds features from historical matches and computes target label (FTR).  
  - Uses rolling form features (average points) and head-to-head features.  
  - Hyperparameter tuning with `GridSearchCV` + `TimeSeriesSplit`.  
  - Trains a final XGBoost model and saves:
    - `final_superlig_model.json` (model)
    - `prediction_assets.joblib` (histories used for feature creation)
- Prediction pipeline that:
  - Loads model + assets.
  - Prepares features for an arbitrary `home` / `away` pair.
  - Returns a JSON response with predicted class and probabilities.
---

## 🛠️ In progress / Next steps (short & actionable)

- **Automated weekly retraining workflow**
  - Current: model trained offline on full CSV and saved assets.
  - Goal: after each matchweek, automatically:
    1. Collect the previous week’s match results (scraped or from an API).
    2. Append the new matches to the master dataset (`superlig_data.csv`) while avoiding duplicates (`Date + HomeTeam + AwayTeam` as unique key).
    3. Recompute all features (team form, home/away form, H2H, combined H2H).
    4. Retrain the XGBoost model using the same hyperparameter search and cross-validation pipeline.
    5. Save updated model (`final_superlig_model.json`) and feature histories (`prediction_assets.joblib`) for inference.
  - This ensures the model stays up-to-date without needing to retrain on every prediction request.

- **Data integrity**
  - Ensure new matches are normalized (dates, team names) before appending.
  - maybe consider using Database.

- **Model robustness & ops**
  - Implement a safe model-reload strategy in Flask so new models can be loaded without downtime..


## How the model predicts (concise, practical)

When training and when predicting the same feature engineering steps run:

1. **Team form** — average points in recent matches:
   - `HT_form`: last **10** matches average points for home team (3/1/0 scoring).
   - `AT_form`: last **10** matches average points for away team.

2. **Home/Away specific form**:
   - Home team: average points in last **5 home** matches (`HT_home_form_5`).
   - Away team: average points in last **5 away** matches (`AT_away_form_5`).

3. **Head-to-head (H2H)**:
   - Directional H2H (team-specific): last 5 mutual matches **from home team perspective** and **from away team perspective** (captures if a team specifically struggles vs that opponent when hosting/visiting).
   - **Combined H2H**: ignores home/away — pools all past encounters between the two teams using a stable key (`combined_key = tuple(sorted([home_team, away_team]))`). This captures matchup-level dynamics (rivalry balance) and is included for both home/away slots.

4. **Model & training**:
   - XGBoost classifier tuned with grid search and time-series cross-validation.
   - Final model saved to `final_superlig_model.json`.
   - Feature histories saved to `prediction_assets.joblib` for fast inference without recomputing long histories.

---

## Quick run (dev)

1. Start Docker (make sure Docker is running).  
2. From repo root:
```bash
docker compose up --build
