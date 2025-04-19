import React, { useState } from "react";
import axios from "axios";

// Định nghĩa interface cho settings
interface FrontendSettings {
  platform: "react" | "kotlin" | "swift" | "cpp";
  url: string;
  settings: Record<string, any>; // settings có thể là object bất kỳ
}

// Định nghĩa interface cho response từ API
interface UpdateResponse {
  message: string;
}

const FrontendPanel: React.FC = () => {
  const [settings, setSettings] = useState<FrontendSettings>({
    platform: "react",
    url: "",
    settings: {},
  });

  const handleUpdate = async () => {
    try {
      const response = await axios.post<UpdateResponse>(
        "/frontend/update",
        settings
      );
      alert(response.data.message);
    } catch (error) {
      console.error("Error updating frontend:", error);
    }
  };

  return (
    <div className="frontend-panel">
      <h3>Frontend Management</h3>
      <div>
        <h4>Update Frontend</h4>
        <select
          value={settings.platform}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            setSettings({
              ...settings,
              platform: e.target.value as FrontendSettings["platform"],
            })
          }
        >
          <option value="react">React</option>
          <option value="kotlin">Kotlin</option>
          <option value="swift">Swift</option>
          <option value="cpp">C++</option>
        </select>
        <input
          type="text"
          placeholder="URL"
          value={settings.url}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setSettings({ ...settings, url: e.target.value })
          }
        />
        <button onClick={handleUpdate}>Update</button>
      </div>
    </div>
  );
};

export default FrontendPanel;
