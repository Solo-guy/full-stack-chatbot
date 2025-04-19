def manage_coreml(action: str, params: dict) -> dict:
    """
    Manage Core ML operations (e.g., run inference).
    """
    try:
        if action == "run_inference":
            # Giả lập inference (Core ML chạy trên Swift)
            return {"prediction": f"Core ML inference for model {params.get('model_id')}"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}