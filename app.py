from flask import Flask
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():

    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": API_KEY
    }

    today = datetime.now().strftime("%Y-%m-%d")

    try:

        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers=headers,
            params={"date": today},
            timeout=10
        )

        data = response.json()

        matches = data.get("response", [])

        html = "<h1>⚽ BETAI</h1>"

        for match in matches[:15]:

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            html += f"<p>{home} vs {away}</p>"

        return html

    except Exception as e:
        return f"Hata: {e}"

if __name__ == "__main__":
    app.run()
