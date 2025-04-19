import requests
from ...utils.db import get_cockroach_session

# APIsix gateway
APISIX_URL = "http://localhost:9080"

def manage_healthcare(action: str, params: dict) -> dict:
    """
    Manage healthcare backend operations (patient record, appointment).
    """
    try:
        if action == "get_record":
            # Gọi API lấy hồ sơ bệnh nhân
            response = requests.get(
                f"{APISIX_URL}/healthcare/record",
                params={"patient_id": params.get("patient_id")}
            )
            if response.status_code != 200:
                return {"error": f"Get record failed: {response.text}"}
            return {"record": response.json().get("record")}

        elif action == "book_appointment":
            # Gọi API đặt lịch hẹn
            response = requests.post(
                f"{APISIX_URL}/healthcare/appointment",
                json={"patient_id": params.get("patient_id"), "doctor_id": params.get("doctor_id"), "time": params.get("time")}
            )
            if response.status_code != 200:
                return {"error": f"Book appointment failed: {response.text}"}

            # Lưu lịch hẹn vào CockroachDB
            with get_cockroach_session() as session:
                session.execute(
                    "INSERT INTO appointments (patient_id, doctor_id, time) VALUES (%s, %s, %s)",
                    (params.get("patient_id"), params.get("doctor_id"), params.get("time"))
                )
                session.commit()

            return {"appointment_id": response.json().get("appointment_id")}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}