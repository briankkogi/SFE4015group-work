from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model and other necessary components
#model = joblib.load('rf_model.pkl')
model = joblib.load('best_stacking_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoder = joblib.load('label_encoder.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {
            'Age': int(request.form['Age']),
            'SystolicBP': int(request.form['SystolicBP']),
            'DiastolicBP': int(request.form['DiastolicBP']),
            'BS': float(request.form['BS']),
            'BodyTemp': float(request.form['BodyTemp']),
            'HeartRate': int(request.form['HeartRate'])
        }
        
        # Prepare the input for the model
        df = pd.DataFrame([data])
        df_scaled = scaler.transform(df)
        prediction = model.predict(df_scaled)
        risk_level = label_encoder.inverse_transform(prediction)[0]
        
        return render_template('result.html', risk_level=risk_level)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
