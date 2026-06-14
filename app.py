from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>⚽ BETAI</h1>
    <p>Sistem başarıyla çalışıyor.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
