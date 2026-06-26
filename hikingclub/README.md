# Georgia Hiking Club — Local Pen-Test Target

A deliberately vulnerable Flask app for practicing with **OWASP ZAP**.
Self-contained, in-memory, **local-only**. Payments are mocked — nothing is
ever charged. Do not expose this to a network.

## Run

```bash
pip install flask
python app.py
# http://127.0.0.1:5000
```

Data resets every restart (it lives in memory).

## Lab accounts

| email             | password | role   |
|-------------------|----------|--------|
| admin@ghc.test    | admin    | admin  |
| leader@ghc.test   | leader   | leader |
| sam@ghc.test      | password | member |
| quinn@ghc.test    | 123      | member |
| pat@ghc.test      | hunter2  | member (banned) |

## Pointing ZAP at it

1. ZAP → **Automated Scan** → URL `http://127.0.0.1:5000` → **Attack**.
   The spider crawls the nav links/forms, then the active scanner fires
   payloads. This alone surfaces the unauthenticated findings (XSS, open
   redirect, error disclosure, missing headers, cookie flags, leaky API).
2. To reach the **access-control** findings behind login, set up a ZAP
   Context with form-based authentication (login at `/auth/login`,
   logged-out indicator = the text `Member Login`), or just proxy your
   browser through ZAP, log in manually, then spider/active-scan.

See `SECURITY_NOTES.md` for the full list of what's planted and where —
that's your answer key to check ZAP's report against.
