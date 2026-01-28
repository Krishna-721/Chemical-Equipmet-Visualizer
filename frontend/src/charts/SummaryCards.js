export default function SummaryCards({ summary }) {
  if (!summary) return null;

  return (
    <div className="cards">
      <div className="card">Total Equipment: {summary.total_equipment}</div>
      <div className="card">Valid Rows: {summary.valid_rows}</div>
      <div className="card">Avg Flowrate: {summary.average_flowrate.toFixed(2)}</div>
      <div className="card">Avg Pressure: {summary.average_pressure.toFixed(2)}</div>
      <div className="card">Avg Temperature: {summary.average_temperature.toFixed(2)}</div>
    </div>
  );
}
