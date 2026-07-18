import { useEffect, useRef, useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  History,
  ImagePlus,
  Leaf,
  Sparkles,
  Upload,
  WandSparkles,
} from "lucide-react";
import { analyzeImage } from "../services/api";

const MAX_FILE_SIZE = 10 * 1024 * 1024;

const ALLOWED_FILE_TYPES = [
  "image/jpeg",
  "image/png",
  "image/webp",
];

export default function Home({
  onResult,
  onOpenHistory,
}) {
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  function validateFile(selectedFile) {
    if (!ALLOWED_FILE_TYPES.includes(selectedFile.type)) {
      return "Please upload a JPG, PNG, or WEBP image.";
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      return "The image must be smaller than 10 MB.";
    }

    return "";
  }

  function updateSelectedFile(selectedFile) {
    if (!selectedFile) return;

    const validationError = validateFile(selectedFile);

    if (validationError) {
      setError(validationError);
      return;
    }

    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setError("");
  }

  function chooseFile(event) {
    const selectedFile = event.target.files?.[0];
    updateSelectedFile(selectedFile);
  }

  function handleDragEnter(event) {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(true);
  }

  function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();

    if (event.currentTarget.contains(event.relatedTarget)) {
      return;
    }

    setDragActive(false);
  }

  function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
  }

  function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();

    setDragActive(false);

    const selectedFile = event.dataTransfer.files?.[0];
    updateSelectedFile(selectedFile);
  }

  function openFilePicker() {
    fileInputRef.current?.click();
  }

  function removeFile() {
    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setFile(null);
    setPreview("");
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  async function submit(event) {
    event.preventDefault();

    if (!file) {
      setError("Choose a street or neighborhood image first.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await analyzeImage(file);
      onResult(result);
    } catch (err) {
      setError(
        err?.message ||
          "The image could not be analyzed. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="home-page">
      <header className="hero">
        <div className="brand">
          <span className="brand-icon">
            <Leaf size={22} />
          </span>

          <span>Canopy AI</span>
        </div>

        <p className="eyebrow">
          AI-powered Urban Improvement Assistant
        </p>

        <h1>
          Reimagine streets as greener, cooler, and more walkable places.
        </h1>

        <p className="hero-copy">
          Upload one urban image and receive an AI-powered assessment,
          practical improvement recommendations, sustainability scores,
          and a downloadable project report.
        </p>

        <div className="hero-actions">
          <button
            type="button"
            onClick={openFilePicker}
          >
            <Upload size={19} />
            Upload an Image
          </button>

          <button
            type="button"
            className="secondary"
            onClick={onOpenHistory}
          >
            <History size={19} />
            View Project History
          </button>
        </div>

        <div className="hero-highlights">
          <span>
            <CheckCircle2 size={17} />
            Urban scene analysis
          </span>

          <span>
            <CheckCircle2 size={17} />
            Practical recommendations
          </span>

          <span>
            <CheckCircle2 size={17} />
            Downloadable PDF report
          </span>
        </div>
      </header>

      <section className="workflow-section">
        <div className="section-heading">
          <p className="eyebrow">How it works</p>
          <h2>From one image to actionable urban insights</h2>
        </div>

        <div className="workflow">
          <article className="workflow-card">
            <span className="workflow-number">01</span>

            <div className="workflow-icon">
              <Upload size={24} />
            </div>

            <h3>Upload</h3>

            <p>
              Add a clear photo of a street, neighborhood, public space,
              or parking area.
            </p>
          </article>

          <ArrowRight
            className="workflow-arrow"
            size={24}
            aria-hidden="true"
          />

          <article className="workflow-card">
            <span className="workflow-number">02</span>

            <div className="workflow-icon">
              <WandSparkles size={24} />
            </div>

            <h3>Analyze</h3>

            <p>
              AI evaluates greenery, shade, walkability, heat risk,
              solar potential, and current urban issues.
            </p>
          </article>

          <ArrowRight
            className="workflow-arrow"
            size={24}
            aria-hidden="true"
          />

          <article className="workflow-card">
            <span className="workflow-number">03</span>

            <div className="workflow-icon">
              <Leaf size={24} />
            </div>

            <h3>Improve</h3>

            <p>
              Review recommendations, expected impact, visualization,
              and a structured PDF report.
            </p>
          </article>
        </div>
      </section>

      <section className="analysis-section">
        <div className="analysis-copy">
          <p className="eyebrow">Start your assessment</p>

          <h2>Upload an urban image</h2>

          <p>
            For the best results, use a clear daytime image showing the
            road, sidewalk, buildings, greenery, and surrounding space.
          </p>

          <div className="supported-formats">
            <span>JPG</span>
            <span>PNG</span>
            <span>WEBP</span>
            <span>Maximum 10 MB</span>
          </div>
        </div>

        <form
          className="upload-panel"
          onSubmit={submit}
        >
          <div
            className={`dropzone ${
              dragActive ? "drag-active" : ""
            } ${preview ? "has-preview" : ""}`}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={chooseFile}
              disabled={loading}
            />

            {preview ? (
              <div className="preview-container">
                <img
                  src={preview}
                  alt="Selected urban area preview"
                />

                <div className="preview-overlay">
                  <div>
                    <strong>{file?.name}</strong>
                    <span>
                      {file
                        ? `${(file.size / 1024 / 1024).toFixed(2)} MB`
                        : ""}
                    </span>
                  </div>

                  <button
                    type="button"
                    className="secondary preview-change-button"
                    onClick={openFilePicker}
                    disabled={loading}
                  >
                    <ImagePlus size={18} />
                    Change Image
                  </button>
                </div>
              </div>
            ) : (
              <button
                type="button"
                className="dropzone-content"
                onClick={openFilePicker}
                disabled={loading}
              >
                <span className="upload-icon">
                  <Upload size={38} />
                </span>

                <strong>
                  Drag and drop an image here
                </strong>

                <span>
                  or click to browse your device
                </span>
              </button>
            )}
          </div>

          {preview && (
            <button
              type="button"
              className="remove-file-button"
              onClick={removeFile}
              disabled={loading}
            >
              Remove selected image
            </button>
          )}

          {error && (
            <p
              className="error"
              role="alert"
            >
              {error}
            </p>
          )}

          <button
            type="submit"
            className="analyze-button"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="button-spinner" />
                Analyzing Urban Image...
              </>
            ) : (
              <>
                <Sparkles size={20} />
                Start AI Analysis
                <ArrowRight size={19} />
              </>
            )}
          </button>

          <p className="analysis-disclaimer">
            Canopy AI provides early-stage indicators and recommendations.
            Results are not a substitute for professional engineering,
            architectural, or municipal assessment.
          </p>
        </form>
      </section>
    </main>
  );
}