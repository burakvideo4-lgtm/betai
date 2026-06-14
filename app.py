from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# Burayı her gün güncelleyip kaydedersen site otomatik güncellenir
DATA = {
    "tarih": datetime.now().strftime('%d.%m.%Y'),
    "tabs": {
        "TEKLİ": [{"lig": "İngiltere - PL", "mac": "Arsenal - Liverpool", "tahmin": "MS 1", "oran": "1.95"}],
        "İKİLİ": [{"lig": "İngiltere / Almanya", "mac": "Arsenal - Liverpool & Bayern - Dortmund", "tahmin": "MS 1 & Üst", "oran": "3.45"}],
        "ÜÇLÜ": [{"lig": "İtalya Serisi A", "mac": "Milan - Inter - Napoli", "tahmin": "KG VAR", "oran": "7.20"}],
        "BANKO": [{"lig": "İspanya - La Liga", "mac": "Real Madrid - Getafe", "tahmin": "MS 1", "oran": "1.45"}],
        "KAZANANLAR": [{"lig": "Fransa - Ligue 1", "mac": "Barcelona - Sevilla", "tahmin": "2.5 Üst (KAZANDI)", "oran": "1.60"}],
        "KAYBEDENLER": [{"lig": "İngiltere - PL", "mac": "Chelsea - Everton", "tahmin": "KG Var (KAYBETTİ)", "oran": "1.70"}]
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
            .header { background: #065f46; color: white; padding: 25px; text-align: center; border-bottom: 5px solid #047857; }
            .tabs-container { display: flex; justify-content: center; gap: 5px; background: #064e3b; padding: 10px; flex-wrap: wrap; }
            .tab-btn { background: #059669; color: white; border: none; padding: 10px 15px; cursor: pointer; border-radius: 4px; font-weight: bold; font-size: 13px; }
            .tab-btn:hover { background: #10b981; }
            .content-box { max-width: 700px; margin: 20px auto; padding: 10px; }
            .card { 
                background: #ffffff; border: 1px solid #e5e7eb; border-left: 6px solid #065f46; 
                border-radius: 8px; padding: 16px; margin-bottom: 12px; display: flex; 
                justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .mac-detay { display: flex; flex-direction: column; gap: 4px; }
            .lig-adi { font-size: 11px; color: #6b7280; text-transform: uppercase; font-weight: 700; }
            .mac-isim { font-size: 14px; font-weight: 600; color: #111827; }
            .tahmin-badge { background: #d1fae5; color: #065f46; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; width: fit-content; }
            .oran-kutu { background: #065f46; color: white; padding: 10px 18px; border-radius: 6px; font-weight: 800; font-size: 16px; }
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
            <h2 id="tab-title" style="text-align:center; color:#065f46;">Lütfen Bir Kategori Seçin</h2>
            <div id="tab-data"></div>
        </div>

        <script>
            const allData = {{ data.tabs | tojson }};
            function showTab(tabName) {
                document.getElementById('tab-title').innerText = tabName;
                const container = document.getElementById('tab-data');
                container.innerHTML = '';
                allData[tabName].forEach(item => {
                    container.innerHTML += `
                    <div class="card">
                        <div class="mac-detay">
                            <span class="lig-adi">${item.lig}</span>
                            <span class="mac-isim">${item.mac}</span>
                            <span class="tahmin-badge">TAHMİN: ${item.tahmin}</span>
                        </div>
                        <div class="oran-kutu">${item.oran}</div>
                    </div>`;
                });
            }
        </script>
    </body>
    </html>
    """, data=DATA)

if __name__ == '__main__':
    app.run(debug=True)
