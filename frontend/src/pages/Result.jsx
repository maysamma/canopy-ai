import { useMemo, useState } from "react";
import {
  AlertTriangle,
  ArrowLeft,
  Building2,
  CheckCircle2,
  Download,
  FileText,
  ImageIcon,
  Leaf,
  Lightbulb,
  Loader2,
  Map,
  Sparkles,
  Sun,
  Trees,
  TrendingUp,
} from "lucide-react";

import ScoreCard from "../components/ScoreCard";
import {
  downloadProjectReport,
  generateVisualization,
} from "../services/api";

function normalizeScore(value) {
  const numericValue = Number(value);

  if (Number.isNaN(numericValue)) {
    return 0;
  }

  return Math.min(100, Math.max(0, numericValue));
}

function getScoreStatus(score) {
  if (score >= 75) {
    return {
      label: "Strong",
      className: "score-status-good",
    };
  }

  if (score >= 50) {
    return {
      label: "Moderate",
      className: "score-status-medium",
    };
  }

  return {
    label: "Needs Improvement",
    className: "score-status-low",
  };
}

function getHeatRiskStatus(score) {
  if (score <= 25) {
    return {
      label: "Low Risk",
      className: "score-status-good",
    };
  }

  if (score <= 50) {
    return {
      label: "Moderate Risk",
      className: "score-status-medium",
    };
  }

  return {
    label: "High Risk",
    className: "score-status-low",
  };
}

function formatValue(value) {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return "Not detected";
  }

  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }

  return String(value);
}

