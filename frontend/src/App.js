import { useState } from "react";
import { isAuthenticated } from "./api";

import Login from "./pages/login";
import Upload from "./pages/upload";
import History from "./pages/history";
import Logout from "./components/logout";

import "./style.css";

export default function App() {
  const [authenticated, setAuthenticated] = useState(isAuthenticated());
  const [refreshKey, setRefreshKey]=useState(0)

  function handleLogin() {
    setAuthenticated(true);   
  }

  function handleLogout() {
    setAuthenticated(false);  
  }
  function handleUploadSuccess(){
    setRefreshKey(prev=>prev+1)
  }

  return (
    <div className="container">
      <div className="header">
        <h2>Chemical Equipment Parameter Visualizer</h2>
        {authenticated && <Logout onLogout={handleLogout} />}
      </div>

      {!authenticated && <Login onLogin={handleLogin} />}

      <Upload 
      authenticated={authenticated}
      onUploadSuccess={handleUploadSuccess}
      />

      <History authenticated={authenticated}
      refreshKey={refreshKey}
      />

    </div>
  );
}
