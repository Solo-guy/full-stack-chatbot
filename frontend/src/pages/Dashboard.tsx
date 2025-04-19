import React, { useState, useEffect } from "react";
import axios from "axios";

// Định nghĩa interface cho metric
interface Metric {
  [key: string]: any; // Dữ liệu metric có thể có cấu trúc linh hoạt
}

// Định nghĩa interface cho response từ API
interface MetricsResponse {
  metrics: Metric[];
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<Metric[]>([]);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.post<MetricsResponse>(
          "/monitoring/monitor-metrics",
          {
            metric: "system_metrics",
            timeframe: "1h",
          }
        );
        setMetrics(response.data.metrics);
      } catch (error) {
        console.error("Error fetching metrics:", error);
      }
    };
    fetchMetrics();
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div>
        <h3>System Metrics</h3>
        <ul>
          {metrics.map((metric, index) => (
            <li key={index}>{JSON.stringify(metric)}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
