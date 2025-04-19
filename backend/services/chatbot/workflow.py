import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def manage_workflow(workflow_data: dict) -> dict:
    """
    Manage workflow engine with flowchart, undo/redo, and retry.
    """
    try:
        action = workflow_data.get("action")
        workflow_id = workflow_data.get("workflow_id", "default")

        # Lưu hành động vào Redis (hỗ trợ undo/redo)
        history_key = f"workflow:{workflow_id}:history"
        history = redis_client.lrange(history_key, 0, 9)  # Lưu tối đa 10 bước
        history = [json.loads(h) for h in history]
        history.append(workflow_data)
        redis_client.ltrim(history_key, 0, 9)
        redis_client.lpush(history_key, *[json.dumps(h) for h in history])

        # Xử lý hành động
        if action == "undo":
            if len(history) > 1:
                redis_client.lpop(history_key)
                return {"workflow": history[-2]}
        elif action == "redo":
            # Giả lập redo (cần stack riêng trong Redis)
            return {"workflow": history[-1]}
        elif action == "retry":
            # Giả lập retry API
            return {"workflow": workflow_data, "status": "retried"}

        return {"workflow": workflow_data}
    except Exception as e:
        return {"error": str(e)}