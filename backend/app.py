import os
import smtplib
import threading
from datetime import datetime, timezone
from email.message import EmailMessage
from functools import wraps

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, redirect, request, session
from flask_cors import CORS
from supabase import create_client

load_dotenv()
FRONTEND = os.getenv("FRONTEND_URL", "http://localhost:3000")
REDIRECT = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5000/auth/callback")
if REDIRECT.startswith("http://"):  # local development only
    os.environ["AUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
CORS(app, origins=[FRONTEND], supports_credentials=True)
db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# ---------- Google OAuth 2.0 ----------
@app.get("/auth/login")
def login():
    return oauth.google.authorize_redirect(REDIRECT)


@app.get("/auth/callback")
def callback():
    info = oauth.google.authorize_access_token()["userinfo"]
    user = db.table("users").upsert(
        {"email": info["email"], "name": info.get("name") or info["email"], "picture": info.get("picture")},
        on_conflict="email",
    ).execute().data[0]
    session["user_id"] = user["id"]  # first login creates the account
    return redirect(FRONTEND)


@app.post("/auth/logout")
def logout():
    session.clear()
    return "", 204


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        uid = session.get("user_id")
        rows = db.table("users").select("*").eq("id", uid).execute().data if uid else []
        if not rows:
            abort(401)
        return fn(rows[0], *args, **kwargs)

    return wrapper


# ---------- Gmail notifications (SMTP + app password) ----------
def send_mail(recipients, subject, body):
    def _send():
        try:
            msg = EmailMessage()
            msg["From"] = os.environ["GMAIL_USER"]
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject
            msg.set_content(body)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.environ["GMAIL_USER"], os.environ["GMAIL_APP_PASSWORD"])
                smtp.send_message(msg)
        except Exception as exc:  # never break the API because of email
            app.logger.error("Email failed: %s", exc)

    threading.Thread(target=_send, daemon=True).start()


def notify(task, event, actor):
    people = db.table("users").select("id,name,email").in_("id", [task["created_by"], task["assigned_to"]]).execute().data
    by_id = {p["id"]: p for p in people}
    verb, subject = ("created", "New task") if event == "created" else ("completed", "Task completed")
    body = (
        f"{actor['name']} {verb} a task.\n\n"
        f"Title: {task['title']}\n"
        f"Description: {task.get('description') or '-'}\n"
        f"Created by: {by_id[task['created_by']]['name']}\n"
        f"Assigned to: {by_id[task['assigned_to']]['name']}\n"
    )
    send_mail(sorted({p["email"] for p in people}), f"{subject}: {task['title']}", body)


# ---------- API ----------
@app.get("/api/me")
@login_required
def me(user):
    return jsonify(user)


@app.get("/api/users")
@login_required
def list_users(user):
    return jsonify(db.table("users").select("id,name,email,picture").order("name").execute().data)


@app.get("/api/tasks")
@login_required
def list_tasks(user):
    mine = f"created_by.eq.{user['id']},assigned_to.eq.{user['id']}"
    return jsonify(db.table("tasks").select("*").or_(mine).order("created_at", desc=True).execute().data)


@app.post("/api/tasks")
@login_required
def create_task(user):
    data = request.get_json(force=True)
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="Title is required"), 400
    assignee = data.get("assigned_to") or user["id"]
    if not db.table("users").select("id").eq("id", assignee).execute().data:
        return jsonify(error="Assignee not found"), 400
    task = db.table("tasks").insert({
        "title": title,
        "description": (data.get("description") or "").strip() or None,
        "created_by": user["id"],
        "assigned_to": assignee,
    }).execute().data[0]
    notify(task, "created", user)
    return jsonify(task), 201


@app.patch("/api/tasks/<task_id>/complete")
@login_required
def complete_task(user, task_id):
    rows = db.table("tasks").select("*").eq("id", task_id).execute().data
    if not rows:
        abort(404)
    task = rows[0]
    if user["id"] not in (task["created_by"], task["assigned_to"]):
        abort(403)
    if task["status"] != "completed":
        task = db.table("tasks").update(
            {"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat()}
        ).eq("id", task_id).execute().data[0]
        notify(task, "completed", user)
    return jsonify(task)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
