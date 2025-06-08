from locust import HttpUser, task, between

class PaymentUser(HttpUser):
    wait_time = between(0.1,1)

    @task
    def create_payment(self):
        self.client.post(
            "/payments/",
            json={"amount": 50},  # ← Correct payload
            headers={"Content-Type": "application/json"}  # ← Important
        )
