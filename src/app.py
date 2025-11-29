import platform
from flask import Flask, request
import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import os

MODEL_PATH = 'iris_model.joblib'

app = Flask(__name__)

def load_model():
    model = None
    if os.path.exists(MODEL_PATH):
        print("Loading model...", end="")
        model = joblib.load(MODEL_PATH)
    else:
        print("Generating model...", end="")
        iris = load_iris()
        model = RandomForestClassifier(random_state=42)
        model.fit(iris.data, iris.target)
        joblib.dump(model, MODEL_PATH)
    print("done!")
    return model

model = load_model()
iris_data = load_iris()
feature_names = iris_data["feature_names"]
target_names = iris_data["target_names"]

# Module 1: healthcheck
@app.route('/healthcheck')
def system_info():
    return {
        'Platform': platform.platform(),
        'Node': platform.node(),
    }

# Module 2: prediction
@app.route('/predict')
def predict():
    try:
        data = request.json

        # Request verify
        features = []
        features_array = None
        for i in range(4):
            if (not f"feature{i}" in data):
                return {"error": f"Param 'feature{i}' provided."}, 400
            else:
                features.append(data[f"feature{i}"])
        try:
            features_array = np.array(features, dtype=float).reshape(1, -1)
        except ValueError:
            return {"error": "All features must be numbers"}, 400
        
        # Prediction
        prediction = model.predict(features_array)[0]
        return {"prediction": target_names[prediction],}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host="0.0.0.0")
