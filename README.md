# 🌳 Canopy AI

<p align="center">
  <strong>AI-powered Urban Improvement Assistant</strong><br>
  Transform urban images into actionable sustainability insights using AI.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-61DAFB?logo=react)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange)
![License](https://img.shields.io/badge/License-Educational-success)

</p>

---

# 📖 Overview

**Canopy AI** is an AI-powered platform that analyzes urban environments from a single image.

The system combines computer vision, AI reasoning, and urban planning principles to evaluate streets, neighborhoods, parks, and public spaces.

Users simply upload an image and receive:

- Urban scene analysis
- Sustainability indicators
- AI-generated recommendations
- Professional PDF report
- AI visualization prompt for urban improvement

Canopy AI is designed as an early-stage decision support tool for municipalities, architects, urban planners, researchers, and students.

---

# ❗ Problem Statement

Evaluating urban environments traditionally requires:

- Field inspections
- GIS tools
- Expert analysis
- Manual documentation
- Long review cycles

These processes are expensive and time-consuming.

Canopy AI accelerates the first stage of urban assessment by providing AI-generated indicators from a single image in seconds.

> **Disclaimer**
>
> Canopy AI provides preliminary AI-generated urban indicators. The results are intended to support early-stage planning and should not replace engineering, architectural, or municipal review.

---

# ✨ Features

- Upload urban images
- AI-powered scene understanding
- Urban sustainability assessment
- Green Coverage estimation
- Walkability evaluation
- Shade assessment
- Solar Potential estimation
- Heat Risk estimation
- Automatic issue detection
- Practical urban recommendations
- AI visualization prompt generation
- Professional PDF report generation
- Project history
- SQLite persistence

---

# 🤖 AI Workflow

```text
Upload Image
      │
      ▼
Vision Agent
      │
      ▼
Urban Assessment
      │
      ▼
Recommendation Engine
      │
      ▼
Visualization Prompt
      │
      ▼
Image Generation
      │
      ▼
Professional PDF Report
```

---

# 🏗 Multi-Agent Architecture

```text
                 User
                   │
                   ▼
            React Frontend
                   │
                   ▼
             FastAPI Backend
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 Vision Agent  Planner Agent  Report Agent
                   │
                   ▼
        Visualization Agent
```

---

# 📊 Analysis Output

Each project includes:

- Scene Type
- Trees
- Buildings
- Roads
- Sidewalks
- Vehicles
- Empty Spaces
- Shade

Urban indicators:

- Green Coverage
- Walkability
- Shade
- Solar Potential
- Heat Risk

AI-generated:

- Summary
- Current Issues
- Recommendations
- Expected Impact
- Visualization Prompt

---

# 📄 PDF Report

The generated report includes:

- Cover page
- Overall Urban Score
- Executive Summary
- Original Image
- Assessment Scores
- Current Issues
- Recommendations
- Assessment Notes

---

# 🖼 Screenshots

## Home

![Home](assets/home.png)

## Analysis Results

![Results](assets/result.png)

## Project History

![History](assets/history.png)

## PDF Report

![Report Cover](assets/report1.png)

![Report Assessment & Recommendations ](assets/report2.png)
```

---

# 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | React + Vite |
| Backend | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| AI Vision | Google Gemini |
| Image Processing | Pillow |
| Reports | ReportLab |
| API | REST |

---

# 📂 Project Structure

```text
canopy-ai/

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
│   └── canopy.db
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│
└── README.md
```

---

# 🚀 Installation

## Clone

```bash
git clone https://github.com/maysamma/canopy-ai.git

cd canopy-ai
```

---

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# ⚙ Environment Variables

Create:

```text
backend/.env
```

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY

GEMINI_MODEL=gemini-2.5-flash

GEMINI_IMAGE_MODEL=gemini-3.1-flash-image
```

---

# 📡 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/projects` | Create project |
| GET | `/api/projects` | List projects |
| GET | `/api/projects/{id}` | Get project |
| POST | `/api/projects/{id}/visualization` | Generate visualization |
| GET | `/api/projects/{id}/report` | Download PDF |

---

# 🗺 Roadmap

- ✅ Urban image upload
- ✅ AI analysis
- ✅ Recommendation engine
- ✅ Professional PDF reports
- ✅ SQLite project history
- ✅ Improved visualization prompt
- ⏳ Better image generation provider
- ⏳ Cloud deployment
- ⏳ User authentication
- ⏳ Analytics dashboard

---

# 🔮 Future Improvements

- Support additional image-generation providers
- GIS integration
- Interactive dashboards
- Multi-language reports
- Cost estimation for improvements
- Compare multiple projects
- Street-level analytics
- Cloud deployment

---

# 👤 Author

**Maysam Abduljalil**

GitHub:
https://github.com/maysamma

---

© 2026 Canopy AI