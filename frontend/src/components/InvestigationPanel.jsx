import { useState } from "react";

function InvestigationPanel({ result, inputPreview, mode }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="investigation glass-panel">
      <button
        type="button"
        className="investigation-toggle"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
      >
        <span>{open ? "Close Investigation" : "Open Investigation"}</span>
        <span className={`investigation-chevron ${open ? "is-open" : ""}`} aria-hidden="true">▾</span>
      </button>

      {open && (
        <div className="investigation-body">
          <dl className="investigation-grid">
            <div>
              <dt className="lab-label">Input Type</dt>
              <dd>{mode === "sms" ? "SMS" : "URL"}</dd>
            </div>
            <div>
              <dt className="lab-label">Submitted Evidence</dt>
              <dd className="investigation-evidence">{inputPreview}</dd>
            </div>
            <div>
              <dt className="lab-label">Prediction</dt>
              <dd>{result.prediction}</dd>
            </div>
            <div>
              <dt className="lab-label">Confidence</dt>
              <dd>{(result.confidence * 100).toFixed(2)}%</dd>
            </div>
            <div>
              <dt className="lab-label">Mapped SHAP Reasons</dt>
              <dd>{result.reasons?.length ?? 0}</dd>
            </div>
          </dl>

          <div>
            <span className="lab-label">Raw API Response</span>
            <pre className="investigation-json">{JSON.stringify(result, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default InvestigationPanel;
