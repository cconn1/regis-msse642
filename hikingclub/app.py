"""
Georgia Hiking Club (GHC) — deliberately vulnerable demo app.

PURPOSE: a self-contained, LOCAL-ONLY practice target for OWASP ZAP.
Do NOT deploy this anywhere reachable. Every weakness here is intentional
and catalogued in SECURITY_NOTES.md. Payments are mocked — no money moves.

Run:
    pip install flask
    python app.py
    # open http://127.0.0.1:5000
"""

from functools import wraps

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)

# VULN (weak secret): static, guessable signing key for the session cookie.
app.secret_key = "dev-not-secret-123"

# VULN (insecure cookie flags): session cookie is readable by JavaScript,
# carries no SameSite attribute, and is not marked Secure.
app.config.update(
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE=None,
)


# ---------------------------------------------------------------------------
# In-memory "database". Plaintext passwords are themselves a finding, and are
# exposed wholesale by /api/users below.
# ---------------------------------------------------------------------------
MEMBERS: dict[int, dict] = {
    1: {
        "id": 1, "name": "Avery Admin", "email": "admin@ghc.test",
        "password": "admin", "role": "admin", "banned": False,
        "medical": "None on file.",
        "performance": ["Completed D5 routes; strong endurance."],
        "dues_paid": True,
    },
    2: {
        "id": 2, "name": "Logan Leader", "email": "leader@ghc.test",
        "password": "leader", "role": "leader", "banned": False,
        "medical": "Mild asthma; carries inhaler.",
        "performance": ["Certified leader; paces D2-D4 groups well."],
        "dues_paid": True,
    },
    3: {
        "id": 3, "name": "Riley Ridge", "email": "riley@ghc.test",
        "password": "leader", "role": "leader", "banned": False,
        "medical": "None on file.",
        "performance": ["Leads water/paddle trips."],
        "dues_paid": True,
    },
    4: {
        "id": 4, "name": "Sam Summit", "email": "sam@ghc.test",
        "password": "password", "role": "member", "banned": False,
        "medical": "Type 1 diabetic; carries glucose tabs.",
        "performance": ["No-show on 2 of last 4 trips."],
        "dues_paid": True,
    },
    5: {
        "id": 5, "name": "Quinn Quartz", "email": "quinn@ghc.test",
        "password": "123", "role": "member", "banned": False,
        "medical": "Recovering from ankle sprain.",
        "performance": ["DNF on last D4."],
        "dues_paid": False,
    },
    6: {
        "id": 6, "name": "Pat Pebble", "email": "pat@ghc.test",
        "password": "hunter2", "role": "member", "banned": True,
        "medical": "None on file.",
        "performance": ["Banned: repeated policy violations."],
        "dues_paid": False,
    },
}


def _next_member_id() -> int:
    return max(MEMBERS) + 1 if MEMBERS else 1


