from flask import Flask
import random
import os

app = Flask(__name__)

TEAMS = [
    "Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor",
    "Barcelona", "Real Madrid", "PSG", "Man United",
    "Bayern Munich", "Juventus"
]


# -------------------------
# 🧠 TEAM POWER
# -------------------------
def power(team):
    base = random.randint(60, 90)
    if team in ["Galatasaray", "Fenerbahçe", "Beşiktaş", "Real Madrid", "Barcelona"]:
        base += 10
    return min(base, 99)


# -------------------------
# ⚽ MATCH GENERATOR
# -------------------------
def match():
    h = random.choice(TEAMS)
    a = random.choice(TEAMS)
    while h == a:
        a = random.choice(TEAMS)
    return h, a


# -------------------------
# 🧠 ANALYSIS
# -------------------------
def analyze(h, a):
    hp = power(h)
    ap = power(a)

    total = hp + ap

    home = hp / total
    away = ap / total
    draw = random.uniform(0.10, 0.25)

    probs = {"HOME": home, "DRAW": draw, "AWAY": away}
    winner = max(probs, key=probs.get)

    conf = probs[winner]

    return {
        "home": h,
        "away": a,
        "home_p": round(home * 100, 1),
        "draw_p": round(draw * 100, 1),
        "away_p": round(away * 100, 1),
        "winner": winner,
        "confidence": round(conf * 100, 1),
        "home_odds": round(1 / home, 2),
        "draw_odds": round(1 / draw, 2),
        "away_odds": round(1 / away, 2),
    }


# -------------------------
# 🌐 HOME
# -------------------------
@app.route("/")
def home():

    matches = [analyze(*match()) for _ in range(15)]

    high = sorted(matches, key=lambda x: x["confidence"], reverse=True)[:10]
    safe = [m for m in matches if m["confidence"] > 60]
    risky = [m for m in matches if m["confidence"] < 50]

    top = max(matches, key=lambda x: x["confidence"])

    # -------------------------
    # 🎨 UI (DASHBOARD)
    # -------------------------
    html = """
<!DOCTYPE html>
<html>
<head>
<title>BETAI PRO OFFLINE 2.0</title>

<style>
body {
    margin:0;
    font-family: Arial;
    background:#0f172a;
    color:white;
}

.header {
    background:#111827;
    padding:20px;
    text-align:center;
    font-size:24px;
    font-weight:bold;
}

.tabs {
    display:flex;
    justify-content:center;
    background:#1f2937;
}

.tab {
    padding:15px 20px;
    cursor:pointer;
    color:white;
}

.tab:hover {
    background:#374151;
}

.section {
    display:none;
    padding:20px;
}

.active {
    display:block;
}

.card {
    background:#1e293b;
    padding:15px;
    margin:10px 0;
    border-radius:10px;
}
</style>

<script>
function show(tab){
    let sections = document.getElementsByClassName("section");
    for(let s of sections){
        s.style.display="none";
    }
    document.getElementById(tab).style.display="block";
}
</script>

</head>

<body>

<div class="header">⚽ BETAI PRO OFFLINE 2.0</div>

<div class="tabs">
    <div class="tab" onclick="show('kupon')">Kupon</div>
    <div class="tab" onclick="show('high')">Yüksek Oran</div>
    <div class="tab" onclick="show('safe')">Güvenli</div>
    <div class="tab" onclick="show('risk')">Riskli</div>
    <div class="tab" onclick="show('top')">En Güçlü</div>
</div>
"""

    def render(items):
        out = ""
        for m in items:
            out += f"""
            <div class="card">
                <b>{m['home']} vs {m['away']}</b><br>
                📊 %{m['home_p']} | %{m['draw_p']} | %{m['away_p']}<br>
                🎯 {m['winner']} (%{m['confidence']})<br>
                💰 {m['home_odds']} / {m['draw_odds']} / {m['away_odds']}
            </div>
            """
        return out

    html += f"""
<div id="kupon" class="section active">{render(matches[:10])}</div>
<div id="high" class="section">{render(high)}</div>
<div id="safe" class="section">{render(safe)}</div>
<div id="risk" class="section">{render(risky)}</div>
<div id="top" class="section">{render([top])}</div>

</body>
</html>
"""

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
