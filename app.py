import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Get all currencies from Frankfurter API
def get_currencies():
    url = "https://api.frankfurter.app/currencies"
    response = requests.get(url)
    if response.status_code != 200:
        # fallback if API fails
        return {"USD": "US Dollar", "EUR": "Euro", "INR": "Indian Rupee"}
    return response.json()

# Convert currency
def convert_currency(from_currency, to_currency, amount):
    url = "https://api.frankfurter.app/latest"
    params = {'amount': amount, 'from': from_currency, 'to': to_currency}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    data = response.json()
    return data.get('rates', {}).get(to_currency)

@app.route("/", methods=["POST", "GET"])
def home():
    currencies = get_currencies()
    frm = "USD"
    to = "INR"
    amount = ""
    result = None
    error = None

    if request.method == "POST":
        frm = request.form.get("from_currency", "USD").upper()
        to = request.form.get("to_currency", "INR").upper()
        amount = request.form.get("amount", "")
        try:
            amount_float = float(amount)
            rate = convert_currency(frm, to, amount_float)
            if rate is None:
                error = "⚠️ Conversion failed. Please check currency codes."
            else:
                result = rate
        except ValueError:
            error = "⚠️ Invalid amount entered."

    return render_template("main.html", currencies=currencies, frm=frm, to=to, amount=amount, result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
