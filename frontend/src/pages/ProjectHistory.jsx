import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  CalendarDays,
  FolderOpen,
  History,
  ImageIcon,
  Leaf,
  Loader2,
  Search,
  SlidersHorizontal,
} from "lucide-react";

import { getProjects } from "../services/api";

function formatDate(value) {
  if (!value) {
    return "Unknown date";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "Unknown date";
  }

  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function ProjectHistory({
  onBack,
  onOpenProject,
}) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [sortOrder, setSortOrder] = useState("newest");

  useEffect(() => {
    let active = true;

    async function loadProjects() {
      setLoading(true);
      setError("");

      try {
        const data = await getProjects();

        if (active) {
          setProjects(Array.isArray(data) ? data : []);
        }
      } catch (err) {
        if (active) {
          setError(
            err?.message ||
              "Failed to load projects. Please try again.",
          );
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadProjects();

    return () => {
      active = false;
    };
  }, []);

  const filteredProjects = useMemo(() => {
    const normalizedQuery = searchQuery
      .trim()
      .toLowerCase();

    const filtered = projects.filter((project) => {
      if (!normalizedQuery) {
        return true;
      }

      return [
        project.filename,
        project.id,
        project.status,
      ]
        .filter(Boolean)
        .some((value) =>
          String(value)
            .toLowerCase()
            .includes(normalizedQuery),
        );
    });

    return [...filtered].sort((first, second) => {
      const firstDate = new Date(
        first.created_at || 0,
      ).getTime();

      const secondDate = new Date(
        second.created_at || 0,
      ).getTime();

      if (sortOrder === "oldest") {
        return firstDate - secondDate;
      }

      return secondDate - firstDate;
    });
  }, [projects, searchQuery, sortOrder]);

  return (
    <main className="history-page">
      <nav className="history-nav">
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
          Back to Home
        </button>
      </nav>

      <section className="history-hero">
        <div className="history-hero-content">
          <div className="history-badge">
            <History size={17} />
            Saved urban assessments
          </div>

          <h1>Project History</h1>

          <p>
            Browse previously analyzed urban projects,
            reopen their results, and review saved
            recommendations and reports.
          </p>
        </div>

        <div className="history-stat-card">
          <span className="history-stat-icon">
            <FolderOpen size={25} />
          </span>

          <div>
            <strong>{projects.length}</strong>
            <span>
              {projects.length === 1
                ? "Saved Project"
                : "Saved Projects"}
            </span>
          </div>
        </div>
      </section>

      {!loading && !error && projects.length > 0 && (
        <section className="history-toolbar">
          <label className="history-search">
            <Search size={19} />

            <input
              type="search"
              value={searchQuery}
              onChange={(event) =>
                setSearchQuery(event.target.value)
              }
              placeholder="Search by filename, ID, or status..."
            />
          </label>

          <label className="history-sort">
            <SlidersHorizontal size={18} />

            <select
              value={sortOrder}
              onChange={(event) =>
                setSortOrder(event.target.value)
              }
            >
              <option value="newest">
                Newest first
              </option>

              <option value="oldest">
                Oldest first
              </option>
            </select>
          </label>
        </section>
      )}

      {loading && (
        <section className="history-state-card">
          <Loader2
            size={34}
            className="spin"
          />

          <h2>Loading Projects</h2>

          <p>
            Retrieving your saved urban assessments.
          </p>
        </section>
      )}

      {error && (
        <section className="history-state-card history-error-state">
          <h2>Unable to Load Projects</h2>

          <p>{error}</p>
        </section>
      )}

      {!loading &&
        !error &&
        projects.length === 0 && (
          <section className="history-state-card">
            <span className="history-empty-icon">
              <ImageIcon size={34} />
            </span>

            <h2>No Projects Yet</h2>

            <p>
              Analyze your first urban image to start
              building your Canopy AI project history.
            </p>

            <button
              type="button"
              onClick={onBack}
            >
              Start First Analysis
            </button>
          </section>
        )}

      {!loading &&
        !error &&
        projects.length > 0 &&
        filteredProjects.length === 0 && (
          <section className="history-state-card">
            <Search size={32} />

            <h2>No Matching Projects</h2>

            <p>
              Try a different filename, project ID, or
              status.
            </p>

            <button
              type="button"
              className="secondary"
              onClick={() => setSearchQuery("")}
            >
              Clear Search
            </button>
          </section>
        )}

      {!loading &&
        !error &&
        filteredProjects.length > 0 && (
          <>
            <div className="history-results-header">
              <div>
                <p className="eyebrow">
                  Previous analyses
                </p>

                <h2>
                  {filteredProjects.length}{" "}
                  {filteredProjects.length === 1
                    ? "Project"
                    : "Projects"}
                </h2>
              </div>

              {searchQuery && (
                <p>
                  Showing results for “{searchQuery}”
                </p>
              )}
            </div>

            <section className="history-grid">
              {filteredProjects.map((project) => (
                <article
                  key={project.id}
                  className="history-card"
                >
                  <div className="history-image-wrapper">
                    <img
                      src={project.image_url}
                      alt={
                        project.filename ||
                        "Urban project"
                      }
                    />

                    <span className="history-status">
                      {project.status || "completed"}
                    </span>
                  </div>

                  <div className="history-content">
                    <div className="history-card-heading">
                      <span className="history-card-icon">
                        <ImageIcon size={18} />
                      </span>

                      <div>
                        <h3>
                          {project.filename ||
                            "Urban project"}
                        </h3>

                        <p>
                          Canopy AI urban assessment
                        </p>
                      </div>
                    </div>

                    <dl className="history-meta">
                      <div>
                        <dt>Project ID</dt>
                        <dd>{project.id}</dd>
                      </div>

                      <div>
                        <dt>
                          <CalendarDays size={15} />
                          Created
                        </dt>

                        <dd>
                          {formatDate(
                            project.created_at,
                          )}
                        </dd>
                      </div>
                    </dl>

                    <button
                      type="button"
                      className="history-open-button"
                      onClick={() =>
                        onOpenProject(project)
                      }
                    >
                      <FolderOpen size={18} />
                      Open Project
                    </button>
                  </div>
                </article>
              ))}
            </section>
          </>
        )}
    </main>
  );
}