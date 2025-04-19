import redis
from datetime import datetime, timedelta

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def track_progress(tracker_data: dict) -> dict:
    """
    Track task progress with Gantt chart and ETA.
    """
    try:
        task_id = tracker_data.get("task_id", "default")
        status = tracker_data.get("status", "pending")
        start_time = tracker_data.get("start_time", datetime.now().isoformat())

        # Lưu trạng thái vào Redis
        redis_client.set(f"task:{task_id}", json.dumps({
            "status": status,
            "start_time": start_time,
            "progress": tracker_data.get("progress", 0)
        }))

        # Tính ETA (giả lập)
        eta = (datetime.fromisoformat(start_time) + timedelta(minutes=10)).isoformat()

        # Tạo Gantt chart (giả lập)
        gantt = {
            "task_id": task_id,
            "status": status,
            "start_time": start_time,
            "eta": eta,
            "progress": tracker_data.get("progress", 0)
        }

        return {"tracker": gantt}
    except Exception as e:
        return {"error": str(e)}