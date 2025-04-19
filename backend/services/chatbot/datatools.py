import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def process_data_tools(data: dict) -> dict:
    """
    Process data tools (tables, charts, export).
    """
    try:
        action = data.get("action")
        dataset = data.get("dataset", [])

        # Tạo bảng dữ liệu
        df = pd.DataFrame(dataset)

        # Lọc/sắp xếp
        if data.get("filter"):
            df = df[df[data["filter"]["column"]].str.contains(data["filter"]["value"])]
        if data.get("sort"):
            df = df.sort_values(data["sort"]["column"], ascending=data["sort"]["ascending"])

        # Tạo biểu đồ
        if action == "chart":
            plt.figure(figsize=(8, 6))
            if data["chart_type"] == "bar":
                df.plot(kind="bar", x=data["x"], y=data["y"])
            elif data["chart_type"] == "line":
                df.plot(kind="line", x=data["x"], y=data["y"])
            elif data["chart_type"] == "pie":
                df.plot(kind="pie", y=data["y"])
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            chart = base64.b64encode(buf.read()).decode("utf-8")
            plt.close()
            return {"chart": chart}

        # Xuất dữ liệu
        if action == "export":
            if data["format"] == "csv":
                return {"data": df.to_csv(index=False)}
            elif data["format"] == "json":
                return {"data": df.to_json(orient="records")}
            elif data["format"] == "pdf":
                # Giả lập PDF (cần pdfkit trong thực tế)
                return {"data": "PDF export placeholder"}

        return {"table": df.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}