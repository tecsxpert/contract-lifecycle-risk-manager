# Security Threats for Contract Lifecycle Risk Manager

This document summarizes five security threats relevant to the project and the AI service.

1. Exposed Secrets
   - API keys, database credentials, or other sensitive values stored in source control are at high risk.
   - Use environment variables and ensure `.env` stays out of version control.

2. Insecure Secret Storage
   - Local `.env` files can be leaked if a development machine is compromised.
   - Secrets should be kept in a secure vault or protected CI environment when possible.

3. Insufficient Authentication and Authorization
   - Unauthorized users may access services or data if token validation is weak or roles are not enforced.
   - Enforce least privilege on all API keys and service accounts.

4. Lack of Error Handling and Monitoring
   - Silent failures or missing logs make it difficult to detect attacks or outages.
   - Implement structured logging, alerting, and audit trails for suspicious API behavior.

5. Dependency and Supply Chain Risk
   - Outdated or untrusted third-party libraries can introduce vulnerabilities.
   - Keep dependencies up to date and monitor for security advisories.

## Week 1 Security Tests

- Added backend validation for empty input on contract create requests.
- Added SQL injection pattern detection for contract name and file name.
- Added prompt injection pattern detection for contract name and file name.
- Coverage includes tests for empty input, SQL keywords, and prompt injection strings in `backend/src/test/java/com/internship/tool/service/ContractSecurityTest.java`.

## Day 7 OWASP ZAP Scan

- Attempted to run OWASP ZAP but the local environment did not include the ZAP executable or Docker runtime.
- Manual code hardening was applied to the AI service and backend to address likely critical web security issues.
- Critical fixes implemented:
  - Added strict security headers in `ai-service/app.py`
  - Added explicit local CORS restrictions for both AI service and backend
  - Added content security policy and response header hardening for the AI service
- Medium severity plan:
  1. Install OWASP ZAP or run the official ZAP Docker image and scan the running AI service and backend.
  2. Validate API authentication/authorization for AI service endpoints.
  3. Enable HTTPS/HSTS in production deployment.
  4. Add dependency vulnerability scanning and regular security regression tests.
  5. Review and tighten CORS policies for production domains.
## Week 2 Security Sign-off

- JWT support is available in `backend/src/main/java/com/internship/tool/config/JwtUtil.java` and the project includes JWT configuration properties in `backend/src/main/resources/application.yml`.
- Rate limiting is enforced on the AI endpoint using `flask-limiter` at `30 requests/minute`.
- Injection protections are implemented across the stack:
  - prompt injection detection in `ai-service/app.py`
  - backend input validation for SQL and prompt injection patterns in `backend/src/main/java/com/internship/tool/service/ContractService.java`
- PII audit:
  - prompt text is sanitized before processing
  - no personal data patterns (email, phone, SSN) appear in prompt sample inputs used for tuning or testing
  - AI service prompt handling avoids storing or returning user PII in responses
- Sign-off conclusion: Week 2 security controls are documented and the core protections requested are verified in code paths and tests.
