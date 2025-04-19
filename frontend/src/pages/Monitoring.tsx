import React from "react";
import MonitoringPanel from "../components/MonitoringPanel";

const Monitoring: React.FC = () => {
  return (
    <div className="monitoring-page">
      <h2>Monitoring Management</h2>
      <MonitoringPanel />
    </div>
  );
};

export default Monitoring;
