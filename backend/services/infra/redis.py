import redis

# Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def manage_redis(action: str, params: dict) -> dict:
    """
    Manage Redis operations (e.g., set/get cache).
    """
    try:
        if action == "set":
            key = params.get("key")
            value = params.get("value")
            redis_client.set(key, value)
            return {"message": f"Set {key} to {value}"}

        elif action == "get":
            key = params.get("key")
            value = redis_client.get(key)
            return {"value": value.decode('utf-8') if value else None}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}