import { Pie } from "react-chartjs-2";
import "./chartSetup";
import EquipmentTable from "./EquipmentTable";

export default function EquipmentTypeChart({ distribution }) {
  if (!distribution) return null;

  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  const data = {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: [
          "#4CAF50",
          "#2196F3",
          "#FFC107",
          "#9C27B0",
          "#FF5722",
          "#607D8B",
        ],
      },
    ],
  };

  return (
    <div className="chart-row">
      <div className="chart-box">
        <Pie data={data} />
      </div>

      <div className="table-box">
        <EquipmentTable distribution={distribution} />
      </div>
    </div>
  );
}
