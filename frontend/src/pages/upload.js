import { useState } from "react";
import api from "../api";

export default function Upload({ authenticated, onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");

  function handleUpload() {
    if (!authenticated) {
      setError("Login required to upload datasets");
      return;
    }

    if (!file) {
      setError("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    api.post("upload/", formData)
      .then(() => {
        setError("");
        setFile(null);
        onUploadSuccess && onUploadSuccess();
      })
      .catch(err => {
        if (err.response?.status === 403) {
          setError("Authentication required");
        } else {
          setError(err.response?.data?.error || "Upload failed");
        }
      });
  }

  return (
    <div>
      <h3>Upload Dataset</h3>

      <input
        type="file"
        disabled={!authenticated}
        onChange={e => setFile(e.target.files[0])}
      />

      <button disabled={!authenticated} onClick={handleUpload}>
        Upload
      </button>

      {!authenticated && (
        <p style={{ color: "red" }}>Login required</p>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
