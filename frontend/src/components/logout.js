import { clearAuth } from "../api";

export default function Logout({ onLogout }) {
  function handleLogout() {
    clearAuth();
    onLogout(); 
  }

  return <button onClick={handleLogout}>Logout</button>;
}
