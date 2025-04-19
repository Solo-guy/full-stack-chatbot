import requests

# Cloudflare API
CLOUDFLARE_API = "https://api.cloudflare.com/client/v4"

def manage_cloudflare(action: str, params: dict) -> dict:
    """
    Manage Cloudflare operations (e.g., update DNS, configure WAF).
    """
    try:
        headers = {"Authorization": f"Bearer {params.get('api_key')}"}

        if action == "update_dns":
            # Cập nhật DNS
            response = requests.put(
                f"{CLOUDFLARE_API}/zones/{params.get('zone_id')}/dns_records",
                json={"type": "A", "name": params.get('name'), "content": params.get('ip')},
                headers=headers
            )
            if response.status_code != 200:
                return {"error": f"Failed to update DNS: {response.text}"}
            return {"message": f"DNS updated for {params.get('name')}"}

        elif action == "configure_waf":
            # Cấu hình WAF (giả lập)
            return {"message": f"WAF configured for zone {params.get('zone_id')}"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}