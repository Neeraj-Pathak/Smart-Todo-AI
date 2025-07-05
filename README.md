# 🤖 Smart Todo List with AI

## 🌐 Live Demo

Coming soon or run locally as instructed below.

---

## 🚀 Project Overview

Smart Todo is an intelligent full-stack task management application with AI-powered features. It allows users to manage their daily tasks efficiently by providing smart suggestions like:

* 🔢 **AI-based task prioritization**
* ⏳ **Deadline recommendations**
* 📄 **Enhanced task descriptions based on daily context**
* 🔎 **Smart category/tag suggestions**

Built with:

* **Frontend:** Next.js + Tailwind CSS
* **Backend:** Django REST Framework
* **AI:** LM Studio / OpenAI API (Optional)
* **Database:** PostgreSQL (local or Supabase)

---

## 🔥 Features

* Full CRUD for tasks
* Add daily context (emails, notes, chats)
* Get AI-enhanced suggestions for each task
* Dark mode toggle
* Task filtering by priority
* Quick-add task box

---

## 📁 Folder Structure

```
.
├── backend/                # Django Backend (API, models, views)
├── frontend/               # Next.js Frontend (UI, pages)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
└── README.md               # Project documentation
```

---

## 🔍 Screenshots

### 🔢 Dashboard

![Dashboard](screenshots/dashboard.png)

### ➕ AI-Enhanced Task Creation

![Create Task](screenshots/create-task.png)

### 📄 Context Input Page

![Context Page](screenshots/context.png)

### ☾ Dark Mode Toggle

![Dark Mode](screenshots/dark-mode.png)

---

## 📚 Setup Instructions

### 📅 Prerequisites

* Python 3.10+
* Node.js 18+
* PostgreSQL or Supabase DB (Optional)

### ⚡ Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 🌐 Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Visit: `http://localhost:3000`

---

## 📃 API Endpoints

### Tasks

* `GET /api/tasks/` – Get all tasks
* `POST /api/tasks/` – Create new task

### Context

* `GET /api/context/` – Fetch context entries
* `POST /api/context/` – Add context entry

### AI

* `POST /api/ai/suggestions/` – Get task suggestions (priority, deadline, category)

---

## 📝 Sample AI Output

### Input:

```json
{
  "title": "Prepare Resume for Amazon SDE role",
  "description": "Update resume with latest projects."
}
```

### Context:

* "Amazon off-campus drive begins next week"
* "Project submission deadline is Monday"

### Output:

```json
{
  "priority_score": 6.54,
  "suggested_deadline": "2025-07-07",
  "suggested_category": "Career",
  "enhanced_description": "Update resume with latest projects and certifications for Amazon SDE role."
}
```

---

## 📊 Sample Context Data

```json
[
  {
    "content": "Amazon SDE deadline is this Friday",
    "source_type": "note"
  },
  {
    "content": "Team call scheduled at 4PM",
    "source_type": "whatsapp"
  }
]
```

---

## 📆 Bonus Features Implemented

* [x] Dark mode toggle
* [x] Category auto-tagging using keywords
* [ ] Sentiment analysis (TBD)
* [ ] Export/import tasks (TBD)

---

## 📁 requirements.txt (Python)

```txt
Django>=5.0
psycopg2-binary
djangorestframework
python-dotenv
dj-database-url
corsheaders
openai  # Optional
```

---

## 📥 Deployment / DB

You can run the backend using:

* Local PostgreSQL (preferred for dev)
* Supabase (PostgreSQL with remote access)

Switch database in `settings.py` based on `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/smarttodo
```

---

## 🎓 Author

Made by \ Nerraj Pathak for Full Stack Developer Assignment 🚀

---


