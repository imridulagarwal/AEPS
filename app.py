from flask import Flask, render_template_string, send_file
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)
aeps_df = pd.DataFrame()

def scrape_aeps_data():
    url = "https://www.npci.org.in/what-we-do/aeps/product-statistics/2024-25"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    tables = pd.read_html(res.text)
    for table in tables:
        if "Approved Off-us Transaction" in table.columns[1]:
            return table
    return pd.DataFrame()

def generate_plot(df):
    df["Month"] = df["Month Wise"].astype(str)
    df = df.sort_values("Month")
    plt.figure(figsize=(10, 5))
    plt.plot(df["Month"], df["Total Approved Transaction(In Mn"], marker="o")
    plt.title("Total AEPS Transactions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer

@app.route("/")
def home():
    global aeps_df
    aeps_df = scrape_aeps_data()
    if aeps_df.empty:
        return "⚠️ AEPS data not found."
    plot_url = "/plot.png"
    table_html = aeps_df.to_html(classes="table table-bordered", index=False)
    return render_template_string('''
        <html>
        <head><title>AEPS Analytics</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body class="container">
            <h2 class="mt-4">AEPS Dashboard (2024–25)</h2>
            <img src="{{ plot_url }}" class="img-fluid mb-4"/>
            {{ table_html|safe }}
            <a href="/download" class="btn btn-success mt-3">📥 Download Excel</a>
        </body>
        </html>
    ''', plot_url=plot_url, table_html=table_html)

@app.route("/plot.png")
def plot():
    buffer = generate_plot(aeps_df)
    return send_file(buffer, mimetype="image/png")

@app.route("/download")
def download():
    buffer = BytesIO()
    aeps_df.to_excel(buffer, index=False)
    buffer.seek(0)
    return send_file(buffer, download_name="AEPS_2024_25_Data.xlsx", as_attachment=True)

# Production entry point
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
