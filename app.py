from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# Günlük Veri Yapısı (Burayı her gün güncelleyebilirsin)
gunluk_veriler = {
    "tarih": datetime.now().strftime('%d.%m.%Y'),
    "tekli": [{"mac": "Galatasaray - Fenerbahçe", "tahmin": "MS 1", "oran": 1.95}],
    "ikili": [{"kupon": "Arsenal - Liverpool & Bayern - Dortmund", "oran": 3.45}],
    "uclu": [{"kupon": "Milan, Inter, Napoli", "oran": 7.20}],
    "banko": [{"mac": "Real Madrid - Getafe", "tahmin": "MS 1", "oran": 1.45}],
    "kazananlar": [{"mac": "Barcelona - Sevilla", "tahmin": "2.5 Üst (Kazandı)", "oran": 1.60}],
    "kaybedenler": [{"mac": "Chelsea - Everton", "tahmin": "KG Var (Kaybetti)", "oran": 1.70}]
}

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <style>
            :root { --yesil: #065f46; --acik-yesil: #10b981; }
            body { font-family: 'Segoe UI', sans-serif; background: #f0fdf4; margin: 0; }
            .header { background: var(--yesil); color: white; padding: 20px; text-align: center; }
            .tabs { display: flex; gap: 5px; background: #064e3b; padding: 10px; overflow-x: auto; }
            .tab-btn { color: white; padding: 10px 15px; cursor: pointer; border: none; background: none; font-weight: bold; }
            .tab-btn:hover { background: var(--acik-yesil); }
            .content { padding: 20px; max-width: 800px; margin: auto; }
            .card { background: white; padding: 15px; border-radius: 8px; border-left: 5px solid var(--acik-yesil); margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .oran { color: var(--yesil); font-weight: bold; float: right; }
        </style>
    </head>
    <body>
        <div class="header"><h1>BET-YEŞİL // {{ data.tarih }} Günlük Tahminler</h1></div>
        <div class="tabs">
            <button class="tab-btn">TEKLİ</button>
            <button class="tab-btn">2'Lİ</button>
            <button class="tab-btn">3'LÜ</button>
            <button class="tab-btn">BANKO</button>
            <button class="tab-btn" style="color:#f87171">KAYBEDENLER</button>
            <button class="tab-btn" style="color:#fbbf24">KAZANANLAR</button>
        </div>
        <div class="content">
            <h3>Günün Tekli Tahminleri</h3>
            {% for item in data.tekli %}
            <div class="card">{{ item.mac }} | {{ item.tahmin }} <span class="oran">Oran: {{ item.oran }}</span></div>
            {% endfor %}
            <!-- Diğer sekmeler buraya dinamik eklenebilir -->
        </div>
    </body>
    </html>
    """
    return render_template_string(html, data=gunluk_veriler)

if __name__ == '__main__':
    app.run(debug=True)
