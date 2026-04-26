# Lainaamo - Community Tool Library

Lainaamo is a modern, web-based tool-sharing platform built with Django. It’s designed for communities, housing associations, or maker spaces to manage a shared inventory of tools, allowing users to browse, borrow, and track their loans in real-time.

The project focuses on a high-end user experience, performance optimization, and a robust, scalable cloud architecture.

## Current Project State

Lainaamo is a fully featured, production-ready application. It leverages modern "Hypermedia" patterns to provide a snappy, single-page app feel while maintaining a clean and maintainable Django backend.

### Key Features & Architecture:
- **Interactive UX with HTMX:** Real-time search, category filtering, and instant "inline" tool returns without full-page reloads.
- **Cloud-Native Deployment:** Fully containerized with Docker and hosted on **Azure Container Instances (ACI)** using Infrastructure as Code principles.
- **Decoupled Storage & Database:** - Media files (tool images) are served via **Azure Blob Storage**.
    - Persistent data is managed through a production **Azure Database for MySQL** instance.
- **Performance Optimized:** Uses `prefetch_related` and `select_related` to eliminate N+1 query problems, ensuring sub-second response times.
- **Smart Borrowing Logic:** Features real-time availability tracking, borrowing history, and visual indicators for late returns.
- **Mobile First Design:** A fully responsive UI built with **Tailwind CSS** and **Alpine.js** for interactive components like the mobile navigation.
- **User Management:** Full authentication system with dedicated "My Loans" and "History" views for users.

---

## 🛠️ Tech Stack

**Backend & Framework:**
- Python 3.x, Django 5.x
- **HTMX** (For dynamic, no-reload interactivity)
- **Alpine.js** (For lightweight frontend logic)
- Gunicorn (WSGI HTTP Server)

**Database & Storage:**
- MySQL (Production: Azure Database for MySQL / Dev: Docker)
- Azure Blob Storage (Persistent media handling)

**Infrastructure & DevOps:**
- Docker & Docker Compose
- Azure Container Registry (ACR) & ACI
- Azure CLI

**Frontend:**
- Tailwind CSS
- Django Templates

---

## ⚙️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/VaahtoluotoTuomas/django-community-tool-library.git](https://github.com/VaahtoluotoTuomas/django-community-tool-library.git)
   cd django-community-tool-library
   ```

2. **Start the Local Database with Docker:**
   Ensure you have Docker Desktop running, then spin up the local MySQL container:
   ```bash
   docker compose up -d
   ```

3. **Set up the virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. **Run migrations and populate seed data (optional):**
   ```bash
   python manage.py migrate
   python seed_data.py
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   *Note: Local development defaults to `FileSystemStorage`. Azure Blob Storage requires specific environment variables (`AZURE_STORAGE_CONNECTION_STRING`, etc.) to be configured.*