<div align="center">

# ✅ Task Manager

### Full-Stack Task Management with Google Login and Email Notifications

*Next.js (TypeScript) frontend · Flask REST API · Supabase (PostgreSQL) · Google OAuth 2.0 · Gmail SMTP notifications. Deployed to production.*



![Next.js](https://img.shields.io/badge/Next.js-Frontend-000000?logo=nextdotjs&logoColor=white)




![TypeScript](https://img.shields.io/badge/TypeScript-Typed-3178C6?logo=typescript&logoColor=white)




![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)




![Python](https://img.shields.io/badge/Python-API-3776AB?logo=python&logoColor=white)




![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?logo=supabase&logoColor=white)




![OAuth](https://img.shields.io/badge/Google-OAuth%202.0-4285F4?logo=google&logoColor=white)




![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?logo=vercel&logoColor=white)



[🌐 Live Demo](https://frontend-samarth9.vercel.app) · [📧 Hire Me](mailto:samarthworldwide@gmail.com) · [💼 LinkedIn](https://www.linkedin.com/in/samarth-shukla-b72003293) · [🐙 GitHub](https://github.com/Samarth7272)

</div>

---

## 📌 TL;DR (for recruiters)

- **What:** A production-deployed, multi-user task manager where people sign in with Google, create and assign tasks, and get email notifications.
- **Why it matters:** It covers real-world engineering topics: OAuth 2.0 authentication, session handling, a REST API, a relational database, transactional email and cloud deployment.
- **Stack:** Next.js · TypeScript · Flask (Python) · Supabase · Google OAuth 2.0 · Gmail SMTP · Vercel
- **Try it:** [frontend-samarth9.vercel.app](https://frontend-samarth9.vercel.app)

---

## 🎯 The Problem

Teams lose track of who is doing what when tasks live in chats and notes. People need to assign work to others, mark it complete, and be told when something changes.

**Task Manager** solves this. Users sign in securely with Google, create tasks, assign them to teammates and complete them. Both the creator and the assignee are emailed automatically.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔐 **Google OAuth 2.0 login** | Sign in with a Google account; the first login creates the user automatically |
| 🍪 **Session-based auth** | A signed Flask session cookie keeps users logged in |
| ➕ **Create tasks** | Add tasks and assign them to other registered users |
| ✅ **Complete tasks** | Mark tasks as done through the API |
| 👥 **User directory** | List users so tasks can be assigned to them |
| 📧 **Gmail email notifications** | Creating or completing a task emails both the creator and the assignee via Gmail SMTP |
| 🗄️ **Supabase database** | Persistent storage with a SQL schema and migrations |
| 🚀 **Production deployment** | Frontend and backend deployed to production |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Next.js, TypeScript | UI, routing, type safety |
| **Backend** | Flask (Python) | REST API and OAuth flow |
| **Database** | Supabase (PostgreSQL) | Data storage |
| **Auth** | Google OAuth 2.0 | Secure sign-in |
| **Email** | Gmail SMTP | Task notifications |
| **Hosting** | Vercel | Frontend deployment |
| **Tools** | Git, GitHub | Version control |

---

## 🏗️ Architecture

```
          USER (browser)
                │
                ▼
   NEXT.JS + TYPESCRIPT FRONTEND  (Vercel)
                │   HTTP / JSON + session cookie
                ▼
        FLASK REST API (Python)
        │         │          │
        ▼         ▼          ▼
  Google OAuth  Supabase   Gmail SMTP
  (login)       (database) (notifications)
```

---

## 🔌 API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/auth/login` | Start the Google OAuth 2.0 flow |
| `GET` | `/auth/callback` | OAuth callback; creates the user on first login and sets the session cookie |
| `GET` | `/api/users` | List users |
| `GET` | `/api/tasks` | List tasks |
| `POST` | `/api/tasks` | Create a task (emails creator and assignee) |
| `PATCH` | `/api/tasks/<id>/complete` | Mark a task complete (emails creator and assignee) |

---

## 🔄 How It Works

1. The user clicks **Sign in with Google**. `/auth/login` and `/auth/callback` run the OAuth 2.0 flow.
2. On the first login a user record is created. A signed Flask session cookie keeps them logged in.
3. The frontend calls the REST API to list users, list tasks, create tasks and complete tasks.
4. Creating or completing a task sends an email to both the creator and the assignee through Gmail SMTP.

---

## 📁 Project Structure

```
task-manager/
├── backend/        # Flask API, OAuth flow, email notifications, schema.sql
├── frontend/       # Next.js (TypeScript) application
├── migrations/     # Database migrations
├── .env.example    # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Supabase

Create a project, run `backend/schema.sql` in the SQL Editor, then copy the project URL and the `service_role` key (Settings → API).

### 2. Google OAuth

In Google Cloud Console go to APIs & Services → Credentials → Create **OAuth client ID (Web application)**. Add the redirect URI:

```
http://localhost:5000/auth/callback
```

While the consent screen is in testing mode, add your Gmail accounts as test users.

### 3. Gmail

Turn on 2-Step Verification for the sending account and create an **App Password** at `myaccount.google.com/apppasswords`.

### 4. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # fill in the values
python app.py               # http://localhost:5000
```

### 5. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev                 # http://localhost:3000
```

Open `http://localhost:3000`. Use `localhost`, not `127.0.0.1`, so the session cookie matches. To assign a task to someone, that person must have signed in at least once with their Google account.

---

## 🔒 Security Notes

- Authentication is handled by **Google OAuth 2.0**, so no passwords are stored.
- Sessions use a **signed cookie**.
- Secrets live in `.env` files. Only `.env.example` is committed.

---

## 🎓 Skills Demonstrated

- Designing and shipping a **full-stack application** to production
- Implementing **OAuth 2.0** authentication end to end
- Building a **REST API** with Flask
- Writing a typed **Next.js / TypeScript** frontend
- **Relational data modelling** with Supabase (PostgreSQL) and SQL migrations
- Sending **transactional emails** over SMTP
- **Environment-based configuration** and secret management
- **CI/CD-style deployment** on Vercel
- Professional **Git/GitHub** workflow

---

## 🔮 Roadmap

- [ ] 🧪 Automated tests (pytest for the API, Jest for the frontend)
- [ ] ⚙️ GitHub Actions CI pipeline
- [ ] 🐳 Docker setup
- [ ] ⏰ Due dates, priorities and reminders
- [ ] 🔍 Search and filtering
- [ ] 🔔 In-app notifications
- [ ] 📄 OpenAPI / Swagger documentation

---

## 👨‍💻 About the Author

**Samarth Shukla** is a final-year B.Tech Computer Science student and Software Engineer Intern at LV8 Tech, working on REST API design, OAuth 2.0 and backend architecture for fintech integrations (Next.js, TypeScript, PostgreSQL).

**Skills:** JavaScript/TypeScript · React/Next.js · Node.js/Express · Python (FastAPI, Flask) · MongoDB · PostgreSQL · SQL · Docker · AWS · Git

### 💼 Open to Opportunities

I'm actively looking for **Software Engineer, Backend and Full-Stack** roles (full-time and internships). If this project caught your eye, I'd love to talk.

[

![Email](https://img.shields.io/badge/Email-samarthworldwide%40gmail.com-D14836?logo=gmail&logoColor=white)

](mailto:samarthworldwide@gmail.com)
[

![LinkedIn](https://img.shields.io/badge/LinkedIn-Samarth%20Shukla-0A66C2?logo=linkedin&logoColor=white)

](https://www.linkedin.com/in/samarth-shukla-b72003293)
[

![GitHub](https://img.shields.io/badge/GitHub-Samarth7272-181717?logo=github&logoColor=white)

](https://github.com/Samarth7272)

---

<div align="center">

⭐ If you found this project useful, please give it a star!

</div>
