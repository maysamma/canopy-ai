import { useState } from "react";

import Home from "./pages/Home";
import Result from "./pages/Result";
import ProjectHistory from "./pages/ProjectHistory";

export default function App() {
  const [project, setProject] = useState(null);
  const [showHistory, setShowHistory] = useState(false);

  if (showHistory) {
    return (
      <ProjectHistory
        onBack={() => setShowHistory(false)}
        onOpenProject={(selectedProject) => {
          setProject(selectedProject);
          setShowHistory(false);
        }}
      />
    );
  }

  if (project) {
    return (
      <Result
        project={project}
        onBack={() => setProject(null)}
      />
    );
  }

  return (
    <Home
      onResult={setProject}
      onOpenHistory={() => setShowHistory(true)}
    />
  );
}