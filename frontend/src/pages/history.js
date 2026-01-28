import { useEffect, useState } from "react";
import api from "../api";

export default function History({
  authenticated,
  refreshKey,
  onSelect,
  selectedId
}) {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!authenticated) {
      setDatasets([]);
      return;
    }

    setLoading(true);

    api.get("history/")
      .then(res => setDatasets(res.data))
      .finally(() => setLoading(false));
  }, [authenticated, refreshKey]);

  if (!authenticated) {
    return <p>Please login to view history</p>;
  }

  return (
    <div className="card">
      <h3>Last 5 Datasets</h3>

      {loading && <p>Loading history...</p>}

      <ul className="dataset-list">
        {datasets.map(d => (
          <li
            key={d.id}
            onClick={() => onSelect(d)}
            className={
              d.id === selectedId ? "selected" : ""
            }
          >
            {d.filename}
          </li>
        ))}
      </ul>
    </div>
  );
}
