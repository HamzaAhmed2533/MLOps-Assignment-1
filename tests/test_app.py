from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression


app = Flask(__name__)

# Train a simple model when the app starts
df = pd.DataFrame({
    "ad_spend": [100, 200, 300, 400, 500],
    "units_sold": [10, 25, 40, 55, 70],
})
model = LinearRegression()
model.fit(df[["ad_spend"]], df["units_sold"])


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask ML API is running!"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "ad_spend" not in data:
        return jsonify({"error": "Missing 'ad_spend' value"}), 400

    ad_spend = data["ad_spend"]
    predicted = model.predict([[ad_spend]])[0]

    return jsonify({"predicted_units_sold": float(predicted)})


if __name__ == "__main__":
    app.run(debug=True)
