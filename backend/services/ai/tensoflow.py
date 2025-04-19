import tensorflow as tf

def manage_tensorflow(action: str, params: dict) -> dict:
    """
    Manage TensorFlow operations (e.g., run inference, train model).
    """
    try:
        if action == "run_inference":
            # Giả lập inference
            model_path = params.get("model_path")
            model = tf.keras.models.load_model(model_path)
            input_data = params.get("input_data")
            prediction = model.predict(input_data)
            return {"prediction": prediction.tolist()}

        elif action == "train":
            # Giả lập huấn luyện
            return {"message": f"Training started for TensorFlow model {params.get('model_id')}"}

        return {"error": f"Invalid action: {action}"}
    except Exception as e:
        return {"error": str(e)}