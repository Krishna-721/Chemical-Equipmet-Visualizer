import { useEffect, useState } from "react";
import api from "../api";

export default function History({ authenticated, refreshKey }) {
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!authenticated) {
      setDatasets([]);
      return;
    }

    api.get("history/")
      .then(res => {
        setDatasets(res.data);
        setError("");
      })
      .catch(() => {
        setDatasets([]);
        setError("Failed to load history");
      });
  }, [authenticated, refreshKey]);

  function downloadPDF(id) {
    if (!authenticated) {
      alert("Login required to download reports");
      return;
    }

    api.get(`report/${id}/`, { responseType: "blob" })
      .then(res => {
        const blob = new Blob([res.data], { type: "application/pdf" });
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = `dataset_${id}_report.pdf`;
        document.body.appendChild(link);
        link.click();
        link.remove();

        window.URL.revokeObjectURL(url);
      })
      .catch(err => {
        if (err.response?.status === 403) {
          alert("Authentication required");
        } else {
          alert("Failed to download PDF");
        }
      });
  }

  if (!authenticated) {
    return <p>Please login to view history</p>;
  }

  return (
    <div className="card">
      <h3>Last 5 Datasets</h3>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {datasets.map(d => (
          <li key={d.id}>
            {d.filename}
            <button
              style={{ marginLeft: "10px" }}
              onClick={() => downloadPDF(d.id)}
              disabled={!authenticated}
            >
              Download PDF
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
