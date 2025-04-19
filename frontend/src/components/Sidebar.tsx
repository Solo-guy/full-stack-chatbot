import React from "react";
import { Link } from "react-router-dom";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h3>Modules</h3>
      <ul>
        <li>
          <Link to="/">Dashboard</Link>
        </li>
        <li>
          <Link to="/chatbot">Chatbot</Link>
        </li>
        <li>
          <Link to="/backend">Backend</Link>
        </li>
        <li>
          <Link to="/frontend">Frontend</Link>
        </li>
        <li>
          <Link to="/infra">Infrastructure</Link>
        </li>
        <li>
          <Link to="/monitoring">Monitoring</Link>
        </li>
        <li>
          <Link to="/ai">AI</Link>
        </li>
        <li>
          <Link to="/knowledge">Knowledge</Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
