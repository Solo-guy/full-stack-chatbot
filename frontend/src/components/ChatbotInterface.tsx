import React, { useState, useEffect } from "react";
import { w3cwebsocket as W3CWebSocket } from "websocket";
import "./ChatbotInterface.css";

// Định nghĩa interface cho message
interface Message {
  type: "user" | "bot";
  content: string;
}

// Định nghĩa interface cho model
interface Model {
  name: string;
  version: string;
  capabilities?: string;
}

// Định nghĩa interface cho dữ liệu từ WebSocket
interface WebSocketMessage {
  response: string;
}

// Định nghĩa interface cho dữ liệu từ API /chatbot/models
interface ModelsResponse {
  models: Model[];
}

// Giả định kiểu cho các component chưa được định nghĩa
const Avatar: React.FC = () => <div>Avatar</div>;
const AIIcon: React.FC = () => <div>AIIcon</div>;
const LatencyGraph: React.FC<{ latency: number }> = ({ latency }) => (
  <div>Latency: {latency}</div>
);

const ChatbotInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [model, setModel] = useState<string>("MiniCPM");
  const [models, setModels] = useState<Model[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<
    "connected" | "disconnected"
  >("disconnected");
  const [latency, setLatency] = useState<number>(0);
  const [tokenCount, setTokenCount] = useState<number>(0);
  const [costEstimate, setCostEstimate] = useState<number>(0);

  useEffect(() => {
    // Connect to WebSocket
    const ws = new W3CWebSocket("ws://localhost:8000/chatbot/ws");
    ws.onopen = () => setConnectionStatus("connected");
    ws.onmessage = (event: MessageEvent) => {
      const data: WebSocketMessage = JSON.parse(event.data);
      setMessages((prev) => [...prev, { type: "bot", content: data.response }]);
    };
    ws.onclose = () => setConnectionStatus("disconnected");

    // Fetch models
    fetch("/chatbot/models")
      .then((res) => res.json())
      .then((data: ModelsResponse) => setModels(data.models))
      .catch((error) => console.error("Error fetching models:", error));

    // Cleanup
    return () => ws.close();
  }, []); // Note: messages không cần trong dependency array vì được xử lý trong setMessages callback

  const handleSend = () => {
    if (input) {
      setMessages((prev) => [...prev, { type: "user", content: input }]);
      const ws = new W3CWebSocket("ws://localhost:8000/chatbot/ws"); // Note: Tạo mới ws ở đây có thể không đúng, cần kiểm tra logic
      ws.onopen = () => {
        ws.send(JSON.stringify({ text: input, model }));
        ws.close(); // Đóng ngay sau khi gửi, cần kiểm tra logic nếu muốn duy trì kết nối
      };
      setInput("");
    }
  };

  return (
    <div className="chatbot-interface">
      <div className="model-management">
        <select
          value={model}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            setModel(e.target.value)
          }
        >
          {models.map((m) => (
            <option key={m.name} value={m.name}>
              {m.name} ({m.version})
            </option>
          ))}
        </select>
        <p>
          Capabilities:{" "}
          {models.find((m) => m.name === model)?.capabilities ?? "N/A"}
        </p>
      </div>
      <div className="chat-history">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            {msg.type === "user" ? <Avatar /> : <AIIcon />}
            <span>{msg.content}</span>
          </div>
        ))}
      </div>
      <div className="nlu-input">
        <input
          type="text"
          value={input}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setInput(e.target.value)
          }
          placeholder="Enter command (/create_order, /scale_pod)"
        />
        <button onClick={handleSend}>Send</button>
        <input type="file" accept=".txt,.pdf" />
        <button>Voice Input</button>
      </div>
      <div className="system-monitor">
        <span className={`led ${connectionStatus}`}></span>
        <LatencyGraph latency={latency} />
        <p>Tokens: {tokenCount}</p>
        <p>Cost: ${costEstimate.toFixed(2)}</p>
      </div>
    </div>
  );
};

export default ChatbotInterface;
