# 🚀 DevOps Quest

> A modern, beginner-friendly coding-challenge tracker and real-world DevOps portfolio application demonstrating an end-to-end CI/CD and DevSecOps lifecycle.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [DevOps Toolchain & Rationale](#devops-toolchain--rationale)
3. [Architecture Overview](#architecture-overview)
4. [Project Structure](#project-structure)
5. [Local Development Setup (Windows 11)](#local-development-setup-windows-11)
6. [Testing & Quality Assurance](#testing--quality-assurance)
7. [Containerization & Docker](#containerization--docker)
8. [CI/CD & DevSecOps Pipeline](#cicd--devsecops-pipeline)
9. [Vulnerability Scanning & Code Quality](#vulnerability-scanning--code-quality)
10. [Container Registry (GHCR) & Cloud Deployment (Render)](#container-registry-ghcr--cloud-deployment-render)
11. [Demonstration & Failure Scenarios](#demonstration--failure-scenarios)
12. [Troubleshooting & FAQs](#troubleshooting--faqs)
13. [Future Improvements](#future-improvements)

---

## 🎯 Project Overview

**DevOps Quest** is a mini coding-challenge tracker designed with a clean, modern, dark-themed UI. It helps learners and developers track progress on hands-on DevOps and software engineering challenges.

Beyond being a functional web application, DevOps Quest serves as a reference implementation for production-minded engineering practices:
- **Clean Architecture**: Factory pattern, Blueprints, parameterized SQLite operations.
- **Strict Security Defaults**: Debug mode disabled in production, environment variable-driven config, non-root Docker execution (`appuser:10001`).
- **Robust Testing**: Comprehensive Pytest suite covering unit, route, and API integration tests.
- **Automated CI/CD**: GitHub Actions workflow covering linting, testing, Docker builds, vulnerability scans, GHCR publication, and continuous deployment.

---

## 🛠️ DevOps Toolchain & Rationale

Every tool in DevOps Quest was deliberately chosen to represent industry-standard, modern engineering without unnecessary infrastructure overhead:

| Tool | Purpose | Why We Use It |
| :--- | :--- | :--- |
| **Python 3.13 & Flask** | Application Framework | Minimalist, clean, and flexible. Flask enables beginners to clearly understand request/response lifecycles, routing, and blueprints without framework magic. |
| **SQLite** | Persistence | Zero-configuration, file-based relational database. Ideal for beginner-friendly state management and containerized volumes without provisioning external database servers. |
| **Pytest** | Test Suite | The de facto standard in Python testing. Pytest provides clear assertions, modular fixtures, and easy test discovery. |
| **Ruff** | Linting & Formatting | An extremely fast Python linter and formatter written in Rust. Replaces Black, Flake8, and isort with zero-config speed. |
| **Docker & Compose** | Containerization | Packages the application and runtime into an immutable, portable artifact. Ensures consistency between local Windows 11 development and Linux deployment. |
| **Gunicorn** | Production WSGI Server | High-performance, pre-fork worker HTTP server designed for production UNIX/Linux containers, replacing the single-threaded Flask development server. |
| **GitHub Actions** | CI/CD Automation | Native GitHub workflow engine providing automated builds, test execution, security scans, and deployment triggers on branch events. |
| **Aqua Trivy** | Vulnerability Scanner | Comprehensive security scanner by Aqua Security that audits container images and application dependencies for CVEs before deployment. |
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
│       └── ci.yml                 # CI/CD, DevSecOps, GHCR & Render deployment pipeline
├── app/
│   ├── __init__.py                # Flask application factory (create_app)
│   ├── config.py                  # Environment-driven configuration classes
│   ├── db.py                      # Parameterized SQLite setup, schema initialization & seed data
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py                 # REST API endpoints (/health, /api/challenges, /api/challenges/<id>/toggle)
│   │   └── web.py                 # UI dashboard view and challenge interaction
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Modern dark-themed CSS with accessible contrast and progress bar
│   │   └── js/
│   │       └── main.js            # Vanilla JS for async challenge toggling & DOM updates
│   └── templates/
│       ├── base.html              # Accessible HTML5 shell with header and footer
│       ├── index.html             # Challenge tracker dashboard & progress metrics
│       ├── 404.html               # User-friendly Not Found error page
│       └── 500.html               # User-friendly Server Error page
├── docs/
│   ├── architecture.md            # Mermaid diagrams & system architecture
│   ├── demo-guide.md              # 5-10 minute presentation guide for portfolio
│   └── troubleshooting.md         # Common issues, debugging steps & fixes
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and isolated temporary SQLite database
│   ├── test_api.py                # REST API tests (status codes, JSON schema, toggling)
│   └── test_routes.py             # Route tests (health check, dashboard rendering, 404 handling)
├── .dockerignore                  # Files excluded from Docker builds
├── .env.example                   # Template for local environment variables
├── .gitignore                     # Git ignore rules for Python, SQLite, IDEs
├── Dockerfile                     # Multi-stage production container definition
├── docker-compose.yml             # Local container development environment
├── pyproject.toml                 # Ruff and Pytest tool configuration
├── requirements.txt               # Pinned runtime dependencies
├── requirements-dev.txt           # Pinned development & testing dependencies
├── run.py                         # Local development execution script
├── sonar-project.properties       # Optional SonarCloud code quality configuration
└── README.md                      # Comprehensive project documentation
```

---

## 🚦 Implementation Roadmap

- [x] **Phase 1: Project Planning & Scaffolding** (Structure, README, Git rules, dependencies, config template)
- [x] **Phase 2: Application Implementation** (Flask factory, SQLite storage, dark-themed UI, tests, linting)
- [x] **Phase 3: Dockerization** (Multi-stage non-root Dockerfile, compose, persistent volumes)
- [x] **Phase 4: Continuous Integration** (GitHub Actions workflow, Ruff, Pytest, Docker validation)
- [x] **Phase 5: DevSecOps & Security Scanning** (Trivy CVE scans, SonarCloud quality analysis)
- [x] **Phase 6: Container Publishing** (GitHub Container Registry publication with SHA tags)
- [x] **Phase 7: Continuous Deployment** (Render Web Service deployment via deploy hook)
- [x] **Phase 8: End-to-End Demo & Verification** (Failure scenario drills, presentation guide, final sign-off)

---

## 💻 Local Development Setup (Windows 11)

### 1. Prerequisites
- **Python 3.11 – 3.13** (Verify with `py --version`)
- **Docker Desktop with WSL 2 backend** (Verify with `docker --version`)
- **Git**

### 2. Setup Virtual Environment
```powershell
# Create an isolated virtual environment
py -3 -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install pinned runtime & development dependencies
pip install -r requirements-dev.txt
```

### 3. Configure Environment Variables
```powershell
Copy-Item .env.example .env
```

### 4. Run the Development Server
```powershell
py run.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser:
- **Dashboard:** `http://127.0.0.1:5000/`
- **Health Check:** `http://127.0.0.1:5000/health`
- **REST API:** `http://127.0.0.1:5000/api/challenges`

---

## 🧪 Testing & Quality Assurance

### Run Ruff Linter & Formatter
```powershell
ruff check .
ruff format --check .
```

### Run Pytest Test Suite
```powershell
pytest --cov=app --cov-report=term-missing
```

---

## 🐳 Containerization & Docker

### Local Container Build
```powershell
docker build -t devops-quest:local .
```

### Run with Docker Compose (Persistent Storage)
```powershell
docker compose up --build -d
```
Inspect logs:
```powershell
docker compose logs -f
```
Stop the container:
```powershell
docker compose down
```

---

## 🔄 CI/CD & DevSecOps Pipeline

The GitHub Actions workflow in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) automates 6 continuous delivery stages:

1. **`lint-and-test`**: Executes Ruff linting and runs all 19 Pytest tests.
2. **`docker-verify`**: Compiles the multi-stage Docker image and executes a container boot test with a `/health` probe.
3. **`security-scan`**: Scans the image using **Aqua Trivy**; automatically fails if unmitigated `CRITICAL` vulnerabilities exist.
4. **`sonarcloud`** *(Optional)*: Runs static code analysis if `SONAR_TOKEN` is configured.
5. **`publish-ghcr`**: Authenticates via `GITHUB_TOKEN`, tags the image with `sha-<commit>`, `main`, and `latest`, and pushes to **GHCR** (`ghcr.io`). Runs strictly on pushes to `main`.
6. **`deploy-render`**: Calls the secure Render deploy hook to trigger automated zero-downtime deployment.

---

## 🔐 Required Secrets Configuration

To enable automated container publishing and deployment on GitHub:

| Secret Name | Required / Optional | Description |
| :--- | :---: | :--- |
| `RENDER_DEPLOY_HOOK_URL` | **Required for CD** | Webhook URL from Render Web Service Settings. |
| `SONAR_TOKEN` | Optional | API token from SonarCloud account security settings. |
| `GITHUB_TOKEN` | *Automatic* | Built-in GitHub token for GHCR publishing (`packages: write`). |

---

## 🎤 Demonstration & Failure Scenarios

Full step-by-step presentation scripts and instructions for demonstrating pipeline failure blocking can be found in [docs/demo-guide.md](docs/demo-guide.md):
- **Scenario 1:** Happy path passing change.
- **Scenario 2:** Intentionally failing Pytest test blocks deployment.
- **Scenario 3:** Trivy security scan blocks vulnerable artifacts.

---

## 🔧 Troubleshooting & FAQs

Refer to [docs/troubleshooting.md](docs/troubleshooting.md) for detailed diagnostics on:
- Docker Desktop named pipe connection issues on Windows.
- Port binding conflicts.
- SQLite permissions in containers.
- GitHub Actions secret troubleshooting.

---

## 🌟 Future Improvements

1. **Multi-Architecture Builds:** Build `linux/amd64` and `linux/arm64` container images via Docker Buildx.
2. **Hosted Database:** Transition from SQLite to managed PostgreSQL when scaling horizontally.
3. **Automated Rollbacks:** Implement canary deployments with automatic rollback if post-deploy health checks fail.
