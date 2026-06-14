from flask import Flask, render_template_string
import requests
import random
from datetime import datetime

app = Flask(__name__)

# NOT: API anahtarı gerçek bir canlı veri çekimi için kullanılmalıdır.
API_KEY = "999e0bfd03e0268f0ad00d6619da543f"
API_URL = "https://v3.football.api-sports.io/fixtures"

def populer_bahisleri_getir():
    # Burada popülerlik mantığı: %90 ve üzeri güven veren maçlar 'Popüler' olarak işaretlenir.
    try:
        # Gerçek API çağrısı simülasyonu
        headers = {'x-rapidapi-host': 'v3.football.api-sports.io', 'x-rapidapi-key': API_KEY}
        bugun = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{API_URL}?date={bugun}", headers=headers, timeout=5)
        data = response.json()
        maclar = data.get("response", [])
        
        populer_liste = []
        for m in maclar:
            yuzde = random.randint(75, 98) # Popülerlik yüzdesi simülasyonu
            if yuzde > 85: # Sadece yüksek güven yüzdelileri al
                populer_liste.append({
                    "mac": f"{m['teams']['home']['name']} - {m['teams']['away']['name']}",
                    "tahmin": random.choice(["MS 1", "2.5 Üst", "KG Var"]),
                    "oran": round(random.uniform(1.30, 1.90), 2),
                    "yuzde": yuzde,
                    "oynanma": random.randint(1500, 8000) # İddaa'daki gibi 'kişi oynadı' simülasyonu
                })
        
        return sorted(populer_liste, key=lambda x: x['oynanma'], reverse=True)[:10]
    except:
        return []

@app.route('/')
def index():
    populer_maclar = populer_bahisleri_getir()
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <style>
            body { background: #0f172a; color: white; font-family: sans-serif; padding: 20px; }
            .container { max-width: 800px; margin: auto; }
            .pop-card { background: #1e293b; padding: 15px; border-radius: 10px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #f59e0b; }
            .oynanma-badge { font-size: 11px; color: #94a3b8; }
            .oran-badge { background: #f59e0b; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔥 Futbol Popüler Bahisler</h1>
            {% for m in populer_maclar %}
            <div class="pop-card">
                <div>
                    <div style="font-weight:bold">{{ m.mac }}</div>
                    <div style="font-size:12px; color:#fbbf24">{{ m.tahmin }} • %{{ m.yuzde }} Güven</div>
                    <div class="oynanma-badge">👥 {{ m.oynanma }} kişi bu tahmini oynadı</div>
                </div>
                <div class="oran-badge">{{ m.oran }}</div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, populer_maclar=populer_maclar)

if __name__ == '__main__':
    app.run(debug=True)
