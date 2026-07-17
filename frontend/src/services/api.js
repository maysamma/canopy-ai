const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function analyzeImage(file) {
  const formData = new FormData();
  formData.append("image", file);

  const response = await fetch(`${API_BASE_URL}/api/projects`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Analysis failed.");
  }

  return {
    ...data,
    image_url: `${API_BASE_URL}${data.image_url}`,
  };
}

export async function generateVisualization(projectId) {
  const response = await fetch(
    `${API_BASE_URL}/api/projects/${projectId}/visualization`,
    {
      method: "POST",
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Visualization generation failed."
    );
  }

  return {
    ...data,
    generated_image_url: data.generated_image_url
      ? `${API_BASE_URL}${data.generated_image_url}`
      : null,
  };
}

export async function getProjects() {
  const response = await fetch(
    `${API_BASE_URL}/api/projects`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load projects."
    );
  }

  return data.map((project) => ({
    ...project,
    image_url: project.image_url
      ? `${API_BASE_URL}${project.image_url}`
      : null,
    generated_image_url: project.generated_image_url
      ? `${API_BASE_URL}${project.generated_image_url}`
      : null,
  }));
}

export function downloadProjectReport(projectId) {
  const reportUrl =
    `${API_BASE_URL}/api/projects/${projectId}/report`;

  const link = document.createElement("a");

  link.href = reportUrl;
  link.download = `canopy-report-${projectId}.pdf`;

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}