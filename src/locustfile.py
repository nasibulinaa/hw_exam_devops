from locust import HttpUser, task, between
import random

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def healthcheck_endpoint(self):
        self.client.get("/healthcheck")

    @task(3)
    def make_prediction(self):
        # https://docs.locust.io/en/stable/writing-a-locustfile.html#rest-json-apis
        payload = {
            "feature0": random.uniform(4.5, 7.5),  # sepal_length
            "feature1": random.uniform(2.0, 4.0),  # sepal_width
            "feature2": random.uniform(1.0, 6.5),  # petal_length
            "feature3": random.uniform(0.1, 2.5)   # petal_width
            }
        with self.client.get("/predict", 
                            json=payload,
                            catch_response=True,
                            name="/predict") as response:
            if response.status_code == 200:
                data = response.json()
                response.success() if "prediction" in data else response.failure("No data")
            else:
                response.failure(f"Request failed: {response.status_code} - {response.text}")
