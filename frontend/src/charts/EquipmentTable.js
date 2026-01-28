export default function EquipmentTable({ dataset }) {
  if (!dataset || !dataset.summary) {
    return <p>Select a dataset to view details</p>;
  }

  const distribution = dataset.summary.equipment_type_distribution;

  if (!distribution) {
    return <p>No equipment distribution data available</p>;
  }

  const rows = Object.entries(distribution);

  return (
    <table border="1" cellPadding="8">
      <thead>
        <tr>
          <th>E quipment Type</th>
          <th>Count</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(([type, count]) => (
          <tr key={type}>
            <td>{type}</td>
            <td>{count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
