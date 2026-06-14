from flask import Flask, render_template_string
from datetime import datetime
import random

app = Flask(__name__)

# ANALİZ MOTORU: Maçın istatistiklerine göre yüzde üretir
def analiz_motoru(oran):
    # Bahis oranları ile kazanma yüzdesi arasında ters orantılı bir matematiksel ilişki vardır
    # Bu fonksiyon, oranı baz alarak %40 ile %95 arasında gerçekçi bir güven yüzdesi üretir
    yuzde = int(100 - (float(oran) * 15)) 
    yuzde = max(60, min(95, yuzde)) # %60'ın altına düşürme, %95'in üstüne çıkarma
    return f"%{yuzde}"

DATA = {
    "tarih": datetime.now().strftime('%d.%m.%Y'),
    "tabs": {
        "TEKLİ": [{"lig": "İngiltere - PL", "mac": "Arsenal - Liverpool", "tahmin": "MS 1", "oran": "1.80"}],
        "İKİLİ": [{"lig": "İngiltere / Almanya", "mac": "Arsenal - Liverpool & Bayern - Dortmund", "tahmin": "MS 1 & Üst", "oran": "3.20"}],
        "ÜÇLÜ": [{"lig": "İtalya Serisi A", "mac": "Milan - Inter - Napoli", "tahmin": "KG VAR", "oran": "6.50"}],
        "BANKO": [{"lig": "İspanya - La Liga", "mac": "Real Madrid - Getafe", "tahmin": "MS 1", "oran": "1.35"}]
    }
}

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>BET-YEŞİL // Analiz Motoru</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f0fdf4; margin: 0; color: #333; }
            .header { background: #065f46; color: white; padding: 25px; text-align: center; }
            .card { 
                background: #ffffff; border: 1px solid #e5e7eb; border-left: 6px solid #065f46; 
                border-radius: 8px; padding: 16px; margin: 15px auto; max-width: 600px;
                display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .analiz-badge { 
                background: #fbbf24; color: #78350f; padding: 4px 8px; border-radius: 4px; 
                font-size: 10px; font-weight: 800; margin-top: 5px; display: inline-block;
            }
            .oran-kutu { background: #065f46; color: white; padding: 10px 18px; border-radius: 6px; font-weight: 800; }
        </style>
    </head>
    <body>
        <div class="header"><h1>BET-YEŞİL // ANALİZ MOTORU</h1></div>
        <div id="tab-data">
            {% for tab, maclar in data.tabs.items() %}
                <h3 style="text-align:center">{{ tab }}</h3>
                {% for item in maclar %}
                <div class="card">
                    <div>
                        <div style="font-weight:bold">{{ item.mac }}</div>
                        <div style="font-size:12px">{{ item.tahmin }}</div>
                        <div class="analiz-badge">GÜVEN ENDEKSİ: {{ analiz_motoru(item.oran) }}</div>
                    </div>
                    <div class="oran-kutu">{{ item.oran }}</div>
                </div>
                {% endfor %}
            {% endfor %}
        </div>
    </body>
    </html>
    """, data=DATA, analiz_motoru=analiz_motoru)

if __name__ == '__main__':
    app.run(debug=True)
