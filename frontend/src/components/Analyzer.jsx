import { useEffect, useRef, useState } from "react";
import InputPanel from "./InputPanel";
import LoadingAnalysis from "./LoadingAnalysis";
import ResultCard from "./ResultCard";
import ThreatJourney, { STAGES } from "./ThreatJourney";
import { predict, ApiError } from "../api/predict";

const CYCLE_STAGE_COUNT = STAGES.length - 1; // stages before "verdict" — cycled while waiting on the API
const STAGE_INTERVAL_MS = 320;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function Analyzer({ onResult, id }) {
  const [mode, setMode] = useState("sms");
  const [input, setInput] = useState("");
  const [phase, setPhase] = useState("idle"); // idle | analyzing | result | error
  const [activeIndex, setActiveIndex] = useState(-1);
  const [result, setResult] = useState(null);
  const [resultMeta, setResultMeta] = useState(null); // { mode, preview }
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  useEffect(() => () => clearInterval(intervalRef.current), []);

  function switchMode(nextMode) {
    if (nextMode === mode) return;
    setMode(nextMode);
    setInput("");
    setPhase("idle");
    setResult(null);
    setError(null);
    setActiveIndex(-1);
  }

  function handleClear() {
    setInput("");
    setPhase("idle");
    setResult(null);
    setError(null);
    setActiveIndex(-1);
  }

  async function handleAnalyze() {
    const submitted = input.trim();
    if (!submitted) return;

    setPhase("analyzing");
    setError(null);
    setResult(null);
    setActiveIndex(0);

    let cycle = 0;
    intervalRef.current = setInterval(() => {
      cycle = (cycle + 1) % CYCLE_STAGE_COUNT;
      setActiveIndex(cycle);
    }, STAGE_INTERVAL_MS);

    const minimumDuration = sleep(STAGE_INTERVAL_MS * 3);

    try {
      const [data] = await Promise.all([predict(submitted, mode), minimumDuration]);
      clearInterval(intervalRef.current);
      setActiveIndex(STAGES.length - 1); // land on "Verdict"
      await sleep(260);
      setActiveIndex(STAGES.length); // mark full pipeline complete
      setResult(data);
      setResultMeta({
        mode,
        preview: submitted.length > 140 ? `${submitted.slice(0, 140)}…` : submitted,
      });
      setPhase("result");
      onResult({
        id: `${Date.now()}`,
        inputType: mode,
        preview: submitted.length > 60 ? `${submitted.slice(0, 60)}…` : submitted,
        prediction: data.prediction,
        confidence: data.confidence,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      });
    } catch (err) {
      clearInterval(intervalRef.current);
      setActiveIndex(-1);
      setPhase("error");
      setError(err instanceof ApiError ? err.message : "Something went wrong analyzing this submission.");
    }
  }

  const isAnalyzing = phase === "analyzing";

  return (
    <section className="analyzer" id={id}>
      <div className="analyzer-intro">
        <span className="lab-label">Digital Forensics Console</span>
        <h1>Is this message safe?</h1>
        <p className="analyzer-subhead">
          Submit suspicious digital evidence for AI-powered, explainable threat analysis.
        </p>
      </div>

      <div className="mode-toggle" role="tablist" aria-label="Analysis mode">
        <button
          type="button"
          role="tab"
          aria-selected={mode === "sms"}
          className={`mode-btn ${mode === "sms" ? "is-active" : ""}`}
          onClick={() => switchMode("sms")}
        >
          SMS
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={mode === "url"}
          className={`mode-btn ${mode === "url" ? "is-active" : ""}`}
          onClick={() => switchMode("url")}
        >
          URL
        </button>
      </div>

      <InputPanel
        mode={mode}
        value={input}
        onChange={setInput}
        onAnalyze={handleAnalyze}
        onClear={handleClear}
        disabled={isAnalyzing}
      />

      {isAnalyzing && <LoadingAnalysis activeIndex={activeIndex} />}

      {phase === "error" && (
        <div className="error-banner glass-panel" role="alert">
          <span className="lab-label">Detection Engine Unreachable</span>
          <p>{error}</p>
        </div>
      )}

      {phase === "result" && result && (
        <ResultCard result={result} mode={resultMeta.mode} inputPreview={resultMeta.preview} />
      )}

      <ThreatJourney activeIndex={activeIndex} />
    </section>
  );
}

export default Analyzer;
