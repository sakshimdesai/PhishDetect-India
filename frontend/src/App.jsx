import { useState } from "react";
import Navbar from "./components/Navbar";
import Analyzer from "./components/Analyzer";
import History from "./components/History";
import Footer from "./components/Footer";
import "./App.css";

function App() {
  const [history, setHistory] = useState([]);

  function handleResult(entry) {
    setHistory((prev) => [entry, ...prev].slice(0, 25));
  }

  return (
    <div className="app-shell">
      <div className="bg-grid" aria-hidden="true" />
      <Navbar />
      <main className="app-main">
        <Analyzer onResult={handleResult} id="analyzer" />
        <History entries={history} id="history" />
      </main>
      <Footer />
    </div>
  );
}

export default App;
