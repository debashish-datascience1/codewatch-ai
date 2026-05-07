# OWASP Top 10 (2021) — Security Vulnerability Reference

## A01: Broken Access Control
**CWE IDs:** CWE-22, CWE-284, CWE-285, CWE-639, CWE-732

Access control enforces policies so users cannot act outside their intended permissions.
Failures lead to unauthorized information disclosure, modification, or destruction of data.

**Patterns to detect:**
- Direct object references using user-supplied IDs without authorization checks
- Missing function-level access control (no role/permission check before sensitive operations)
- Path traversal: `../` sequences in file path parameters
- CORS misconfiguration allowing all origins
- Force browsing to authenticated pages without session validation

**Example vulnerable code (Python):**
```python
def get_user_data(user_id):
    # No check that the requester owns this user_id
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")
```

**Fix:** Always verify that the authenticated user is authorized to access the requested resource.

---

## A02: Cryptographic Failures
**CWE IDs:** CWE-259, CWE-327, CWE-328, CWE-330

Failures related to cryptography (or lack thereof) that expose sensitive data.

**Patterns to detect:**
- Hardcoded passwords or secrets in source code
- Use of weak/broken algorithms: MD5, SHA1, DES, RC4
- Use of `random` instead of `secrets` for security-sensitive values
- Passwords stored as plain text or with reversible encryption
- Missing HTTPS / TLS for data in transit
- Weak key sizes (RSA < 2048 bits)

**Example vulnerable code (Python):**
```python
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # MD5 is broken for passwords
```

**Fix:** Use bcrypt, argon2, or scrypt for password hashing. Use `secrets` module for tokens.

---

## A03: Injection
**CWE IDs:** CWE-89 (SQL), CWE-78 (OS Command), CWE-79 (XSS), CWE-917 (Expression Language)

Injection flaws occur when untrusted data is sent to an interpreter as part of a command or query.

**SQL Injection patterns:**
- String concatenation into SQL: `"SELECT * FROM users WHERE name = '" + username + "'"`
- f-string or `.format()` used to build SQL queries
- Missing parameterized queries / prepared statements

**OS Command Injection patterns:**
- `os.system()`, `subprocess.call(shell=True)` with user input
- `eval()` or `exec()` with user-controlled strings

**XSS patterns:**
- Rendering user input directly into HTML without escaping
- `innerHTML =` with unsanitized data

**Example vulnerable code (Python):**
```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)

os.system("ping " + user_input)  # command injection
```

**Fix:** Use parameterized queries, prepared statements, and subprocess with list arguments.

---

## A04: Insecure Design
**CWE IDs:** CWE-73, CWE-183, CWE-209, CWE-657

Design flaws that cannot be fixed by correct implementation alone.

**Patterns to detect:**
- No rate limiting on authentication endpoints
- Security questions with guessable answers
- Business logic flaws (e.g., negative price values accepted)
- Missing input validation at the design level
- Error messages exposing stack traces or internal details

---

## A05: Security Misconfiguration
**CWE IDs:** CWE-16, CWE-611, CWE-732

**Patterns to detect:**
- `DEBUG = True` in production configuration
- Default credentials not changed
- Unnecessary features/services enabled
- Missing security headers (X-Frame-Options, CSP, HSTS)
- XML External Entity (XXE) processing enabled
- Directory listing enabled on web server

**Example vulnerable code (Python/Django):**
```python
DEBUG = True           # must be False in production
SECRET_KEY = "dev"     # hardcoded weak secret key
ALLOWED_HOSTS = ["*"]  # too permissive
```

---

## A06: Vulnerable and Outdated Components
**CWE IDs:** CWE-1035, CWE-937

**Patterns to detect:**
- `requirements.txt` pinning very old library versions
- Known vulnerable packages (e.g., old versions of requests, flask, django)
- No dependency scanning in CI/CD pipeline
- Use of deprecated/unmaintained libraries

---

## A07: Identification and Authentication Failures
**CWE IDs:** CWE-255, CWE-287, CWE-306, CWE-307, CWE-384, CWE-798

**Patterns to detect:**
- No account lockout / brute-force protection
- Weak or guessable session token generation
- Session tokens in URLs (exposed in logs/referrer)
- Missing multi-factor authentication on privileged actions
- Insecure "remember me" functionality
- Hardcoded credentials in code: `password = "admin123"`
- JWT with `alg: none` or weak secret

**Example vulnerable code:**
```python
SECRET_KEY = "password123"           # hardcoded weak JWT secret
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

---

## A08: Software and Data Integrity Failures
**CWE IDs:** CWE-345, CWE-353, CWE-426, CWE-494, CWE-502, CWE-915

**Patterns to detect:**
- Deserializing untrusted data with `pickle.loads()`, `yaml.load()` (without SafeLoader)
- Auto-update mechanisms without integrity verification
- Unsigned code or unsigned scripts being executed

**Example vulnerable code (Python):**
```python
import pickle
data = pickle.loads(user_supplied_bytes)   # arbitrary code execution risk

import yaml
config = yaml.load(user_input)             # use yaml.safe_load instead
```

---

## A09: Security Logging and Monitoring Failures
**CWE IDs:** CWE-117, CWE-223, CWE-532, CWE-778

**Patterns to detect:**
- No logging of authentication events (login, logout, failures)
- Sensitive data (passwords, tokens, PII) logged in plain text
- Log injection: unsanitized user input written directly to logs
- No alerting on repeated failures

**Example vulnerable code:**
```python
logging.info(f"User login attempt: {username} password: {password}")  # logs password
logging.info(user_input)   # log injection if user_input contains newlines
```

---

## A10: Server-Side Request Forgery (SSRF)
**CWE IDs:** CWE-918

SSRF flaws occur when a web application fetches a remote resource using a user-supplied URL
without sufficient validation, allowing attackers to access internal services.

**Patterns to detect:**
- `requests.get(user_supplied_url)` without allowlist validation
- URL redirect targets not validated
- Fetching files from user-controlled paths

**Example vulnerable code (Python):**
```python
url = request.args.get("url")
response = requests.get(url)   # SSRF — attacker can target http://169.254.169.254/
```

**Fix:** Validate URLs against an allowlist of approved domains/IP ranges. Block internal IP ranges.
