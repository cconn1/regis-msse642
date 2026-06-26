# Intentional Vulnerabilities — Answer Key

Every item below is planted on purpose. Use it to verify ZAP's report.
Findings are split by **what ZAP's default scan finds on its own** vs. **what
needs manual checking** (logic/auth flaws ZAP can't reliably infer).

## ZAP auto-detects (passive or active scan)

| # | Finding | Where | ZAP rule (approx.) | OWASP 2021 |
|---|---------|-------|--------------------|------------|
| 1 | Reflected XSS | `GET /search?q=` (rendered with Jinja `|safe`) | Cross Site Scripting (Reflected) — active | A03 Injection |
| 2 | Open redirect | `GET /go?url=` and `GET /auth/login?next=` | External Redirect — active | A01 |
| 3 | Cookie missing HttpOnly | session cookie (`SESSION_COOKIE_HTTPONLY=False`) | Cookie No HttpOnly Flag — passive | A05 |
| 4 | Cookie missing SameSite | session cookie (`SESSION_COOKIE_SAMESITE=None`) | Cookie Without SameSite Attribute — passive | A05 |
| 5 | Cookie missing Secure | session cookie (`SESSION_COOKIE_SECURE=False`) | Cookie Without Secure Flag — passive | A05 |
| 6 | CSP not set | no headers added anywhere | CSP Header Not Set — passive | A05 |
| 7 | Anti-clickjacking missing | no `X-Frame-Options`/CSP frame-ancestors | Missing Anti-clickjacking Header — passive | A05 |
| 8 | MIME-sniffing | no `X-Content-Type-Options` | X-Content-Type-Options Missing — passive | A05 |
| 9 | No anti-CSRF tokens | every POST form (login, profile, ban, pay, etc.) | Absence of Anti-CSRF Tokens — passive | A01 |
| 10 | Error / stack-trace disclosure | `GET /api/risk?score=0` (and any bad input); `debug=True` | Application Error Disclosure — passive; debugger exposure | A05 |

## Manual / logic findings (verify by hand, ZAP won't flag reliably)

| # | Finding | Where | OWASP 2021 |
|---|---------|-------|------------|
| 11 | Sensitive data exposure (no auth) — dumps every user incl. **plaintext passwords** | `GET /api/users` | A01 / A02 |
| 12 | Plaintext password storage | `MEMBERS` dict in `app.py` | A02 Cryptographic Failures |
| 13 | Weak, static session secret | `app.secret_key = "dev-not-secret-123"` | A02 |
| 14 | IDOR — read/edit any member, medical, performance, payment history | `/members/<id>`, `/members/<id>/profile`, `/members/<id>/medical`, `/members/<id>/performance-notes`, `/payments/history/<id>` | A01 |
| 15 | Broken function-level access control — any logged-in user can **ban/unban** (spec: admin only) | `POST /admin/members/<id>/ban`, `/unban` | A01 |
| 16 | Broken access control — confidential **medical** data is leader/admin-only per spec, but any member can read it | `/members/<id>/medical` | A01 |
| 17 | Broken access control — leader compliance/health records editable by anyone logged in | `/leaders/<id>/compliance` | A01 |
| 18 | Privilege escalation via self-registration — `role` taken from the form | `POST /members/register` (set role=admin) | A01 |
| 19 | Weak password policy not enforced — advertised min_length 1; any non-empty password accepted; policy changeable without auth | `/security/password-policy`, `/auth/change-password`, `/members/register` | A07 |
| 20 | No brute-force protection / rate limiting / lockout on login | `POST /auth/login` | A07 |
| 21 | No old-password check on change | `POST /auth/change-password` | A07 |
| 22 | Missing screening on trip registration — banned & unpaid members register freely; no difficulty/fitness gate (spec required) | `POST /trips/<id>/register` | A04 Insecure Design |

## Endpoints that ARE enforced (so you can see contrast / true negatives)

- `@role_required("leader","admin")`: approve/reject registration, waitlist
  view & promote, attendance, unpaid report, drop-unpaid, refund.
- `@login_required` is present on member/payment routes — the bug there is
  **object-level** access control (any logged-in user, any record), not a
  missing login.

## Notes for the writeup
- The public surface (no login) already yields findings 1–13 and 19. The
  object-level access-control issues (14–17, 21) require an authenticated
  ZAP context or a manual logged-in session.
- `debug=True` is itself a Security Misconfiguration finding; in a real
  report you'd flag both the debugger and the verbose tracebacks.
