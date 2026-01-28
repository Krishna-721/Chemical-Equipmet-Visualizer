import EquipmentTypeChart from "../charts/EquipmentTypeChart";
import EquipmentTable from "../charts/EquipmentTable";
import api from "../api";

export default function Dashboard({ dataset }) {
  if (!dataset) {
    return <p>Select a dataset to view analysis</p>;
  }

  function downloadPDF() {
    api.get(`report/${dataset.id}/`, { responseType: "blob" })
      .then(res => {
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement("a");
        link.href = url;
        link.download = `${dataset.filename}_report.pdf`;
        link.click();
      });
  }

  return (
    <div className="dashboard">
      <h3>Selected Dataset</h3>
      <p><b>{dataset.filename}</b></p>

      <div className="viz-grid">
        <EquipmentTypeChart
          distribution={dataset.summary.equipment_type_distribution}
        />

        {/* ✅ pass dataset, not summary */}
        <EquipmentTable dataset={dataset} />
      </div>

      <button onClick={downloadPDF}>Download PDF</button>
    </div>
  );
}
