# 🔧 DevOps Quest - Troubleshooting & Diagnostics Guide

This guide covers common errors encountered during local development on Windows 11, Docker container execution, and GitHub Actions CI/CD pipeline runs, along with exact diagnostic steps and proven resolutions.

---

## 1. Local Development on Windows 11

### Issue 1.1: `docker: failed to connect to the docker API at npipe://...`
- **Symptom**: Running `docker ps` or `docker build` fails with:
  `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine... The system cannot find the file specified.`
- **Root Cause**: Docker Desktop is not running or the WSL 2 Linux backend engine has not finished initializing.
- **Resolution**:
  1. Launch Docker Desktop from the Start Menu or PowerShell:
     ```powershell
     Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
     ```
  2. Wait 30–45 seconds until the whale icon in the Windows taskbar tray shows green ("Engine running").
  3. Verify connectivity:
     ```powershell
     docker ps
     ```

### Issue 1.2: Port 5000 Already in Use
- **Symptom**: `Address already in use` or container fails to bind to port 5000.
- **Root Cause**: A background Python process or another local web server is bound to port 5000.
- **Diagnostic**:
  ```powershell
  Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object OwningProcess
  ```
- **Resolution**:
  Terminate the lingering process or map the container or local server to another port (e.g., `PORT=5001 py run.py` or `-p 5005:5000` in Docker).

### Issue 1.3: SQLite `attempt to write a readonly database` or `database is locked`
- **Root Cause**: Container running as unprivileged user `appuser` (UID 10001) cannot write to host-mounted SQLite database file due to host directory permissions.
- **Resolution**:
  Ensure the host folder or volume is owned or readable/writable by UID 10001, or use the Docker named volume defined in `docker-compose.yml`:
  ```bash
  docker compose down -v
  docker compose up --build -d
  ```

---

## 2. GitHub Actions CI/CD Pipeline Failures

### Issue 2.1: Linting or Formatting Failures in `lint-and-test`
- **Symptom**: Job `lint-and-test` fails during the `Ruff Lint Checks` step.
- **Diagnostic**: Open the workflow run, expand the `Run Ruff Lint Checks` step, and inspect the flagged files and rule codes (e.g., `E501`, `F401`, `I001`).
- **Fix**: Run Ruff locally before committing:
  ```powershell
  ruff check . --fix
  ruff format .
  ```

### Issue 2.2: Pytest Failures Blocking Deployment
- **Symptom**: `pytest` exits with code 1, immediately cancelling downstream jobs (`docker-verify`, `publish-ghcr`, `deploy-render`).
- **Diagnostic**: Inspect the Pytest traceback in the job logs. Look for assertion mismatches or unhandled exceptions.
- **Verification**: Run tests locally with full verbosity:
  ```powershell
  pytest -vv
  ```

### Issue 2.3: Trivy Scan Fails with `CRITICAL` Vulnerabilities
- **Symptom**: Job `security-scan` fails at step `Run Trivy Image Scan (Fail on CRITICAL)`.
- **Diagnostic**: Download the Trivy scan summary from the job logs to identify the CVE identifier and affected library.
- **Resolution**:
  1. If the vulnerability is in a Python dependency: upgrade the package in `requirements.txt` to a patched release.
  2. If the vulnerability is in the base OS: update the base image in `Dockerfile` (e.g., update from `python:3.13-slim-bookworm` to the latest Debian point release).
  3. Re-run scan to confirm zero unmitigated CRITICAL CVEs.

### Issue 2.4: GHCR `denied: installation not allowed to Create organization package`
- **Symptom**: Job `publish-ghcr` fails during image push to `ghcr.io`.
- **Root Cause**: The repository workflow does not have package write permissions, or GHCR package creation is disabled in repository settings.
- **Resolution**:
  1. In your GitHub repository: Navigate to **Settings** > **Actions** > **General**.
  2. Under **Workflow permissions**, ensure **Read and write permissions** is selected.
  3. Check that the workflow YAML specifies `permissions: packages: write` on the publishing job.

### Issue 2.5: Render Deploy Hook Returns HTTP 404 / 401
- **Symptom**: Job `deploy-render` reports `Render deploy hook returned unexpected status: HTTP 404`.
- **Root Cause**: The GitHub repository secret `RENDER_DEPLOY_HOOK_URL` is either missing, mistyped, or regenerated in Render.
- **Resolution**:
  1. Log in to the [Render Dashboard](https://dashboard.render.com).
  2. Open your Web Service > **Settings** > scroll to **Deploy Hook**.
  3. Copy the URL (`https://api.render.com/deploy/srv-xxxx?key=yyyy`).
  4. In GitHub: Navigate to **Settings** > **Secrets and variables** > **Actions** > add or update `RENDER_DEPLOY_HOOK_URL`.

