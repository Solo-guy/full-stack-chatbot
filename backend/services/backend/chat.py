import requests
from kafka import KafkaProducer
import json
from ...utils.db import get_cockroach_session, get_scylla_session

# APIsix gateway
APISIX_URL = "http://localhost:9080"

# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def manage_chat(action: str, params: dict) -> dict:
    """
    Manage chat backend operations (login, send message, start call).
    """
    try:
        if action == "login":
            # Gọi API đăng nhập qua APIsix
            response = requests.post(
                f"{APISIX_URL}/auth/login",
                json={"username": params.get("username"), "password": params.get("password")}
            )
            if response.status_code != 200:
                return {"error": f"Login failed: {response.text}"}
            return {"token": response.json().get("token")}

        elif action == "send_message":
            # Gửi tin nhắn qua APIsix
            response = requests.post(
                f"{APISIX_URL}/chat/send",
                json={"user_id": params.get("user_id"), "message": params.get("message")}
            )
            if response.status_code != 200:
                return {"error": f"Send message failed: {response.text}"}

            # Lưu tin nhắn vào ScyllaDB
            with get_scylla_session() as session:
                session.execute(
                    "INSERT INTO messages (user_id, message, timestamp) VALUES (%s, %s, %s)",
                    (params.get("user_id"), params.get("message"), params.get("timestamp"))
                )

            # Gửi thông báo qua Kafka
            producer.send('chat_messages', {
                'user_id': params.get("user_id"),
                'message': params.get("message"),
                'timestamp': params.get("timestamp")
            })

            return {"message": "Message sent successfully"}

        elif action == "start_call":
            # Bắt đầu cuộc gọi qua APIsix (LiveKit)
            response = requests.post(
                f"{APISIX_URL}/call/start",
                json={"user_id": params.get("user_id"), "room": params.get("room")}
            )
            if response.status_code != 200:
                return {"error": f"Start call failed: {response.text}"}
            return {"call_id": response.json().get("call_id")}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}