import React from "react";
import ChatbotInterface from "../components/ChatbotInterface";
import TaskManager from "../components/TaskManager";

const Chatbot: React.FC = () => {
  return (
    <div className="chatbot-page">
      <h2>Chatbot</h2>
      <div className="dual-pane">
        <div className="left-pane">
          <ChatbotInterface />
        </div>
        <div className="right-pane">
          <TaskManager />
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
