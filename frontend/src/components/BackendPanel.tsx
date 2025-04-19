import React, { useState, useEffect } from "react";
import axios from "axios";

// Định nghĩa interface cho status
interface BackendStatus {
  status: string;
  message_count: number;
  metrics: Record<string, any>; // metrics có thể là object bất kỳ
}

const BackendPanel: React.FC = () => {
  const [status, setStatus] = useState<BackendStatus | {}>({});

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get<BackendStatus>(
          "/backend/monitor?name=chat"
        );
        setStatus(response.data);
      } catch (error) {
        console.error("Error fetching backend status:", error);
      }
    };
    fetchStatus();
  }, []);

  return (
    <div className="backend-panel">
      <h3>Backend Management</h3>
      <div>
        <h4>Chat Backend Status</h4>
        <p>Status: {"status" in status ? status.status : "N/A"}</p>
        <p>
          Message Count:{" "}
          {"message_count" in status ? status.message_count : "N/A"}
        </p>
        <p>
          Metrics:{" "}
          {"metrics" in status ? JSON.stringify(status.metrics) : "N/A"}
        </p>
      </div>
    </div>
  );
};

export default BackendPanel;
