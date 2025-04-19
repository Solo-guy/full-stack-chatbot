import requests
from ...utils.db import get_cockroach_session

# APIsix gateway
APISIX_URL = "http://localhost:9080"

def manage_education(action: str, params: dict) -> dict:
    """
    Manage education backend operations (course list, quiz submission).
    """
    try:
        if action == "list_courses":
            # Gọi API liệt kê khóa học
            response = requests.get(f"{APISIX_URL}/education/course")
            if response.status_code != 200:
                return {"error": f"List courses failed: {response.text}"}
            return {"courses": response.json().get("courses", [])}

        elif action == "submit_quiz":
            # Gọi API nộp bài kiểm tra
            response = requests.post(
                f"{APISIX_URL}/education/quiz",
                json={"user_id": params.get("user_id"), "quiz_id": params.get("quiz_id"), "answers": params.get("answers")}
            )
            if response.status_code != 200:
                return {"error": f"Submit quiz failed: {response.text}"}

            # Lưu bài kiểm tra vào CockroachDB
            with get_cockroach_session() as session:
                session.execute(
                    "INSERT INTO quizzes (user_id, quiz_id, answers, timestamp) VALUES (%s, %s, %s, %s)",
                    (params.get("user_id"), params.get("quiz_id"), json.dumps(params.get("answers")), params.get("timestamp"))
                )
                session.commit()

            return {"quiz_id": response.json().get("quiz_id")}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}