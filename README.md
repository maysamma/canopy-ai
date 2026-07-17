# 🌿 Canopy AI

> **AI-powered Urban Improvement Assistant**

Canopy AI is an AI-powered platform that helps evaluate streets and urban spaces from a single image.

The system analyzes the uploaded scene using multimodal AI, identifies urban characteristics, estimates sustainability indicators, and provides practical recommendations for improving green infrastructure, pedestrian experience, shade, and overall urban quality.

In addition to the analysis, Canopy AI can generate an improved visualization of the same location and produce a professional PDF report summarizing the results.

---

## 🎯 Problem Statement

Urban planners, municipalities, architects, and researchers often need a quick way to evaluate existing streets and public spaces.

Traditional assessments usually require:
- Manual field inspections
- Multiple software tools
- Time-consuming documentation
- Expert interpretation

This makes early-stage urban evaluation slower and more expensive.

Canopy AI provides an AI-assisted preliminary assessment from a single image, helping users identify improvement opportunities within seconds.

> **Disclaimer:**  
> Canopy AI provides preliminary AI-generated urban indicators. The results are intended to support early-stage decision-making and should not be considered engineering measurements, architectural approval, or municipal approval.
---

# ✨ Key Features

- 📷 Upload a street or neighborhood image.
- 🤖 AI-powered urban scene analysis using Gemini Vision.
- 🌳 Estimate Green Coverage.
- 🚶 Evaluate Walkability.
- 🌤️ Assess Shade Availability.
- ☀️ Estimate Solar Potential.
- 🌡️ Assess Heat Risk.
- 📋 Detect urban issues automatically.
- 💡 Generate practical urban improvement recommendations.
- 🎨 Generate an AI-enhanced visualization of the same location.
- 📄 Export a professional PDF report.
- 🗂️ Store projects permanently using SQLite.
- 📚 Browse previous analyses through Project History.

---

# 🏗️ System Architecture

```
                User
                  │
                  ▼
        React + Vite Frontend
                  │
                  ▼
           FastAPI Backend
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
Vision AI     SQLite DB    PDF Generator
     │                         │
     ▼                         ▼
Urban Analysis          Professional Report
     │
     ▼
Visualization Generator
```

---

# 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite |
| Backend | FastAPI |
| Database | SQLite + SQLAlchemy |
| Vision AI | Google Gemini Vision |
| Image Generation | Google Gemini Image Model |
| PDF Reports | ReportLab |
| Image Processing | Pillow |
| API Testing | Swagger UI |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
canopy-ai-starter/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── uploads/
│   ├── generated/
│   ├── reports/
│   ├── canopy.db
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── index.html
│
└── README.md
```

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/maysamma/canopy-ai-lite.git
cd canopy-ai-lite
```

---

## Backend Setup

```powershell
cd backend

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Run the backend:

```powershell
uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

Open a second terminal.

```powershell
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

## Environment Variables

Create a `.env` file inside the `backend` folder.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_IMAGE_MODEL=gemini-3.1-flash-image
```

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Check API health status |
| `POST` | `/api/projects` | Upload an image and create a new analysis project |
| `GET` | `/api/projects` | Retrieve all saved projects |
| `GET` | `/api/projects/{project_id}` | Retrieve a specific project |
| `POST` | `/api/projects/{project_id}/visualization` | Generate an improved urban visualization |
| `GET` | `/api/projects/{project_id}/report` | Download the PDF report |

---

# 📊 Analysis Output

Each analysis includes:

- 🌳 Green Coverage
- 🚶 Walkability
- 🌤️ Shade
- ☀️ Solar Potential
- 🌡️ Heat Risk
- 🏙️ Detected Urban Scene
- ⚠️ Current Issues
- 💡 Recommendations
- 📈 Expected Impact
- 📝 AI-generated Summary

---

# 📸 Screenshots

## Home Page

> Upload a street or neighborhood image for AI analysis.

![Home](docs/screenshots/home.png)

---

## Analysis Results

> View sustainability indicators, detected issues, recommendations, and AI-generated insights.

![Results](docs/screenshots/results.png)

---

## Project History

> Browse previously analyzed projects and reopen them instantly.

![History](docs/screenshots/history.png)

---

## PDF Report

> Download a professional urban assessment report in PDF format.

![PDF Report](docs/screenshots/report.png)

---

# 🚀 Future Work

The current version demonstrates the core capabilities of Canopy AI. Future improvements include:

- Support additional AI vision providers.
- Improve image-to-image urban visualization quality.
- Add GIS and map integration.
- Generate interactive dashboards.
- Export reports in multiple formats.
- Support multilingual reports.
- Improve urban scoring using computer vision models.
- Add authentication and user accounts.
- Deploy the application to the cloud.

---

# 👥 Team

**Canopy AI** was developed as an AI-powered urban analysis platform for hackathon and educational purposes.

Main responsibilities included:

- AI Integration
- Backend Development
- Frontend Development
- Database Design
- PDF Report Generation
- Urban Analysis Pipeline

---

# 📄 License

This project is released for educational and demonstration purposes.

© 2026 Canopy AI