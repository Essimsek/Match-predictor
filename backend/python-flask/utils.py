import requests
from bs4 import BeautifulSoup

url = "https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

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

def get_last_matches():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    last_matches = []

    for i in range(1, 6):
        selector = f"#spieltagtabs-{i} #spieltagsbox table.livescore"
        table = soup.select_one(selector)
        if table:
            rows = table.select("tr.begegnungZeile")
            if not rows:
                continue

            for row in rows:
                match_id = row.get("data-id")
                home_team = row.select_one("td.verein-heim .vereinsname a").get_text(strip=True)
                away_team = row.select_one("td.verein-gast .vereinsname a").get_text(strip=True)
                score = row.select_one("td.ergebnis span.matchresult")
                score = score.get_text(strip=True) if score else "N/A"
                home_score, away_score = score.split(":") if ":" in score else (None, None)

                if home_score > away_score:
                    result = "H"
                elif away_score > home_score:
                    result = "A"
                else:
                    result = "D"
                last_matches.append({
                    "id": match_id,
                    "home": home_team,
                    "away": away_team,
                    "home_goals": home_score,
                    "away_goals": away_score,
                    "FTR": result
                })
            break
    return last_matches

def get_next_matches() -> list:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    fixtures = []

    # get the table for the current week
    table = soup.select_one("#spieltagtabs-2 #spieltagsbox table.livescore")
    if not table:
        print("❌ Bu haftanın maç tablosu bulunamadı")
        return []

    rows = table.select("tr.begegnungZeile")
    for row in rows:
        match_id = row.get("data-id")

        home_team = row.select_one("td.verein-heim .vereinsname a").get_text(strip=True)
        away_team = row.select_one("td.verein-gast .vereinsname a").get_text(strip=True)

        result_or_time = row.select_one("td.ergebnis span.matchresult")
        if not result_or_time:
            continue

        classes = result_or_time.get("class", [])
        text = result_or_time.get_text(strip=True)

        if "finished" in classes:
            status = "finished"
            value = text  # score
        elif "live" in classes:
            status = "live"
            value = text  # minutes
        else:
            status = "upcoming"
            value = text  # hour

        def get_img_src(img_tag):
            if not img_tag:
                return None
            return img_tag.get("src") or img_tag.get("data-src")

        home_logo = get_img_src(row.select_one("td.verein-heim img"))
        away_logo = get_img_src(row.select_one("td.verein-gast img"))

        fixtures.append({
            "id": match_id,
            "home": home_team,
            "home_logo": home_logo,
            "away": away_team,
            "away_logo": away_logo,
            "status": status,
            "value": value
        })

    return fixtures


if __name__ == "__main__":
    #matches = get_next_matches()
    #print("current match week:")
    #for i in matches:
        #print(i)
    matches = get_next_matches()
    for i in matches:
        print(i)