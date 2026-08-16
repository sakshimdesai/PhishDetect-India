function PhishingDNA({ reasons, verdict }) {
  const strandLabel =
    verdict === "Phishing"
      ? "Phishing Signals"
      : "Legitimacy Signals";

  return (
    <div className="dna-block">
      <span className="lab-label">{strandLabel}</span>

      {(!reasons || reasons.length === 0) ? (
        <p className="empty-note">
          No dominant signals were detected for this submission.
        </p>
      ) : (
        <div className="dna-grid">
          {reasons.map((reason) => {
            const isPhishing =
              reason.direction === "phishing";

            const contribution =
              Number(reason.contribution);

            const formattedContribution =
              contribution >= 0
                ? `+${contribution.toFixed(2)}`
                : contribution.toFixed(2);

            return (
              <div
                className={`dna-card ${
                  isPhishing ? "is-threat" : "is-safe"
                }`}
                key={reason.feature}
              >
                <span
                  className="dna-strand"
                  aria-hidden="true"
                />

                <span className="dna-feature">
                  {reason.feature.replaceAll("_", " ")}
                </span>

                <span
                  className={`dna-severity ${
                    isPhishing ? "is-threat" : "is-safe"
                  }`}
                >
                  {formattedContribution}
                </span>

                <span className="dna-direction lab-label">
                  {isPhishing
                    ? "Pushes prediction toward phishing"
                    : "Pushes prediction toward legitimate"}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default PhishingDNA;