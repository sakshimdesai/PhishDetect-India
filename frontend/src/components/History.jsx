import { useEffect, useState } from "react";

function History({ id }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadHistory() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          "http://127.0.0.1:5000/history?limit=50"
        );

        if (!response.ok) {
          throw new Error("Unable to load prediction history.");
        }

        const data = await response.json();

        setHistory(data.history || []);
      } catch (err) {
        setError(
          "Unable to load prediction history. Please make sure the Flask server is running."
        );
      } finally {
        setLoading(false);
      }
    }

    loadHistory();
  }, []);

  return (
    <section
      className="history glass-panel"
      id={id}
      aria-label="Prediction history"
    >
      <div className="history-head">
        <span className="lab-label">Prediction History</span>

        <h3>Recent analyses</h3>

        <p className="history-note">
          Previous SMS and URL predictions retrieved from the PhishDetect India
          SQLite database.
        </p>
      </div>

      {loading ? (
        <p className="empty-note">Loading prediction history...</p>
      ) : error ? (
        <p className="empty-note">{error}</p>
      ) : history.length === 0 ? (
        <p className="empty-note">No predictions have been recorded yet.</p>
      ) : (
        <ul className="history-list">
          {history.map((entry) => (
            <li className="history-row" key={entry.id}>
              <span
                className={`history-dot ${
                  entry.prediction === "Phishing"
                    ? "is-threat"
                    : "is-safe"
                }`}
                aria-hidden="true"
              />

              <span className="history-type lab-label">
                {entry.input_type.toUpperCase()}
              </span>

              <span className="history-preview">
                {entry.input}
              </span>

              <span
                className={`history-verdict ${
                  entry.prediction === "Phishing"
                    ? "is-threat"
                    : "is-safe"
                }`}
              >
                {entry.prediction}
              </span>

              <span className="history-confidence">
                {(entry.confidence * 100).toFixed(1)}%
              </span>

              <span className="history-time lab-label">
                {entry.timestamp}
              </span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default History;