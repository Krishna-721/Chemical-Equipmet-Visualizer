import { useState } from "react";
import api from "../api";

export default function Upload({ authenticated, onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleUpload() {
    if (!authenticated) {
      setError("Login required to upload datasets");
      return;
    }

    if (!file) {
      setError("No file selected");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    api.post("upload/", formData)
      .then(res => {
        setFile(null);
        onUploadSuccess(res.data.summary);
      })
      .catch(err => {
        setError(
          err.response?.data?.error || "Upload failed"
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }

  return (
    <div className="card">
      <h3>Upload Dataset</h3>

      <input
        type="file"
        disabled={!authenticated || loading}
        onChange={e => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        disabled={!authenticated || loading}
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {!authenticated && (
        <p className="error">Login required</p>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
}
