# OWASP ZAP Scan Report - Day 7

## Scan Attempt

A scan was attempted for Day 7, but the local environment did not include a runnable OWASP ZAP installation or Docker engine. The following checks were performed:

- `where zap` / `where zap.bat` / `where owasp-zap` returned no executable.
- `docker version` was unavailable in the current environment.

## Findings

Because OWASP ZAP could not be executed, the scan report is not available. Instead, manual hardening was applied based on likely critical web security findings.

## Critical Fixes Implemented

- Added strict security headers to `ai-service/app.py` using Flask-Talisman and `@app.after_request`.
- Added explicit local CORS restrictions for AI service endpoints via `flask-cors`.
- Restricted backend CORS in `backend/src/main/java/com/internship/tool/controller/ContractController.java` to `http://localhost:3000`.
- Hardened the AI service API with a CSP that blocks inline scripts and external resources.

## Medium Severity Plan

1. Install OWASP ZAP locally or run the official Docker image and scan both the AI service and backend.
2. Add authentication and authorization to the AI service `/api/prompt` endpoint.
3. Enforce HTTPS and HSTS for production deployments.
4. Add automated dependency vulnerability scanning.
5. Harden CORS policy for production domains and remove wildcard origins.
