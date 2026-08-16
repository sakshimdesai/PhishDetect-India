const STAGES = [
  {
    key: "input",
    label: "Input Received",
    detail: "SMS or URL evidence submitted",
  },
  {
    key: "preprocessing",
    label: "Input Preparation",
    detail: "Input prepared for analysis",
  },
  {
    key: "features",
    label: "Feature Extraction",
    detail: "Convert evidence into model features",
  },
  {
    key: "model",
    label: "Model Inference",
    detail: "Random Forest classification",
  },
  {
    key: "explainability",
    label: "Explainability",
    detail: "Feature-level model attribution",
  },
  {
    key: "verdict",
    label: "Verdict",
    detail: "Prediction + confidence",
  },
];

/**
 * activeIndex:
 * -1 = idle
 * 0..5 = current stage
 * 6 = all stages complete
 */
function ThreatJourney({ activeIndex = -1, id }) {
  return (
    <section
      className="journey"
      id={id}
      aria-label="Detection pipeline"
    >
      <div className="journey-head">
        <span className="lab-label">
          Detection Pipeline
        </span>

        <h3>
          How a submission moves through the lab
        </h3>
      </div>

      <div
        className="journey-track"
        role="list"
      >
        {STAGES.map((stage, index) => {
          const isDone =
            activeIndex > index ||
            activeIndex === STAGES.length;

          const isActive =
            activeIndex === index;

          return (
            <div
              className={`journey-node ${
                isDone ? "is-done" : ""
              } ${
                isActive ? "is-active" : ""
              }`}
              role="listitem"
              key={stage.key}
            >
              <div className="journey-dot">
                <span className="journey-index">
                  {String(index + 1).padStart(2, "0")}
                </span>
              </div>

              <div className="journey-copy">
                <span className="journey-label">
                  {stage.label}
                </span>

                <span className="journey-detail">
                  {stage.detail}
                </span>
              </div>

              {index < STAGES.length - 1 && (
                <div
                  className="journey-line"
                  aria-hidden="true"
                />
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default ThreatJourney;
export { STAGES };