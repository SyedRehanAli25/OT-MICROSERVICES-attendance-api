# client/postgres/models/message.py

class CustomMessage:
    def __init__(self, message: str):
        self.message = message

class HealthMessage:
    def __init__(self, message: str, postgresql: str, redis: str, status: str):
        self.message = message
        self.postgresql = postgresql
        self.redis = redis
        self.status = status
