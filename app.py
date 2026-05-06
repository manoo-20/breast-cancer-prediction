from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

# Load model + scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [float(x) for x in request.form.values()]

        final = np.array(features).reshape(1, -1)
        final = scaler.transform(final)

        prediction = model.predict(final)

        if prediction[0] == 1:
            result = "⚠️ Malignant (High Risk)"
        else:
            result = "✅ Benign (Safe)"

        return render_template('index.html', prediction_text=result)

    except:
        return render_template('index.html', prediction_text="Invalid Input")

if __name__ == "__main__":
    app.run(debug=True)