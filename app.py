from flask import Flask
import requests
import os
import random

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route("/")
def home():

    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": API_KEY
    }

    try:
        response = requests.get(
            "https://v3.football.api-sports.io/fixtures",
            headers=headers,
            params={"live": "all"},
            timeout=10
        )

        data = response.json()
        matches = data.get("response", [])

        html = "<h1>🔴 CANLI MAÇLAR - BETAI</h1>"

        if not matches:
            return "<h1>Şu an canlı maç yok ⚽</h1>"

        for match in matches:

            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            goals_home = match["goals"]["home"]
            goals_away = match["goals"]["away"]

            minute = match["fixture"]["status"]["elapsed"]
            status = match["fixture"]["status"]["short"]

            html += f"""
            <div style="margin-bottom:15px;">
                <b>{home}</b> {goals_home} - {goals_away} <b>{away}</b><br>
                ⏱️ Dakika: {minute} <br>
                📊 Durum: {status}
            </div>
            <hr>
            """

        return html

    except Exception as e:
        return f"Hata: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