export default function Result({
  project,
  onBack,
}) {
  const { analysis } = project;

  const [generatedImageUrl, setGeneratedImageUrl] = useState(
    project.generated_image_url || null,
  );

  const [
    visualizationLoading,
    setVisualizationLoading,
  ] = useState(false);

  const [
    visualizationError,
    setVisualizationError,
  ] = useState(
    project.visualization_status === "unavailable"
      ? "Image generation is currently unavailable because the Gemini API quota is not active."
      : project.visualization_status === "failed"
        ? "The previous visualization attempt failed. Please try again."
        : "",
  );

  const scoreItems = useMemo(
    () => [
      {
        label: "Green Coverage",
        value: normalizeScore(
          analysis.scores.green_coverage,
        ),
      },
      {
        label: "Walkability",
        value: normalizeScore(
          analysis.scores.walkability,
        ),
      },
      {
        label: "Shade",
        value: normalizeScore(
          analysis.scores.shade,
        ),
      },
      {
        label: "Solar Potential",
        value: normalizeScore(
          analysis.scores.solar_potential,
        ),
      },
      {
        label: "Heat Risk",
        value: normalizeScore(
          analysis.scores.heat_risk,
        ),
        isHeatRisk: true,
      },
    ],
    [analysis.scores],
  );

  const overallScore = useMemo(() => {
    const greenCoverage = normalizeScore(
      analysis.scores.green_coverage,
    );

    const walkability = normalizeScore(
      analysis.scores.walkability,
    );

    const shade = normalizeScore(
      analysis.scores.shade,
    );

    const solarPotential = normalizeScore(
      analysis.scores.solar_potential,
    );

    const heatRisk = normalizeScore(
      analysis.scores.heat_risk,
    );

    const heatComfortScore = 100 - heatRisk;

    const total =
      greenCoverage +
      walkability +
      shade +
      solarPotential +
      heatComfortScore;

    return Math.round(total / 5);
  }, [analysis.scores]);

  const overallStatus = getScoreStatus(overallScore);

  async function handleGenerateVisualization() {
    setVisualizationLoading(true);
    setVisualizationError("");

    try {
      const result = await generateVisualization(
        project.id,
      );

      setGeneratedImageUrl(
        result.generated_image_url,
      );
    } catch (error) {
      setVisualizationError(
        error?.message ||
          "Visualization generation failed.",
      );
    } finally {
      setVisualizationLoading(false);
    }
  }

  return (
    <main className="result-page">
      <nav className="result-nav">
        <div className="brand">
          <span className="brand-icon">
            <Leaf size={21} />
          </span>

          <span>Canopy AI</span>
        </div>

        <button
          type="button"
          className="secondary"
          onClick={onBack}
        >
          <ArrowLeft size={18} />
          New Analysis
        </button>
      </nav>

      <section className="result-hero">
        <div className="result-hero-content">
          <div className="analysis-complete-badge">
            <CheckCircle2 size={17} />
            Analysis completed
          </div>

          <h1>
            Urban Improvement Assessment
          </h1>

          <p className="result-summary">
            {analysis.summary}
          </p>

          <div className="project-meta">
            <span>
              <FileText size={16} />
              Project ID: {project.id}
            </span>

            <span>
              <ImageIcon size={16} />
              {project.filename}
            </span>
          </div>
        </div>

        <div className="result-image-wrapper">
          <img
            src={project.image_url}
            alt="Uploaded urban street"
          />

          <span className="result-image-label">
            Original Urban Scene
          </span>
        </div>
      </section>

      <section className="overview-section">
        <article className="overall-score-card">
          <div className="overall-score-header">
            <div>
              <p className="eyebrow">
                Overall assessment
              </p>

              <h2>Urban Performance Score</h2>
            </div>

            <TrendingUp size={30} />
          </div>

          <div className="overall-score-content">
            <div
              className="overall-score-ring"
              style={{
                "--overall-score": `${overallScore * 3.6}deg`,
              }}
            >
              <div>
                <strong>{overallScore}</strong>
                <span>/ 100</span>
              </div>
            </div>

            <div className="overall-score-description">
              <span
                className={`overall-status ${overallStatus.className}`}
              >
                {overallStatus.label}
              </span>

              <p>
                This score combines greenery,
                walkability, shade, solar potential,
                and heat comfort into one early-stage
                urban performance indicator.
              </p>
            </div>
          </div>
        </article>

        <article className="assessment-summary-card">
          <div className="summary-icon">
            <Sparkles size={24} />
          </div>

          <div>
            <p className="eyebrow">
              Assessment insight
            </p>

            <h2>Key Opportunity</h2>

            <p>
              Focus on the lowest-performing areas
              first to create a cooler, greener, and
              more comfortable pedestrian
              environment.
            </p>
          </div>
        </article>
      </section>

      <section className="score-section">
        <div className="result-section-heading">
          <div>
            <p className="eyebrow">
              Performance indicators
            </p>

            <h2>Urban Assessment Scores</h2>
          </div>

          <p>
            Scores range from 0 to 100 and represent
            early-stage AI indicators based on the
            uploaded image.
          </p>
        </div>

        <div className="scores-grid">
          {scoreItems.map((item) => (
            <div
              className="score-card-wrapper"
              key={item.label}
            >
              <ScoreCard
                label={item.label}
                value={item.value}
                suffix=""
              />

              {(() => {
                const status = item.isHeatRisk
                  ? getHeatRiskStatus(item.value)
                  : getScoreStatus(item.value);

                return (
                  <span className={status.className}>
                    {status.label}
                  </span>
                );
              })()}
            </div>
          ))}
        </div>
      </section>

      <section className="two-column">
        <article className="panel issues-panel">
          <div className="panel-title">
            <span className="panel-title-icon warning-icon">
              <AlertTriangle size={21} />
            </span>

            <div>
              <p className="eyebrow">
                Current condition
              </p>

              <h2>Current Issues</h2>
            </div>
          </div>

          {analysis.issues?.length ? (
            <ul className="issues-list">
              {analysis.issues.map(
                (issue, index) => (
                  <li key={`${issue}-${index}`}>
                    <span>{index + 1}</span>
                    <p>{issue}</p>
                  </li>
                ),
              )}
            </ul>
          ) : (
            <p className="empty-result-message">
              No major urban issues were detected.
            </p>
          )}
        </article>

        <article className="panel scene-panel">
          <div className="panel-title">
            <span className="panel-title-icon scene-icon">
              <Map size={21} />
            </span>

            <div>
              <p className="eyebrow">
                Vision analysis
              </p>

              <h2>Detected Scene</h2>
            </div>
          </div>

          <dl className="scene-details">
            {Object.entries(
              analysis.scene || {},
            )
              .filter(
                ([key]) =>
                  !key.startsWith("image_"),
              )
              .map(([key, value]) => (
                <div key={key}>
                  <dt>
                    {key.replaceAll("_", " ")}
                  </dt>

                  <dd>{formatValue(value)}</dd>
                </div>
              ))}
          </dl>
        </article>
      </section>

      <section className="panel recommendations-panel">
        <div className="result-section-heading recommendation-heading">
          <div>
            <p className="eyebrow">
              Action plan
            </p>

            <h2>
              Recommendations & Expected Impact
            </h2>
          </div>

          <p>
            Practical interventions suggested by
            Canopy AI based on the detected urban
            conditions.
          </p>
        </div>

        <div className="recommendations">
          {analysis.recommendations?.map(
            (item, index) => (
              <article key={`${item.title}-${index}`}>
                <div className="recommendation-top">
                  <span className="recommendation-icon">
                    {index % 4 === 0 ? (
                      <Trees size={21} />
                    ) : index % 4 === 1 ? (
                      <Sun size={21} />
                    ) : index % 4 === 2 ? (
                      <Building2 size={21} />
                    ) : (
                      <Lightbulb size={21} />
                    )}
                  </span>

                  <span
                    className={`priority priority-${String(
                      item.priority,
                    ).toLowerCase()}`}
                  >
                    {item.priority}
                  </span>
                </div>

                <h3>{item.title}</h3>

                <p className="recommendation-action">
                  {item.action}
                </p>

                <div className="expected-impact">
                  <TrendingUp size={17} />

                  <div>
                    <strong>
                      Expected Impact
                    </strong>

                    <small>
                      {item.impact}
                    </small>
                  </div>
                </div>
              </article>
            ),
          )}
        </div>
      </section>

      <section className="panel visualization-panel">
        <div className="result-section-heading">
          <div>
            <p className="eyebrow">
              AI-powered redesign
            </p>

            <h2>AI Visualization</h2>
          </div>

          <p>
            Generate a realistic improved version
            while preserving the original road and
            building layout.
          </p>
        </div>

        {generatedImageUrl ? (
          <div className="visualization-result">
            <div>
              <div className="visualization-image-heading">
                <span>Before</span>
                <small>Original image</small>
              </div>

              <img
                src={project.image_url}
                alt="Original urban scene"
              />
            </div>

            <div>
              <div className="visualization-image-heading">
                <span>After</span>
                <small>AI visualization</small>
              </div>

              <img
                src={generatedImageUrl}
                alt="AI-generated improved urban scene"
              />
            </div>
          </div>
        ) : (
          <div className="visualization-empty-state">
            <span className="visualization-empty-icon">
              <ImageIcon size={34} />
            </span>

            <h3>
              Create an improved urban visualization
            </h3>

            <p>
              Canopy AI will apply the suggested
              greenery, shade, walkability, and
              sustainability improvements.
            </p>

            <button
              type="button"
              onClick={
                handleGenerateVisualization
              }
              disabled={visualizationLoading}
            >
              {visualizationLoading ? (
                <>
                  <Loader2
                    size={18}
                    className="spin"
                  />
                  Generating Visualization...
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  Generate Visualization
                </>
              )}
            </button>
          </div>
        )}

        {visualizationError && (
          <p
            className="visualization-error"
            role="alert"
          >
            {visualizationError}
          </p>
        )}
      </section>

      <section className="report-action-section">
        <div>
          <span className="report-action-icon">
            <FileText size={25} />
          </span>

          <div>
            <h2>Download Project Report</h2>

            <p>
              Export the assessment, scores,
              recommendations, expected impact, and
              available visualizations as a PDF.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={() =>
            downloadProjectReport(project.id)
          }
        >
          <Download size={18} />
          Download PDF Report
        </button>
      </section>

      <p className="disclaimer result-disclaimer">
        {analysis.disclaimer ||
          "Canopy AI provides early-stage indicators and recommendations. Results are not a substitute for professional engineering, architectural, or municipal assessment."}
      </p>
    </main>
  );
}