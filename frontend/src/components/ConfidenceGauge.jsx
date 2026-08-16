function ConfidenceGauge({ confidence, verdict }) {
  const pct = Math.round(confidence * 1000) / 10; // one decimal, e.g. 96.4
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - confidence);
  const color = verdict === "Phishing" ? "var(--threat)" : "var(--safe)";

  return (
    <div className="gauge">
      <svg viewBox="0 0 130 130" width="130" height="130">
        <circle cx="65" cy="65" r={radius} fill="none" stroke="var(--hairline)" strokeWidth="8" />
        <circle
          cx="65"
          cy="65"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 65 65)"
          className="gauge-arc"
        />
      </svg>
      <div className="gauge-center">
        <span className="gauge-value" style={{ color }}>{pct}%</span>
        <span className="gauge-label lab-label">Confidence</span>
      </div>
    </div>
  );
}

export default ConfidenceGauge;
