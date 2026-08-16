function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="navbar-mark" aria-hidden="true">
          <svg viewBox="0 0 28 28" width="26" height="26">
            <polygon
              points="14,1.5 26,7.5 26,17 14,26.5 2,17 2,7.5"
              fill="none"
              stroke="var(--signal)"
              strokeWidth="1.4"
            />
            <circle cx="14" cy="13" r="3.2" fill="var(--signal)" />
          </svg>
        </div>
        <div className="navbar-titles">
          <span className="navbar-title">PHISHDETECT INDIA</span>
          <span className="navbar-subtitle lab-label">Threat Lab · AI-Powered Threat Intelligence</span>
        </div>
        <nav className="navbar-links" aria-label="Section navigation">
          <a href="#analyzer">Analyzer</a>
          <a href="#journey">Pipeline</a>
          <a href="#history">History</a>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
