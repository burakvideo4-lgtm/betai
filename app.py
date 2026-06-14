from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# Günlük Yönetim Paneli - Burayı güncellemen yeterli
DATA = {
    "tarih": datetime.now().strftime('%d.%m.%Y'),
    "tabs": {
        "TEKLİ": [{"mac": "Galatasaray - Fenerbahçe", "tahmin": "MS 1", "oran": 1.95}],
        "İKİLİ": [{"kupon": "Arsenal - Liverpool & Bayern - Dortmund", "oran": 3.45}],
        "ÜÇLÜ": [{"kupon": "Milan - Inter - Napoli", "oran": 7.20}],
        "BANKO": [{"mac": "Real Madrid - Getafe", "tahmin": "MS 1", "oran": 1.45}],
        "KAZANANLAR": [{"mac": "Barcelona - Sevilla", "tahmin": "2.5 Üst", "oran": 1.60}],
        "KAYBEDENLER": [{"mac": "Chelsea - Everton", "tahmin": "KG Var", "oran": 1.70}]
    }
}

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>BET-YEŞİL // Premium Analiz</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f0fdf4; margin: 0; color: #333; }
            .header { background: #065f46; color: white; padding: 25px; text-align: center; }
            .tabs-container { display: flex; justify-content: center; gap: 10px; background: #064e3b; padding: 15px; }
            .tab-btn { background: #059669; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px; font-weight: bold; }
            .tab-btn:hover { background: #10b981; }
            .content-box { max-width: 800px; margin: 20px auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .card { border-bottom: 1px solid #eee; padding: 15px 0; display: flex; justify-content: space-between; }
            .oran { background: #065f46; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <div class="header"><h1>BET-YEŞİL // {{ data.tarih }}</h1></div>
        <div class="tabs-container">
            {% for tab in data.tabs.keys() %}
            <button class="tab-btn" onclick="showTab('{{ tab }}')">{{ tab }}</button>
            {% endfor %}
        </div>
        
        <div id="content-area" class="content-box">
            <h2 id="tab-title">Hoş Geldin! Bir kategori seç.</h2>
            <div id="tab-data"></div>
        </div>

        <script>
            const allData = {{ data.tabs | tojson }};
            function showTab(tabName) {
                document.getElementById('tab-title').innerText = tabName;
                const container = document.getElementById('tab-data');
                container.innerHTML = '';
                allData[tabName].forEach(item => {
                    container.innerHTML += `<div class="card">
                        <span>${item.mac || item.kupon} - <b>${item.tahmin || ''}</b></span>
                        <span class="oran">${item.oran}</span>
                    </div>`;
                });
            }
        </script>
    </body>
    </html>
    """, data=DATA)

if __name__ == '__main__':
    app.run(debug=True)
