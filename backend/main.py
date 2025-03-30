import requests
from bs4 import BeautifulSoup

url = "https://www.transfermarkt.com.tr/super-lig/tabelle/wettbewerb/TR1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
for row in soup.select("table.items tbody tr"):
    position = row.find("td", class_="rechts").text.strip()
    team_td = row.find("td", class_="hauptlink")
    team = row.find("img")["alt"]
    points = row.find_all("td", class_="zentriert")[-1].text.strip()
    img = row.find("td", class_="no-border-rechts").find("img")["src"]
    print(f"{position}. {team} | Puan: {points} | Logo: {img}")