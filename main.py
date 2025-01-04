import os
import requests
import pandas as pd
from dotenv import load_dotenv

# 1. Umgebungsvariablen laden
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# 2. API-Endpunkt für Zeitreihendaten (z.B. tägliche Aktienkurse)
BASE_URL = "https://www.alphavantage.co/query"
symbol = "AAPL"  # Beispiel: Apple Inc. (Symbol)
function = "TIME_SERIES_DAILY"  # Tägliche Aktienkurse

# 3. API-Abfrageparameter
params = {"function": function, "symbol": symbol, "apikey": API_KEY, "datatype": "json"}

# 4. API-Daten abrufen
response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Fehler beim Abrufen der Daten: {response.status_code}")
    exit()

# 5. Daten extrahieren und bereinigen
try:
    time_series = data["Time Series (Daily)"]
except KeyError:
    print("Fehler: Die API-Antwort enthält keine Zeitseriendaten.")
    exit()

# Daten in ein DataFrame umwandeln
df = pd.DataFrame.from_dict(time_series, orient="index")
df = df.astype(
    {
        "1. open": float,
        "2. high": float,
        "3. low": float,
        "4. close": float,
        "5. volume": int,
    }
)

# Daten sortieren und bereinigen
df = df.sort_index(ascending=False)  # Umkehrung der Reihenfolge (neueste Daten oben)
df = df.rename(
    columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume",
    }
)

# 6. Speichern als CSV
output_file = "data/stock_data.csv"
df.to_csv(output_file)

print(f"Die Daten wurden erfolgreich in {output_file} gespeichert.")
