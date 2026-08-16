const SMS_MAX = 1000;

function isPlausibleUrl(value) {
  if (!value.trim()) return false;
  try {
    new URL(value.includes("://") ? value : `http://${value}`);
    return /\./.test(value);
  } catch {
    return false;
  }
}

function InputPanel({ mode, value, onChange, onAnalyze, onClear, disabled }) {
  const trimmed = value.trim();
  const urlLooksValid = mode === "url" ? isPlausibleUrl(value) : true;
  const canAnalyze = trimmed.length > 0 && urlLooksValid && !disabled;

  return (
    <div className="input-panel glass-panel">
      <div className="input-panel-head">
        <span className="lab-label">
          {mode === "sms" ? "Evidence · SMS Message" : "Evidence · URL"}
        </span>
        {mode === "sms" && (
          <span className={`char-count ${trimmed.length > SMS_MAX ? "is-over" : ""}`}>
            {value.length}/{SMS_MAX}
          </span>
        )}
      </div>

      {mode === "sms" ? (
        <textarea
          className="input-textarea"
          placeholder="Paste a suspicious SMS message here..."
          value={value}
          maxLength={SMS_MAX}
          onChange={(event) => onChange(event.target.value)}
          disabled={disabled}
          aria-label="Suspicious SMS message"
          rows={6}
        />
      ) : (
        <input
          className="input-url"
          type="text"
          inputMode="url"
          placeholder="https://example.com/verify"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          disabled={disabled}
          aria-label="Suspicious URL"
          aria-invalid={trimmed.length > 0 && !urlLooksValid}
        />
      )}

      {mode === "url" && trimmed.length > 0 && !urlLooksValid && (
        <p className="input-hint is-warning" role="alert">
          That doesn't look like a valid URL yet — check it includes a domain, e.g. example.com/path
        </p>
      )}

      <div className="input-panel-actions">
        <button
          type="button"
          className="btn btn-ghost"
          onClick={onClear}
          disabled={disabled || value.length === 0}
        >
          Clear
        </button>
        <button
          type="button"
          className="btn btn-primary"
          onClick={onAnalyze}
          disabled={!canAnalyze}
        >
          Analyze Threat
        </button>
      </div>
    </div>
  );
}

export default InputPanel;
