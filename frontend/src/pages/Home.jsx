import { useState } from "react";
import { Leaf, Upload, WandSparkles } from "lucide-react";
import { analyzeImage } from "../services/api";

export default function Home({
  onResult,
  onOpenHistory,
}) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function chooseFile(event) {
    const selected = event.target.files?.[0];
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setError("");
  }

  async function submit(event) {
    event.preventDefault();
    if (!file) {
      setError("Choose a street image first.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const result = await analyzeImage(file);
      onResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <header className="hero">
        <div className="brand"><Leaf size={24} /> Canopy AI</div>
        <p className="eyebrow">AI-powered Urban Improvement Assistant</p>
        <h1>Transform any street into a greener, cooler, and more walkable place.</h1>
        <p className="hero-copy">Upload one image and receive a clear early-stage assessment with practical urban recommendations.</p>
        <button
          type="button"
          className="secondary"
          style={{ marginTop: "32px" }}
          onClick={onOpenHistory}
        >
          View Project History
        </button>
      </header>

      <section className="workflow">
        <div><Upload size={22}/><span>Upload</span></div>
        <div><WandSparkles size={22}/><span>Analyze</span></div>
        <div><Leaf size={22}/><span>Improve</span></div>
      </section>

      <form className="upload-panel" onSubmit={submit}>
        <label className="dropzone">
          {preview ? <img src={preview} alt="Street preview" /> : <><Upload size={42}/><strong>Choose a street or neighborhood image</strong><span>JPG, PNG, or WEBP - up to 10 MB</span></>}
          <input type="file" accept="image/png,image/jpeg,image/webp" onChange={chooseFile} />
        </label>
        {error && <p className="error">{error}</p>}
        <button disabled={loading}>{loading ? "Analyzing..." : "Start AI Analysis"}</button>
      </form>
    </main>
  );
}
