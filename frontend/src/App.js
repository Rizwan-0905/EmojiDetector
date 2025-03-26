import React, { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("/api/process", {
        method: "POST",
        body: formData,
      });
      const jsonResponse = await response.json();
      setResult(jsonResponse);
    } catch (error) {
      console.error("Error processing the image:", error);
    }
    setLoading(false);
  };

  const handleClear = () => {
    setSelectedFile(null);
    setResult(null);
    // Clear the file input value if needed.
    document.getElementById("fileInput").value = "";
  };

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <h1>Emoji detector</h1>
          <p>
            Upload your screenshot to extract emojis, messages, and timestamps.
          </p>
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
                <button type="button" className="clear-button" onClick={handleClear}>
                  Clear
                </button>
              )}
            </div>
          </form>
        </div>

        {result && (
          <div className="card result-card">
            <h2>Analysis Result</h2>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>© 2025 Emoji detector. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
