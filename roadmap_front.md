

# ERP AI Frontend - README

## 📌 Project Overview

This frontend is a **modern, minimalist, high-end React/TypeScript application** designed to interact with an existing ERP AI backend. It provides a clean, professional dashboard for querying the backend LLM and visualizing metrics, with a focus on **UX, responsiveness, and maintainability**.

* Technology: React 18+, TypeScript, TailwindCSS, Framer Motion
* API communication: Axios + typed endpoints
* Modular architecture for maintainability
* Fully Dockerized

---

## 🎯 Tech Stack

* **React 18+**: functional components, hooks, context API
* **TypeScript**: strict typing, interfaces for API responses
* **Vite**: fast bundler and development
* **TailwindCSS**: modern, responsive, utility-first styling
* **Framer Motion**: smooth animations
* **React Router v6**: SPA navigation
* **TanStack Query (React Query)**: API state management, caching
* **Axios**: HTTP client for backend API
* **React Markdown + Syntax Highlighting**: display GPT-like responses
* **Jest + React Testing Library**: unit and integration tests
* **ESLint + Prettier**: code quality and formatting
* **Docker**: containerized dev and production
* **Optional**: Chart.js or Recharts for embedded metrics

---

## 🏗️ Architecture

### Folder Structure

```
frontend/
├─ public/                  # Static assets
├─ src/
│  ├─ api/                  # Axios API wrapper and typed endpoints
│  │  └─ erp.ts
│  ├─ components/           # Reusable components
│  │  ├─ Sidebar.tsx
│  │  ├─ Navbar.tsx
│  │  ├─ DashboardLayout.tsx
│  │  ├─ Prompt.tsx
│  │  ├─ ChatBubble.tsx
│  │  └─ Metrics.tsx
│  ├─ hooks/                # Custom React hooks
│  │  └─ useScrollToBottom.ts
│  ├─ pages/                # Page components
│  │  ├─ PromptPage.tsx
│  │  ├─ MetricsPage.tsx
│  │  └─ HomePage.tsx
│  ├─ types/                # TypeScript interfaces
│  │  └─ api.ts
│  ├─ App.tsx               # Router and layout
│  ├─ main.tsx              # Entry point
│  └─ styles/               # Tailwind + custom styles
│     └─ globals.css
├─ package.json
├─ tsconfig.json
├─ vite.config.ts
└─ Dockerfile
```

---

## ⚡ Features

### 1. Dashboard Layout

* Sidebar for navigation: Prompt, Metrics, GitHub
* Top Navbar with optional breadcrumbs
* Responsive, mobile-first, minimal design
* Dark/light theme support (optional)

### 2. Prompt / LLM Chat

* GPT-style interface:

  * User input box
  * Display response in Markdown with formatting (tables, bold, code)
  * Smooth typing animation
  * Automatic scroll to latest response
* API integration: `/api/question`
* Handles sources and references returned by backend

### 3. Metrics

* Display backend metrics (Prometheus/Grafana)
* Optional: embedded iframe or charts with Recharts/Chart.js
* Responsive, clean, interactive visuals

### 4. UX / UI High-End

* Smooth animations using Framer Motion
* Minimalist, professional, modern styling
* Feedback on loading and API errors
* Modular and reusable components for scalability

---

## 🛠️ Best Practices

* **TypeScript strict mode** for all components and API responses
* **Custom hooks** for reusable logic
* **Separation of concerns**: pages vs components vs hooks
* **API layer**: central axios instance with error handling and typed responses
* **React Query** for caching and automatic state updates
* **Tailwind utility classes** + component variants for modular styling
* **Accessibility**: keyboard navigation, aria labels
* **Unit tests**: Jest + React Testing Library
* **Dockerization**: single-stage dev build, multi-stage prod build

---

## 🗺️ Frontend Roadmap

### Phase 1 – Setup & MVP

* React + TypeScript + Vite project
* TailwindCSS setup
* Sidebar + Navbar + DashboardLayout
* Prompt page with API call and response display
* Metrics page with placeholder charts or iframe

### Phase 2 – UX Enhancements

* Smooth typing animation for LLM responses
* Markdown rendering for tables and formatting
* Scroll to bottom for new messages
* Error handling and loading states
* Responsive design

### Phase 3 – Optimization & Testing

* React Query caching for API requests
* Lazy loading pages/components
* Unit and integration tests
* Dockerfile production-ready
* Optional: dark/light mode toggle

### Phase 4 – Polish & Production

* Framer Motion animations for prompt bubbles
* GitHub link in sidebar
* Embed Grafana metrics dynamically
* CI/CD pipeline with Docker build & push

---

## 👤 Recommended Frontend Profile

* Senior React/TypeScript developer
* Experience in **high-end UX/UI design**
* Knowledge of **TailwindCSS & Framer Motion**
* Familiarity with **API integration with backend**, async requests
* Strong TypeScript skills, modular architecture
* Experience with **Dockerized frontend deployment**
* Ability to write **testable, maintainable, production-ready code**

---

## 🚀 Docker Setup (Frontend)

**Dockerfile (example)**

```dockerfile
# Stage 1: build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

# Stage 2: serve
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml snippet**

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - VITE_API_URL=http://backend:8000/api
```

---

This README provides **everything needed to implement the frontend**: structure, tech stack, features, best practices, roadmap, and production deployment.

