from flask import Flask, render_template_string
import random

app = Flask(__name__)

def futbol_populer_bahisleri():
    # İddaa popüler bahis simülasyonu
    takimlar = [("Galatasaray", "Fenerbahçe"), ("Real Madrid", "Barcelona"), ("Arsenal", "Liverpool"), 
                ("Bayern Munich", "Dortmund"), ("Milan", "Inter"), ("PSG", "Monaco"), ("Juventus", "Napoli")]
    
    populer_liste = []
    for ev, dep in takimlar:
        populer_liste.append({
            "mac": f"{ev} - {dep}",
            "tahmin": random.choice(["MS 1", "MS 2", "2.5 Üst", "KG Var"]),
            "oran": round(random.uniform(1.30, 2.10), 2),
            "oynanma": random.randint(2000, 15000)
        })
    # Oynanma sayısına göre yüksekten düşüğe sırala
    return sorted(populer_liste, key=lambda x: x['oynanma'], reverse=True)

@app.route('/')
def index():
    maclar = futbol_populer_bahisleri()
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: 'Roboto', sans-serif; background: #f4f4f4; padding: 20px; color: #333; }
            .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h2 { border-bottom: 2px solid #e11d48; padding-bottom: 10px; color: #e11d48; }
            .mac-item { display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #eee; }
            .mac-info { font-weight: bold; }
            .oynanma { font-size: 12px; color: #777; }
            .oran-box { background: #e11d48; color: white; padding: 8px 15px; border-radius: 4px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>FUTBOL BAHİSLER</h2>
            {% for m in maclar %}
            <div class="mac-item">
                <div>
                    <div class="mac-info">{{ m.mac }}</div>
                    <div class="oynanma">Tahmin: {{ m.tahmin }} | 👥 {{ m.oynanma }} kişi oynadı</div>
                </div>
                <div class="oran-box">{{ m.oran }}</div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, maclar=maclar)

if __name__ == '__main__':
    app.run(debug=True)
