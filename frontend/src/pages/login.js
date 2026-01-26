import { useState } from "react";
import { setAuth } from "../api";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  function handleLogin() {
    if (!username || !password) {
      alert("Username and password required");
      return;
    }

    setAuth(username, password);
    onLogin(); 
    alert("Login successful");
  }

  return (
    <div className="card">
      <h3>Login</h3>
      <input
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
