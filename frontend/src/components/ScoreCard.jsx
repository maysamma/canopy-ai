export default function ScoreCard({ label, value, suffix = "%" }) {
  return (
    <article className="score-card">
      <span>{label}</span>
      <strong>{value}{typeof value === "number" ? suffix : ""}</strong>
    </article>
  );
}
