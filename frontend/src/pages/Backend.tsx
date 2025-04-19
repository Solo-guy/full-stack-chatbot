import React from "react";
import BackendPanel from "../components/BackendPanel";

const Backend: React.FC = () => {
  return (
    <div className="backend-page">
      <h2>Backend Management</h2>
      <BackendPanel />
    </div>
  );
};

export default Backend;
