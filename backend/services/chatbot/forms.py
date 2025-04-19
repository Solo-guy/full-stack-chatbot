from jsonschema import validate, ValidationError

def render_form(form_data: dict) -> dict:
    """
    Render dynamic form from JSON schema.
    """
    try:
        # Ví dụ schema cho form thêm backend
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "url": {"type": "string", "format": "uri"},
                "api_key": {"type": "string"}
            },
            "required": ["name", "url"]
        }

        # Xác thực dữ liệu
        validate(instance=form_data, schema=schema)

        # Tạo form (giả lập, trả về dữ liệu đã xác thực)
        return {
            "form": {
                "name": form_data.get("name"),
                "url": form_data.get("url"),
                "api_key": form_data.get("api_key")
            }
        }
    except ValidationError as e:
        return {"error": f"Invalid form data: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}