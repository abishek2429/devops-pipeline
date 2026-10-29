# 🚀 DevOps Quest

> A modern, beginner-friendly coding-challenge tracker and real-world DevOps portfolio application demonstrating an end-to-end CI/CD and DevSecOps lifecycle.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [DevOps Toolchain & Rationale](#devops-toolchain--rationale)
3. [Architecture Overview](#architecture-overview)
4. [Project Structure](#project-structure)
5. [Local Development Setup](#local-development-setup)
6. [Testing & Quality Assurance](#testing--quality-assurance)
7. [Containerization & Docker](#containerization--docker)
8. [CI/CD Pipeline Architecture](#cicd-pipeline-architecture)
9. [DevSecOps & Scanning](#devsecops--scanning)
10. [Container Registry (GHCR) & Deployment (Render)](#container-registry-ghcr--deployment-render)
11. [Troubleshooting & FAQs](#troubleshooting--faqs)
12. [Future Improvements](#future-improvements)

---

## 🎯 Project Overview

**DevOps Quest** is a mini coding-challenge tracker designed with a clean, modern, dark-themed UI. It helps learners and developers track progress on hands-on DevOps and software engineering challenges.

Beyond being a functional web application, DevOps Quest serves as a reference implementation for production-minded engineering practices:
- **Clean Architecture**: Factory pattern, Blueprints, parameterized SQLite operations.
- **Strict Security Defaults**: Debug mode disabled in production, environment variable-driven config, non-root Docker execution.
- **Robust Testing**: Comprehensive Pytest suite covering unit, route, and API integration tests.
- **Automated CI/CD**: GitHub Actions workflow covering linting, testing, Docker builds, vulnerability scans, GHCR publication, and continuous deployment.

---

## 🛠️ DevOps Toolchain & Rationale

Every tool in DevOps Quest was deliberately chosen to represent industry-standard, modern engineering without unnecessary infrastructure overhead:

| Tool | Purpose | Why We Use It |
| :--- | :--- | :--- |
| **Python & Flask** | Application Framework | Minimalist, clean, and flexible. Flask enables beginners to clearly understand request/response lifecycles, routing, and blueprints without framework magic. |
| **SQLite** | Persistence | Zero-configuration, file-based relational database. Ideal for beginner-friendly state management and containerized volumes without provisioning external database servers. |
| **Pytest** | Test Suite | The de facto standard in Python testing. Pytest provides clear assertions, modular fixtures, and easy test discovery. |
| **Ruff** | Linting & Formatting | An extremely fast Python linter and formatter written in Rust. Replaces Black, Flake8, and isort with zero-config speed. |
| **Docker & Compose** | Containerization | Packages the application and runtime into an immutable, portable artifact. Ensures consistency between local Windows 11 development and Linux deployment. |
| **Gunicorn** | Production WSGI Server | High-performance, pre-fork worker HTTP server designed for production UNIX/Linux containers, replacing the single-threaded Flask development server. |
| **GitHub Actions** | CI/CD Automation | Native GitHub workflow engine providing automated builds, test execution, security scans, and deployment triggers on branch events. |
| **Trivy** | Vulnerability Scanner | Comprehensive security scanner by Aqua Security that audits container images and application dependencies for CVEs before deployment. |
| **GHCR** | Image Registry | GitHub Container Registry stores OCI-compliant container images securely, integrated natively with GitHub access controls. |
| **SonarCloud** | Code Quality Gate | Cloud-native static code analysis (SAST) platform tracking code smells, technical debt, and test coverage metrics. |
| **Render** | Deployment Target | Fast, developer-friendly Cloud Application Platform supporting Docker web services with zero-downtime deployments and health checks. |

---

## 🏗️ Architecture Overview

DevOps Quest follows a decoupled modular design:
- **Presentation Layer**: Responsive dark-themed HTML5, CSS3 variables, and vanilla JavaScript.
- **Application Layer**: Flask application factory with modular Blueprints (`web` and `api`).
- **Data Access Layer**: SQLite database module managing safe migrations, schema initialization, and parameterized queries.
- **Operational Layer**: Gunicorn WSGI server running as an unprivileged user inside a hardened Docker container.

Detailed architectural diagrams and sequence flows can be found in [docs/architecture.md](docs/architecture.md).

---

## 📁 Project Structure

```text
devops-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD & DevSecOps pipeline
├── app/
│   ├── __init__.py                # Flask application factory
│   ├── config.py                  # Environment-driven configuration classes
│   ├── db.py                      # SQLite initialization & database helper
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py                 # REST API endpoints (/health, /api/challenges)
│   │   └── web.py                 # Dashboard and web views
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Modern dark-themed responsive CSS
│   │   └── js/
│   │       └── main.js            # Vanilla JavaScript client logic
│   └── templates/
│       ├── base.html              # Base layout template
│       ├── index.html             # Challenge dashboard template
│       ├── 404.html               # Not Found error page
│       └── 500.html               # Internal Server Error page
├── docs/
│   ├── architecture.md            # Mermaid diagrams & system architecture
│   ├── demo-guide.md              # 5-10 minute presentation guide
│   └── troubleshooting.md         # Common issues, debugging steps & fixes
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and test database setup
│   ├── test_api.py                # API & challenge functionality tests
│   └── test_routes.py             # Health check & page rendering tests
├── .dockerignore                  # Files excluded from Docker builds
├── .env.example                   # Template for local environment variables
├── .gitignore                     # Git ignore rules for Python, SQLite, IDEs
├── Dockerfile                     # Multi-stage production container definition
├── docker-compose.yml             # Local container development environment
├── pyproject.toml                 # Ruff and Pytest tool configuration
├── requirements.txt               # Pinned runtime dependencies
├── requirements-dev.txt           # Pinned development & testing dependencies
├── run.py                         # Local development execution script
└── README.md                      # Comprehensive project documentation
```

---

## 🚦 Implementation Roadmap

- [x] **Phase 1: Project Planning & Scaffolding** (Structure, README, Git rules, dependencies, config template)
- [x] **Phase 2: Application Implementation** (Flask factory, SQLite storage, dark-themed UI, tests, linting)
- [x] **Phase 3: Dockerization** (Multi-stage non-root Dockerfile, compose, persistent volumes)
- [ ] **Phase 4: Continuous Integration** (GitHub Actions workflow, Ruff, Pytest, Docker validation)
- [ ] **Phase 5: DevSecOps & Security Scanning** (Trivy CVE scans, SonarCloud quality analysis)
- [ ] **Phase 6: Container Publishing** (GitHub Container Registry publication with SHA tags)
- [ ] **Phase 7: Continuous Deployment** (Render Web Service deployment via deploy hook)
- [ ] **Phase 8: End-to-End Demo & Verification** (Failure scenario drills, presentation guide, final sign-off)