# ---------------------------------------------------------------------------
# Trips. Display fields drive the homepage cards; the rest drive the logic.
# ---------------------------------------------------------------------------
TRIPS: dict[int, dict] = {
    1: {
        "id": 1, "month": "JUN", "day": "04", "time": "10:00 AM",
        "title": "HIKE: THURSDAY MORNING SEMI-FITNESS AT VICKERY CREEK",
        "status": "EVENT STARTED", "status_class": "status-live",
        "difficulty": "D2", "type": "local", "price": 0, "leader_id": 2,
        "capacity_min": 4, "capacity_max": 15,
        "description": "A brisk morning fitness hike with varied terrain and creek views.",
        "location": "Vickery Creek - Grooveway Park Entrance",
        "registrations": [4, 5], "waitlist": [], "attendance": {}, "paid": [],
    },
    2: {
        "id": 2, "month": "JUN", "day": "05", "time": "12:30 PM",
        "title": "HIKE: YONAH PRESERVE PLUS YONAH MOUNTAIN",
        "status": "GET ON THE WAITING LIST", "status_class": "status-wait",
        "difficulty": "D4", "type": "local", "price": 0, "leader_id": 2,
        "capacity_min": 4, "capacity_max": 11,
        "description": "A challenging mountain route with sustained elevation gain.",
        "location": "Yonah Preserve / Yonah Mountain",
        "registrations": [4], "waitlist": [5], "attendance": {}, "paid": [],
    },
    3: {
        "id": 3, "month": "JUN", "day": "06", "time": "8:00 AM",
        "title": "HIKE: KMNBP KOLB FARM LOOP",
        "status": "REGISTER NOW", "status_class": "status-open",
        "difficulty": "D2", "type": "local", "price": 0, "leader_id": 3,
        "capacity_min": 4, "capacity_max": 15,
        "description": "A moderate loop with rolling hills and wooded sections.",
        "location": "Kennesaw Mountain National Battlefield Park",
        "registrations": [], "waitlist": [], "attendance": {}, "paid": [],
    },
    5: {
        "id": 5, "month": "JUN", "day": "07", "time": "9:00 AM",
        "title": "WATER: EASY PADDLE AT HOLLIS Q LATHAM RESERVOIR",
        "status": "REGISTER NOW", "status_class": "status-open",
        "difficulty": "D3", "type": "local", "price": 0, "leader_id": 3,
        "capacity_min": 2, "capacity_max": 8,
        "description": "Relaxed paddle on calm water with a gear check at launch.",
        "location": "Hollis Q. Latham Reservoir",
        "registrations": [], "waitlist": [], "attendance": {}, "paid": [],
    },
    7: {
        "id": 7, "month": "JUN", "day": "09", "time": "6:05 PM",
        "title": "INDOOR CLIMB: INDOOR CLIMBING @ CRA",
        "status": "REGISTER NOW", "status_class": "status-open",
        "difficulty": "PAID D4", "type": "excursion", "price": 25, "leader_id": 2,
        "capacity_min": 1, "capacity_max": 8,
        "description": "Evening indoor climbing with belay support and orientation.",
        "location": "CRA Climbing Gym",
        "registrations": [], "waitlist": [], "attendance": {}, "paid": [],
    },
    8: {
        "id": 8, "month": "JUN", "day": "10", "time": "10:00 AM",
        "title": "HIKE: CLOUDLAND CANYON WITH A NEW ROUTE",
        "status": "GET ON THE WAITING LIST", "status_class": "status-wait",
        "difficulty": "D5", "type": "excursion", "price": 60, "leader_id": 2,
        "capacity_min": 4, "capacity_max": 12,
        "description": "Advanced canyon hike with steep sections and scenic overlooks.",
        "location": "Cloudland Canyon State Park",
        "registrations": [4], "waitlist": [], "attendance": {}, "paid": [4],
    },
}


def _spots(trip: dict) -> str:
    filled = len(trip["registrations"])
    waiting = len(trip["waitlist"])
    base = f"{filled} of {trip['capacity_max']} spots filled"
    return base + (f", {waiting} waiting" if waiting else "")


# ---------------------------------------------------------------------------
# Auth helpers. NOTE the deliberately inconsistent enforcement below.
# ---------------------------------------------------------------------------
def current_user() -> dict | None:
    return MEMBERS.get(session.get("user_id"))


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapper


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user = current_user()
            if user is None:
                return redirect(url_for("login", next=request.path))
            if user["role"] not in roles:
                return render_template("error.html",
                                       message="Forbidden: insufficient role."), 403
            return view(*args, **kwargs)
        return wrapper
    return decorator


@app.context_processor
def inject_user():
    return {"current_user": current_user()}


# ---------------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------------
@app.get("/")
def index() -> str:
    return render_template("index.html", trips=TRIPS.values())


@app.get("/hiking")
def hiking() -> str:
    return render_template("error.html",
                           message="Welcome to the Georgia Hiking Club!")


@app.get("/events/<int:event_id>")
@app.get("/trips/<int:trip_id>")
def trip_detail(event_id: int | None = None, trip_id: int | None = None):
    tid = trip_id if trip_id is not None else event_id
    trip = TRIPS.get(tid)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    leader = MEMBERS.get(trip["leader_id"])
    return render_template("trip_detail.html", trip=trip, spots=_spots(trip),
                           leader=leader)


@app.get("/search")
def search():
    # VULN (reflected XSS): `q` is handed to the template and rendered with
    # the |safe filter, bypassing Jinja autoescaping.
    q = request.args.get("q", "")
    needle = q.strip().lower()
    hits = [t for t in TRIPS.values()
            if needle and (needle in t["title"].lower()
                           or needle in t["location"].lower())]
    return render_template("search.html", q=q, results=hits)


