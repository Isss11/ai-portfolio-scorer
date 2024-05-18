import "./circular-progress.css";

function getColor(progress) {
  if (progress < 20) return "#ef4444";
  if (progress < 40) return "#f97316";
  if (progress < 60) return "#facc15";
  if (progress < 80) return "#22c55e";
  return "#3b82f6";
}

export function CircularProgress({ progress, ...props }) {
  return (
    <svg
      viewBox="0 0 100 100"
      className="circular-progress"
      style={{ "--to-progress": progress, "--color": getColor(progress) }}
      {...props}
    >
      <circle className="bg"></circle>
      <circle className="fg"></circle>
    </svg>
  );
}
