import { useEffect, useState } from "react";
import { ArrowLeft } from "lucide-react";

import { getProjects } from "../services/api";

export default function ProjectHistory({
  onBack,
  onOpenProject,
}) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProjects() {
      try {
        const data = await getProjects();
        setProjects(data);
      } catch (err) {
        setError(
          err.message || "Failed to load projects."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProjects();
  }, []);

  return (
    <main className="result-page">
      <button
        className="secondary"
        onClick={onBack}
      >
        <ArrowLeft size={18} />
        Back
      </button>

      <h1>Project History</h1>

      <p className="hero-copy">
        Browse previously analyzed urban projects.
      </p>

      {loading && (
        <p>Loading projects...</p>
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {!loading &&
        !error &&
        projects.length === 0 && (
          <div className="panel">
            <h2>No Projects Yet</h2>

            <p>
              Analyze your first urban image to
              start building your project history.
            </p>
          </div>
        )}

      {!loading &&
        !error &&
        projects.length > 0 && (
          <div className="history-grid">
            {projects.map((project) => (
              <article
                key={project.id}
                className="history-card"
              >
                <img
                  src={project.image_url}
                  alt={project.filename}
                />

                <div className="history-content">
                  <h3>{project.filename}</h3>

                  <p>
                    <strong>Project ID:</strong>
                    <br />
                    {project.id}
                  </p>

                  <p>
                    <strong>Created:</strong>
                    <br />
                    {new Date(
                      project.created_at
                    ).toLocaleString()}
                  </p>

                  <span className="history-status">
                    {project.status}
                  </span>

                  <button
                    style={{
                      marginTop: "14px",
                      width: "100%",
                    }}
                    onClick={() =>
                      onOpenProject(project)
                    }
                  >
                    Open Project
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
    </main>
  );
}