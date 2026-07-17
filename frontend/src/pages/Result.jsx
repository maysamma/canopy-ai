import { useState } from "react";
import {
  ArrowLeft,
  Download,
  ImageIcon,
  Leaf,
  Loader2,
} from "lucide-react";

import ScoreCard from "../components/ScoreCard";
import {
  downloadProjectReport,
  generateVisualization,
} from "../services/api";


export default function Result({ project, onBack }) {
  const { analysis } = project;

  const [generatedImageUrl, setGeneratedImageUrl] = useState(
    project.generated_image_url || null
  );
  const [visualizationLoading, setVisualizationLoading] = useState(false);

  const [visualizationError, setVisualizationError] = useState(
    project.visualization_status === "unavailable"
      ? "Image generation is currently unavailable because the Gemini API quota is not active."
      : project.visualization_status === "failed"
        ? "The previous visualization attempt failed. Please try again."
        : ""
  );


  async function handleGenerateVisualization() {
    setVisualizationLoading(true);
    setVisualizationError("");

    try {
      const result = await generateVisualization(project.id);

      setGeneratedImageUrl(result.generated_image_url);
    } catch (error) {
      setVisualizationError(
        error.message || "Visualization generation failed."
      );
    } finally {
      setVisualizationLoading(false);
    }
  }

  return (
    <main className="result-page">
      <nav className="result-nav">
        <div className="brand">
          <Leaf size={22} />
          Canopy AI
        </div>

        <button
          className="secondary"
          onClick={onBack}
        >
          <ArrowLeft size={18} />
          New analysis
        </button>
      </nav>

      <section className="result-hero">
        <div>
          <p className="eyebrow">
            Analysis completed
          </p>

          <h1>
            Urban Improvement Assessment
          </h1>

          <p>{analysis.summary}</p>
        </div>

        <img
          src={project.image_url}
          alt="Uploaded street"
        />
      </section>

      <section className="scores-grid">
        <ScoreCard
          label="Green Coverage"
          value={analysis.scores.green_coverage}
        />

        <ScoreCard
          label="Walkability"
          value={analysis.scores.walkability}
        />

        <ScoreCard
          label="Shade"
          value={analysis.scores.shade}
        />

        <ScoreCard
          label="Solar Potential"
          value={analysis.scores.solar_potential}
        />

        <ScoreCard
          label="Heat Risk"
          value={analysis.scores.heat_risk}
          suffix=""
        />
      </section>

      <section className="two-column">
        <article className="panel">
          <h2>Current Issues</h2>

          <ul>
            {analysis.issues.map((issue) => (
              <li key={issue}>
                {issue}
              </li>
            ))}
          </ul>
        </article>

        <article className="panel">
          <h2>Detected Scene</h2>

          <dl>
            {Object.entries(analysis.scene)
              .filter(([key]) => !key.startsWith("image_"))
              .map(([key, value]) => (
                <div key={key}>
                  <dt>
                    {key.replaceAll("_", " ")}
                  </dt>

                  <dd>{value}</dd>
                </div>
              ))}
          </dl>
        </article>
      </section>

      <section className="panel">
        <h2>
          Recommendations & Expected Impact
        </h2>

        <div className="recommendations">
          {analysis.recommendations.map((item) => (
            <article key={item.title}>
              <span className="priority">
                {item.priority}
              </span>

              <h3>{item.title}</h3>

              <p>{item.action}</p>

              <small>{item.impact}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>AI Visualization</h2>

        <p>
          Generate a realistic improved version of the uploaded
          street using the analysis recommendations.
        </p>

        {generatedImageUrl ? (
          <div className="visualization-result">
            <div>
              <h3>Before</h3>

              <img
                src={project.image_url}
                alt="Original urban scene"
              />
            </div>

            <div>
              <h3>After</h3>

              <img
                src={generatedImageUrl}
                alt="AI-generated improved urban scene"
              />
            </div>
          </div>
        ) : (
          <button
            onClick={handleGenerateVisualization}
            disabled={visualizationLoading}
          >
            {visualizationLoading ? (
              <>
                <Loader2
                  size={18}
                  className="spin"
                />
                Generating visualization...
              </>
            ) : (
              <>
                <ImageIcon size={18} />
                Generate Visualization
              </>
            )}
          </button>
        )}

        {visualizationError && (
          <p className="visualization-error">
            {visualizationError}
          </p>
        )}
      </section>

      <p className="disclaimer">
        {analysis.disclaimer}
      </p>

      <button onClick={() => downloadProjectReport(project.id)}>
        <Download size={18} />
        Download PDF Report
      </button>
    </main>
  );
}