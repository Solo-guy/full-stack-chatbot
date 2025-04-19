import requests
from ...utils.db import get_cockroach_session

# APIsix gateway
APISIX_URL = "http://localhost:9080"

def manage_sales(action: str, params: dict) -> dict:
    """
    Manage sales backend operations (list products, create order).
    """
    try:
        if action == "list_products":
            # Gọi API liệt kê sản phẩm
            response = requests.get(f"{APISIX_URL}/sales/list")
            if response.status_code != 200:
                return {"error": f"List products failed: {response.text}"}
            return {"products": response.json().get("products", [])}

        elif action == "create_order":
            # Gọi API tạo đơn hàng
            response = requests.post(
                f"{APISIX_URL}/sales/order",
                json={"user_id": params.get("user_id"), "items": params.get("items")}
            )
            if response.status_code != 200:
                return {"error": f"Create order failed: {response.text}"}

            # Lưu đơn hàng vào CockroachDB
            with get_cockroach_session() as session:
                session.execute(
                    "INSERT INTO orders (user_id, items, timestamp) VALUES (%s, %s, %s)",
                    (params.get("user_id"), json.dumps(params.get("items")), params.get("timestamp"))
                )
                session.commit()

            return {"order_id": response.json().get("order_id")}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}