import requests
from bs4 import BeautifulSoup

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

def get_next_fixtures() -> list:
    url = "https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    fixtures = []

    for row in soup.select("tr.begegnungZeile"):
        # Date
        date_tag = row.select_one("td.zeit span.spielzeitpunkt a")
        date = date_tag.get_text(strip=True) if date_tag else ""

        # Kickoff time
        kickoff_tag = row.select_one("td.ergebnis span.matchresult")
        kickoff = kickoff_tag.get_text(strip=True) if kickoff_tag else ""

        # Home team
        home_tag = row.select_one("td.verein-heim a[title]")
        home = home_tag.get_text(strip=True) if home_tag else ""
        home_logo_tag = row.select_one("td.verein-heim img")
        home_logo = home_logo_tag["src"] if home_logo_tag else ""

        # Away team
        away_tag = row.select_one("td.verein-gast a[title]")
        away = away_tag.get_text(strip=True) if away_tag else ""
        away_logo_tag = row.select_one("td.verein-gast img")
        away_logo = away_logo_tag["src"] if away_logo_tag else ""

        fixtures.append({
            "date": date,
            "home": home,
            "home_logo": home_logo,
            "away": away,
            "away_logo": away_logo,
            "kickoff": kickoff
        })

    return fixtures



print(get_next_fixtures())