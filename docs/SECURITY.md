# Security Hardening Guide

This guide lists the security controls implemented and recommendations.

Implemented controls
- Secure HTTP headers via middleware (X-Frame-Options, X-Content-Type-Options, Referrer-Policy)
- CORS configured to allow specific origins (configurable via .env)
- Rate limiting middleware to protect against API abuse
- GZip compression disabled for small responses, enabled for larger
- Secrets loaded via .env and not committed

Recommendations
- Use HTTPS termination (TLS) at reverse proxy (nginx / load balancer)
- Add authentication and JWT signing keys stored in secrets manager
- Enable WAF and DDoS protection on public endpoints
- Use a proper rate-limiter backed by Redis for multi-instance deployments
- Sanitize all inputs at model boundaries; use JSON schema validation for API payloads
