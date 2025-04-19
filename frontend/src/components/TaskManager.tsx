import React, { useState } from "react";
import axios from "axios";
import "./TaskManager.css";

// Định nghĩa interface cho formData
interface FormData {
  name?: string;
  url?: string;
  [key: string]: any; // Cho phép các trường linh hoạt
}

// Định nghĩa interface cho workflow
interface Workflow {
  action?: string;
  [key: string]: any; // Cho phép các trường linh hoạt
}

// Định nghĩa interface cho tracker
interface Tracker {
  task_id?: string;
  [key: string]: any; // Cho phép các trường linh hoạt
}

// Định nghĩa interface cho dataTable (dữ liệu linh hoạt)
interface DataRow {
  [key: string]: any; // Dữ liệu trong dataTable có thể có cấu trúc linh hoạt
}

// Định nghĩa interfaces cho response từ API
interface FormResponse {
  form: FormData;
}

interface WorkflowResponse {
  workflow: Workflow;
}

interface TrackerResponse {
  tracker: Tracker;
}

interface DataToolsResponse {
  data: DataRow[];
}

const TaskManager: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({});
  const [workflow, setWorkflow] = useState<Workflow>({});
  const [tracker, setTracker] = useState<Tracker>({});
  const [dataTable, setDataTable] = useState<DataRow[]>([]);

  const handleFormSubmit = async () => {
    try {
      const response = await axios.post<FormResponse>(
        "/chatbot/forms",
        formData
      );
      setFormData(response.data.form);
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  const handleWorkflowUpdate = async () => {
    try {
      const response = await axios.post<WorkflowResponse>(
        "/chatbot/workflow",
        workflow
      );
      setWorkflow(response.data.workflow);
    } catch (error) {
      console.error("Error updating workflow:", error);
    }
  };

  const handleTrackerUpdate = async () => {
    try {
      const response = await axios.post<TrackerResponse>(
        "/chatbot/tracker",
        tracker
      );
      setTracker(response.data.tracker);
    } catch (error) {
      console.error("Error updating tracker:", error);
    }
  };

  const handleDataTools = async () => {
    try {
      const response = await axios.post<DataToolsResponse>(
        "/chatbot/datatools",
        { dataset: dataTable }
      );
      setDataTable(response.data.data);
    } catch (error) {
      console.error("Error processing data tools:", error);
    }
  };

  return (
    <div className="task-manager">
      <div className="dynamic-forms">
        <h3>Dynamic Forms</h3>
        <input
          type="text"
          placeholder="Name"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setFormData({ ...formData, name: e.target.value })
          }
        />
        <input
          type="text"
          placeholder="URL"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setFormData({ ...formData, url: e.target.value })
          }
        />
        <button onClick={handleFormSubmit}>Submit</button>
      </div>
      <div className="workflow-engine">
        <h3>Workflow Engine</h3>
        <input
          type="text"
          placeholder="Action"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setWorkflow({ ...workflow, action: e.target.value })
          }
        />
        <button onClick={handleWorkflowUpdate}>Update Workflow</button>
      </div>
      <div className="progress-tracker">
        <h3>Progress Tracker</h3>
        <input
          type="text"
          placeholder="Task ID"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setTracker({ ...tracker, task_id: e.target.value })
          }
        />
        <button onClick={handleTrackerUpdate}>Update Tracker</button>
      </div>
      <div className="data-tools">
        <h3>Data Tools</h3>
        <button onClick={handleDataTools}>Generate Table/Chart</button>
        <div className="data-table">
          {dataTable.map((row, index) => (
            <div key={index}>{JSON.stringify(row)}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TaskManager;
