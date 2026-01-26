import { useState } from "react";
import { isAuthenticated } from "./api";

import Login from "./pages/login";
import Upload from "./pages/upload";
import History from "./pages/history";
import Logout from "./components/logout";

import "./style.css";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(isAuthenticated());

  function handleLogin() {
    setLoggedIn(true);   
  }

  function handleLogout() {
    setLoggedIn(false);  
  }

  return (
    <div className="container">
      <div className="header">
        <h2>Chemical Equipment Parameter Visualizer</h2>
        {loggedIn && <Logout onLogout={handleLogout} />}
      </div>

      {!loggedIn && <Login onLogin={handleLogin} />}

      <Upload />

      <History />
    </div>
  );
}
