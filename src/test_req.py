import requests

BASE_URL="http://localhost:5000"

resp = requests.get(f"{BASE_URL}/healthcheck")
print(resp.text)

resp = requests.get(f"{BASE_URL}/predict", json={ #versicolor
    "feature0": 5.7,
    "feature1": 2.8,
    "feature2": 4.5,
    "feature3": 1.3,
})
print(resp.text)