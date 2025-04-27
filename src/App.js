import React, { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", selectedFile); // 🔥 MUST MATCH FastAPI

    try {
      const response = await fetch("http://localhost:8000/predict/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const jsonResponse = await response.json();
      setResult(jsonResponse);
    } catch (err) {
      console.error("Error processing the image:", err);
      setError("Failed to process image. Please try again.");
    }

    setLoading(false);
  };

  const handleClear = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    document.getElementById("fileInput").value = "";
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <h1>Emoji Detector</h1>
          <p>Upload an image to detect emojis and get their Unicode values.</p>
        </div>
      </header>

      <main className="main-container">
        <div className="card upload-card">
          <form onSubmit={handleSubmit}>
            <label htmlFor="fileInput" className="custom-file-upload">
              {selectedFile ? selectedFile.name : "Select an image"}
            </label>
            <input
              id="fileInput"
              type="file"
              accept="image/*"
              onChange={handleFileChange}
            />
            <div className="button-group">
              <button type="submit" disabled={loading || !selectedFile}>
                {loading ? "Processing..." : "Upload"}
              </button>
              {selectedFile && (
                <button
                  type="button"
                  className="clear-button"
                  onClick={handleClear}
                >
                  Clear
                </button>
              )}
            </div>
          </form>
        </div>

        {error && (
          <div className="card error-card">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="card result-card">
            <h2>Analysis Result</h2>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>© 2025 Emoji Detector. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
