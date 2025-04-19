import requests
from kubernetes import client, config
from ...utils.auth import verify_jwt

# APIsix admin API
APISIX_ADMIN_URL = "http://localhost:9080/admin"

def manage_kubernetes(action: str, params: dict) -> dict:
    """
    Manage Kubernetes operations (e.g., scale pods, update APIsix upstream).
    """
    try:
        # Load Kubernetes configuration
        config.load_kube_config()
        apps_api = client.AppsV1Api()
        core_api = client.CoreV1Api()

        if action == "scale":
            # Scale deployment
            deployment = params.get("deployment")
            replicas = params.get("replicas", 1)
            apps_api.patch_namespaced_deployment_scale(
                name=deployment,
                namespace="default",
                body={"spec": {"replicas": replicas}}
            )

            # Update APIsix upstream
            upstream_data = {
                "nodes": [{"host": params.get("url", "localhost"), "port": 80, "weight": 1}]
            }
            response = requests.put(
                f"{APISIX_ADMIN_URL}/upstreams/{deployment}",
                json=upstream_data
            )
            if response.status_code != 200:
                return {"error": f"Failed to update APIsix upstream: {response.text}"}

            return {"message": f"Scaled {deployment} to {replicas} replicas"}

        elif action == "list_pods":
            # List pods
            pods = core_api.list_namespaced_pod(namespace="default")
            return {"pods": [pod.metadata.name for pod in pods.items]}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}