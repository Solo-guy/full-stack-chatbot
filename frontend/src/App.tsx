import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Dashboard from "./Dashboard";
import Chatbot from "./Chatbot";
import Backend from "./Backend";
import Frontend from "./Frontend";
import Infra from "./Infra";
import Monitoring from "./Monitoring";
import AI from "./AI";
import Knowledge from "./Knowledge";

// Định nghĩa kiểu cho component Route
interface RouteComponentProps {
  // Có thể thêm các props cụ thể nếu cần (ví dụ: match, location, history)
}

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <h1>Admin Panel</h1>
        <Switch>
          <Route exact path="/" component={Dashboard} />
          <Route path="/chatbot" component={Chatbot} />
          <Route path="/backend" component={Backend} />
          <Route path="/frontend" component={Frontend} />
          <Route path="/infra" component={Infra} />
          <Route path="/monitoring" component={Monitoring} />
          <Route path="/ai" component={AI} />
          <Route path="/knowledge" component={Knowledge} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;
