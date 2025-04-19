import React, { useState } from "react";
import axios from "axios";

// Định nghĩa interface cho command
interface InfraCommand {
  service: "kubernetes" | "redis" | "cloudflare";
  action: string;
  params: Record<string, any>; // params có thể là object bất kỳ
}

// Định nghĩa interface cho response từ API
interface ExecuteResponse {
  message: string;
}

const InfraPanel: React.FC = () => {
  const [command, setCommand] = useState<InfraCommand>({
    service: "kubernetes",
    action: "",
    params: {},
  });

  const handleExecute = async () => {
    try {
      const response = await axios.post<ExecuteResponse>(
        `/infra/manage-${command.service}`,
        command
      );
      alert(response.data.message);
    } catch (error) {
      console.error("Error executing infra command:", error);
    }
  };

  return (
    <div className="infra-panel">
      <h3>Infrastructure Management</h3>
      <div>
        <h4>Execute Command</h4>
        <select
          value={command.service}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            setCommand({
              ...command,
              service: e.target.value as InfraCommand["service"],
            })
          }
        >
          <option value="kubernetes">Kubernetes</option>
          <option value="redis">Redis</option>
          <option value="cloudflare">Cloudflare</option>
        </select>
        <input
          type="text"
          placeholder="Action (e.g., scale)"
          value={command.action}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setCommand({ ...command, action: e.target.value })
          }
        />
        <button onClick={handleExecute}>Execute</button>
      </div>
    </div>
  );
};

export default InfraPanel;
