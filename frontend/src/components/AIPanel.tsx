import React, { useState } from "react";
import axios from "axios";

// Định nghĩa interface cho modelConfig
interface ModelConfig {
  model_id: string;
  model_name: string;
  params: Record<string, any>; // params có thể là object bất kỳ
}

const AIPanel: React.FC = () => {
  const [modelConfig, setModelConfig] = useState<ModelConfig>({
    model_id: "",
    model_name: "",
    params: {},
  });

  const handleAdjust = async () => {
    try {
      const response = await axios.post<{ message: string }>(
        "/ai/adjust-model",
        modelConfig
      );
      alert(response.data.message);
    } catch (error) {
      console.error("Error adjusting model:", error);
    }
  };

  return (
    <div className="ai-panel">
      <h3>AI Management</h3>
      <div>
        <h4>Adjust Model</h4>
        <input
          type="text"
          placeholder="Model ID"
          value={modelConfig.model_id}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setModelConfig({ ...modelConfig, model_id: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="Model Name"
          value={modelConfig.model_name}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setModelConfig({ ...modelConfig, model_name: e.target.value })
          }
        />
        <button onClick={handleAdjust}>Adjust</button>
      </div>
    </div>
  );
};

export default AIPanel;
