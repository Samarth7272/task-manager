# Task Manager
Flask API + Next.js (TypeScript) + Supabase + Google OAuth 2.0 + Gmail notifications.

## Setup
1. **Supabase** – create a project, run `backend/schema.sql` in the SQL Editor, then copy the project URL and the `service_role` key (Settings > API).
2. **Google OAuth** – Google Cloud Console > APIs & Services > Credentials > Create OAuth client ID (Web application). Add the redirect URI `http://localhost:5000/auth/callback`. While the consent screen is in testing mode, add your Gmail accounts as test users.
3. **Gmail** – turn on 2-Step Verification for the sending account and create an App Password (myaccount.google.com/apppasswords).
4. **Backend**
   ```
   cd backend
   python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env    # fill in the values
   python app.py           # http://localhost:5000
   ```
5. **Frontend**
   ```
   cd frontend
   npm install
   cp .env.local.example .env.local
   npm run dev             # http://localhost:3000
   ```

Open `http://localhost:3000` (use `localhost`, not `127.0.0.1`, so the session cookie matches). To assign a task to someone else, that person must have signed in once with their Google account.

## How it works
- `GET /auth/login` and `/auth/callback` run the Google OAuth 2.0 flow; the first login creates the user. A signed Flask session cookie keeps them logged in.
- `GET /api/users`, `GET /api/tasks`, `POST /api/tasks`, `PATCH /api/tasks/<id>/complete`.
- Creating or completing a task emails both the creator and the assignee through Gmail SMTP.
