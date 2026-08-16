import ConfidenceGauge from "./ConfidenceGauge";
import ShapReasons from "./ShapReasons";
import PhishingDNA from "./PhishingDNA";
import InvestigationPanel from "./InvestigationPanel";

function ResultCard({ result, mode, inputPreview }) {
  const isThreat = result.prediction === "Phishing";

  return (
    <div className={`result-card glass-panel ${isThreat ? "is-threat" : "is-safe"}`} role="status">
      <div className="result-banner">
        <div className="result-verdict">
          <span className="lab-label">Verdict</span>
          <h2 className="result-verdict-text">
            {isThreat ? "Threat Detected" : "No Threat Detected"}
          </h2>
          <span className={`result-badge ${isThreat ? "is-threat" : "is-safe"}`}>
            {result.prediction}
          </span>
        </div>
        <ConfidenceGauge confidence={result.confidence} verdict={result.prediction} />
      </div>

      <div className="result-divider" aria-hidden="true" />

      <ShapReasons reasons={result.reasons} />

      <div className="result-divider" aria-hidden="true" />

      <PhishingDNA reasons={result.reasons} verdict={result.prediction} />

      <InvestigationPanel result={result} inputPreview={inputPreview} mode={mode} />
    </div>
  );
}

export default ResultCard;
