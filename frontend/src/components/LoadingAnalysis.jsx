import { STAGES } from "./ThreatJourney";

function LoadingAnalysis({ activeIndex }) {
  const stage = STAGES[Math.min(Math.max(activeIndex, 0), STAGES.length - 1)];

  return (
    <div className="loading-strip glass-panel" role="status" aria-live="polite">
      <span className="loading-pulse" aria-hidden="true" />
      <span className="loading-text">
        <span className="lab-label">Analyzing</span>
        <span className="loading-stage">{stage.label}</span>
      </span>
      <span className="loading-progress lab-label">
        {String(Math.min(activeIndex + 1, STAGES.length)).padStart(2, "0")} / {String(STAGES.length).padStart(2, "0")}
      </span>
    </div>
  );
}

export default LoadingAnalysis;
