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
