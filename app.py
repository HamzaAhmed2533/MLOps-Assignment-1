from flask import Flask
from flask import request
from flask import jsonify
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)


# ========== Load & Train Model ==========
DATA_PATH = os.path.join("data", "sales.csv")

# Load dataset
data = pd.read_csv(DATA_PATH)

# Features (ad spend) and target (units sold)
X = data[["ad_spend"]]
y = data["units_sold"]

# Train linear regression model
model = LinearRegression()
model.fit(X, y)


# ========== API Endpoints ==========


@app.route("/")
def home():
    return {"message": "Flask ML API is running!"}


# Prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input
        data = request.get_json()
        ad_spend = data.get("ad_spend")

        # Validate input
        if ad_spend is None:
            return jsonify({"error": "Missing 'ad_spend' value"}), 400

        # Make prediction
        prediction = model.predict([[ad_spend]])[0]

        return jsonify({
            "ad_spend": ad_spend,
            "predicted_units_sold": round(float(prediction), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
