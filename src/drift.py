import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

rng = np.random.RandomState(seed=42)

def introduce_small_drift(current, noise_scale=0.05):
    current = current.copy()
    n = len(current)
    for col in current.select_dtypes(include=[np.number]).columns:
        noise = rng.normal(loc=0.0, scale=noise_scale, size=n)
        current[col] = current[col] + noise
    return current

def check_drift():
    # Reference data
    iris = load_iris()
    reference_data = pd.DataFrame(iris.data, columns=iris.feature_names)
    
    # Add drift (create current data)
    current_data = pd.DataFrame(iris.data, columns=iris.feature_names)
    current_data = introduce_small_drift(current_data, noise_scale=0.8)

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    report.save_html('drift_report_simple.html')

if __name__ == "__main__":
    check_drift()