@app.get("/go")
def go():
    # VULN (open redirect): redirects to any URL with no allow-list check.
    return redirect(request.args.get("url", "/"))


# ---------------------------------------------------------------------------
# Authentication. No rate limiting, no lockout, no password complexity.
# ---------------------------------------------------------------------------
@app.route("/auth/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        user = next((m for m in MEMBERS.values() if m["email"] == email), None)
        # VULN (no brute-force protection): unlimited attempts, generic only
        # by accident; plaintext comparison.
        if user and user["password"] == password:
            if user["banned"]:
                error = "This account is banned."
            else:
                session["user_id"] = user["id"]
                session["role"] = user["role"]
                # VULN (open redirect): `next` is followed without validation.
                nxt = request.args.get("next") or url_for("dashboard")
                return redirect(nxt)
        else:
            error = "Invalid email or password."
    return render_template("login.html", error=error)


@app.get("/auth/logout")
@app.post("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/auth/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    user = current_user()
    message = None
    if request.method == "POST":
        # VULN (weak password policy): any non-empty value accepted; no
        # check of the old password either.
        new = request.form.get("new_password", "")
        if new:
            user["password"] = new
            message = "Password updated."
        else:
            message = "Password cannot be empty."
    return render_template("change_password.html", message=message)


@app.route("/members/register", methods=["GET", "POST"])
def register_member():
    message = None
    if request.method == "POST":
        # VULN (weak password policy + open self-registration as any role):
        # role is taken straight from the form, so anyone can self-register
        # as an admin.
        new_id = _next_member_id()
        MEMBERS[new_id] = {
            "id": new_id,
            "name": request.form.get("name", "New Member"),
            "email": request.form.get("email", f"member{new_id}@ghc.test"),
            "password": request.form.get("password", "x"),
            "role": request.form.get("role", "member"),
            "banned": False, "medical": "None on file.",
            "performance": [], "dues_paid": False,
        }
        message = f"Created member #{new_id}."
    return render_template("register.html", message=message)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@app.get("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ---------------------------------------------------------------------------
# Members. Access control here is intentionally broken.
# ---------------------------------------------------------------------------
@app.get("/members")
@login_required
def list_members():
    return render_template("members.html", members=MEMBERS.values())


@app.get("/members/<int:member_id>")
@login_required
def get_member(member_id: int):
    # VULN (IDOR): any logged-in user can view any member; no ownership/role
    # check.
    member = MEMBERS.get(member_id)
    if member is None:
        return render_template("error.html", message="Member not found."), 404
    return render_template("member_detail.html", member=member)


@app.route("/members/<int:member_id>/profile", methods=["GET", "POST"])
@login_required
def member_profile(member_id: int):
    # VULN (IDOR): any logged-in user can edit anyone's profile.
    member = MEMBERS.get(member_id)
    if member is None:
        return render_template("error.html", message="Member not found."), 404
    if request.method == "POST":
        member["name"] = request.form.get("name", member["name"])
        member["email"] = request.form.get("email", member["email"])
    return render_template("member_detail.html", member=member)


@app.get("/members/<int:member_id>/medical")
@login_required
def member_medical(member_id: int):
    # VULN (broken access control / sensitive data exposure): medical notes
    # are spec'd as leader/admin-only and confidential, but any logged-in
    # user can read them here.
    member = MEMBERS.get(member_id)
    if member is None:
        return render_template("error.html", message="Member not found."), 404
    return render_template("medical.html", member=member)


@app.route("/members/<int:member_id>/performance-notes", methods=["GET", "POST"])
@login_required
def performance_notes(member_id: int):
    member = MEMBERS.get(member_id)
    if member is None:
        return render_template("error.html", message="Member not found."), 404
    if request.method == "POST":
        note = request.form.get("note", "")
        if note:
            member["performance"].append(note)
    return render_template("performance.html", member=member)


# VULN (broken function-level access control): banning is spec'd as admin-only,
# but only a login is required here — any member can ban anyone.
@app.post("/admin/members/<int:member_id>/ban")
@login_required
def ban_member(member_id: int):
    member = MEMBERS.get(member_id)
    if member is None:
        return render_template("error.html", message="Member not found."), 404
    member["banned"] = True
    return redirect(url_for("get_member", member_id=member_id))


@app.post("/admin/members/<int:member_id>/unban")
@login_required
def unban_member(member_id: int):
    member = MEMBERS.get(member_id)
    if member is None:
        return render_template("error.html", message="Member not found."), 404
    member["banned"] = False
    return redirect(url_for("get_member", member_id=member_id))


# ---------------------------------------------------------------------------
# Trips: registration, waitlist, attendance, leader actions
# ---------------------------------------------------------------------------
@app.get("/trips")
@app.get("/trips/local")
@app.get("/trips/excursions")
def list_trips():
    path = request.path
    if path.endswith("/local"):
        trips = [t for t in TRIPS.values() if t["type"] == "local"]
        heading = "Local Trips"
    elif path.endswith("/excursions"):
        trips = [t for t in TRIPS.values() if t["type"] == "excursion"]
        heading = "Paid Excursions"
    else:
        trips = list(TRIPS.values())
        heading = "All Trips"
    return render_template("trips.html", trips=trips, heading=heading,
                           spots=_spots)


@app.post("/trips/<int:trip_id>/register")
@login_required
def register_trip(trip_id: int):
    trip = TRIPS.get(trip_id)
    user = current_user()
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    # VULN (missing screening): the spec calls for screening on fitness /
    # ban status / dues. None of that is enforced — banned and unpaid members
    # register freely, and there is no difficulty gate.
    if user["id"] in trip["registrations"] or user["id"] in trip["waitlist"]:
        msg = "Already registered."
    elif len(trip["registrations"]) < trip["capacity_max"]:
        trip["registrations"].append(user["id"])
        msg = "Registered."
    else:
        trip["waitlist"].append(user["id"])
        msg = "Trip full — added to waitlist."
    return render_template("error.html", message=msg)


@app.post("/trips/<int:trip_id>/cancel-registration")
@login_required
def cancel_registration(trip_id: int):
    trip = TRIPS.get(trip_id)
    user = current_user()
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    for bucket in ("registrations", "waitlist"):
        if user["id"] in trip[bucket]:
            trip[bucket].remove(user["id"])
    return render_template("error.html", message="Registration cancelled.")


@app.post("/trips/<int:trip_id>/registrations/<int:member_id>/approve")
@role_required("leader", "admin")
def approve_registration(trip_id: int, member_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    if member_id in trip["waitlist"]:
        trip["waitlist"].remove(member_id)
        trip["registrations"].append(member_id)
    return render_template("error.html", message="Registration approved.")


@app.post("/trips/<int:trip_id>/registrations/<int:member_id>/reject")
@role_required("leader", "admin")
def reject_registration(trip_id: int, member_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    for bucket in ("registrations", "waitlist"):
        if member_id in trip[bucket]:
            trip[bucket].remove(member_id)
    return render_template("error.html", message="Registration rejected.")


@app.get("/trips/<int:trip_id>/waitlist")
@role_required("leader", "admin")
def view_waitlist(trip_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    waiting = [MEMBERS[m] for m in trip["waitlist"] if m in MEMBERS]
    return render_template("waitlist.html", trip=trip, waiting=waiting)


@app.post("/trips/<int:trip_id>/waitlist/promote")
@role_required("leader", "admin")
def promote_waitlist(trip_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    if trip["waitlist"]:
        nxt = trip["waitlist"].pop(0)
        trip["registrations"].append(nxt)
    return render_template("error.html", message="Promoted next waitlisted member.")


@app.post("/trips/<int:trip_id>/attendance/<int:member_id>")
@role_required("leader", "admin")
def mark_attendance(trip_id: int, member_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    status = request.form.get("status", "Finish")
    trip["attendance"][str(member_id)] = status
    return render_template("error.html", message=f"Attendance set: {status}.")


# ---------------------------------------------------------------------------
# Payments (mocked — no real charge ever occurs)
# ---------------------------------------------------------------------------
@app.route("/payments/membership-dues", methods=["GET", "POST"])
@login_required
def membership_dues():
    user = current_user()
    message = None
    if request.method == "POST":
        # MOCK ONLY: flips a flag, takes no payment details, charges nothing.
        user["dues_paid"] = True
        message = "Dues marked paid (mock — no charge made)."
    return render_template("payments.html", user=user, message=message)


@app.route("/payments/excursions/<int:trip_id>", methods=["GET", "POST"])
@login_required
def pay_excursion(trip_id: int):
    trip = TRIPS.get(trip_id)
    user = current_user()
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    message = None
    if request.method == "POST":
        if user["id"] not in trip["paid"]:
            trip["paid"].append(user["id"])
        message = f"Marked paid for {trip['title']} (mock — no charge made)."
    return render_template("excursion_pay.html", trip=trip, message=message)


@app.get("/payments/history/<int:member_id>")
@login_required
def payment_history(member_id: int):
    # VULN (IDOR): any logged-in user can read any member's payment history.
    member = MEMBERS.get(member_id)
    if member is None:
        return render_template("error.html", message="Member not found."), 404
    paid_trips = [t for t in TRIPS.values() if member_id in t["paid"]]
    return render_template("history.html", member=member, paid_trips=paid_trips)


@app.get("/reports/unpaid-members/<int:trip_id>")
@role_required("leader", "admin")
def unpaid_report(trip_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    unpaid = [MEMBERS[m] for m in trip["registrations"]
              if m not in trip["paid"] and m in MEMBERS]
    return render_template("unpaid.html", trip=trip, unpaid=unpaid)


@app.post("/trips/<int:trip_id>/drop-unpaid/<int:member_id>")
@role_required("leader", "admin")
def drop_unpaid(trip_id: int, member_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    if member_id in trip["registrations"]:
        trip["registrations"].remove(member_id)
    return render_template("error.html", message="Dropped unpaid member.")


@app.post("/trips/<int:trip_id>/refund/<int:member_id>")
@role_required("leader", "admin")
def refund_member(trip_id: int, member_id: int):
    trip = TRIPS.get(trip_id)
    if trip is None:
        return render_template("error.html", message="Trip not found."), 404
    if member_id in trip["paid"]:
        trip["paid"].remove(member_id)
    return render_template("error.html", message="Refund recorded (mock).")


# ---------------------------------------------------------------------------
# Leaders
# ---------------------------------------------------------------------------
@app.get("/leaders")
@login_required
def list_leaders():
    leaders = [m for m in MEMBERS.values() if m["role"] in ("leader", "admin")]
    return render_template("leaders.html", leaders=leaders)


@app.route("/leaders/<int:leader_id>/compliance", methods=["GET", "POST"])
@login_required
def leader_compliance(leader_id: int):
    # VULN (broken access control): compliance/health records for leaders are
    # editable by any logged-in user.
    leader = MEMBERS.get(leader_id)
    if leader is None:
        return render_template("error.html", message="Leader not found."), 404
    if request.method == "POST":
        leader["first_aid"] = request.form.get("first_aid", "unknown")
        leader["physical"] = request.form.get("physical", "unknown")
    return render_template("compliance.html", leader=leader)


# ---------------------------------------------------------------------------
# Security settings + leaky/erroring API endpoints
# ---------------------------------------------------------------------------
@app.route("/security/password-policy", methods=["GET", "PUT", "POST"])
def password_policy():
    # VULN (security misconfiguration): policy is advertised but never
    # enforced anywhere, and it can be changed without authentication.
    policy = {"min_length": 1, "require_symbols": False, "require_digits": False}
    return jsonify(policy)


@app.get("/api/users")
def api_users():
    # VULN (broken access control + sensitive data exposure): dumps every
    # user record — including plaintext passwords — with no auth.
    return jsonify(list(MEMBERS.values()))


@app.get("/api/risk")
def api_risk():
    # VULN (improper error handling / information disclosure): bad input
    # raises an unhandled exception, leaking a stack trace (esp. with debug).
    score = request.args.get("score", "1")
    return jsonify({"risk": 100 / int(score)})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).lower()
    if any(w in message for w in ("trip", "hike")):
        reply = "Browse trips at /trips, local at /trips/local, paid at /trips/excursions."
    elif any(w in message for w in ("pay", "dues", "refund")):
        reply = "Dues: /payments/membership-dues. Excursions: /payments/excursions/<id>."
    elif any(w in message for w in ("member", "register")):
        reply = "Members: /members. Register a trip: /trips/<id>/register."
    elif any(w in message for w in ("leader", "first aid")):
        reply = "Leader compliance: /leaders/<id>/compliance."
    else:
        reply = "Ask about trips, payments, members, or leaders."
    return jsonify({"reply": reply})


if __name__ == "__main__":
    # VULN (security misconfiguration): debug mode exposes the interactive
    # Werkzeug debugger and full tracebacks. Fine for a local lab, never prod.
    app.run(debug=True)
