function ShapReasons({ reasons }) {
  if (!reasons || reasons.length === 0) {
    return (
      <div className="shap-block">
        <span className="lab-label">Why Was This Flagged?</span>
        <p className="empty-note">
          The model didn't surface any mapped SHAP features for this input.
        </p>
      </div>
    );
  }

  const maxAbs = Math.max(...reasons.map((r) => Math.abs(r.contribution)), 0.01);

  return (
    <div className="shap-block">
      <span className="lab-label">Why Was This Flagged?</span>
      <ul className="shap-list">
        {reasons.map((reason) => {
          const isPhishing = reason.direction === "phishing";
          const widthPct = (Math.abs(reason.contribution) / maxAbs) * 100;
          return (
            <li className="shap-row" key={reason.feature}>
              <div className="shap-row-top">
                <span className="shap-feature">{reason.feature.replaceAll("_", " ")}</span>
                <span className={`shap-contribution ${isPhishing ? "is-threat" : "is-safe"}`}>
                  {reason.contribution > 0 ? "+" : ""}
                  {reason.contribution.toFixed(2)}
                </span>
              </div>
              <div className="shap-bar-track" aria-hidden="true">
                <div
                  className={`shap-bar-fill ${isPhishing ? "is-threat" : "is-safe"}`}
                  style={{ width: `${widthPct}%` }}
                />
              </div>
              <p className="shap-explanation">{reason.reason}</p>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default ShapReasons;
