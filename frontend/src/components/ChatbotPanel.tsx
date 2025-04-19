import React, { useState, useEffect } from "react";
import axios from "axios";

// Định nghĩa interface cho model
interface Model {
  name: string;
  version: string;
  capabilities: string;
}

// Định nghĩa interface cho dữ liệu từ API
interface ModelsResponse {
  models: Model[];
}

const ChatbotPanel: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const response = await axios.get<ModelsResponse>("/chatbot/models");
        setModels(response.data.models);
      } catch (error) {
        console.error("Error fetching models:", error);
      }
    };
    fetchModels();
  }, []);

  return (
    <div className="chatbot-panel">
      <h3>Chatbot Management</h3>
      <div>
        <h4>Available Models</h4>
        <ul>
          {models.map((model) => (
            <li key={model.name}>
              {model.name} ({model.version}) - {model.capabilities}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChatbotPanel;
