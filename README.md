# Lainaamo - Community Tool Library

Lainaamo is a modern, web-based tool-sharing platform built with Django. It’s designed for communities, housing associations, or maker spaces to manage a shared inventory of tools, allowing users to browse, borrow, and track their loans in real-time.

The project focuses on a high-end user experience, performance optimization, and a robust, scalable cloud architecture.

## Current Project State

Lainaamo is a fully featured, production-ready application. It leverages modern "Hypermedia" patterns to provide a snappy, single-page app (SPA) feel while maintaining a clean and maintainable Django backend. The deployment process is highly automated, utilizing continuous integration and Infrastructure as Code principles.

### Key Features & Architecture:
- **Interactive UX with HTMX:** Real-time search, category filtering, and instant "inline" tool returns without full-page reloads.
- **Cloud-Native Deployment:** Fully containerized with Docker and hosted on **Azure Container Instances (ACI)**.
- **Automated CI/CD Pipeline:** GitHub Actions automatically build and push new Docker images to Azure Container Registry (ACR) upon code changes.
- **Decoupled Storage & Database:** - Media files (tool images) are served via **Azure Blob Storage**.
  - Persistent data is managed through a secure **Azure Database for MySQL Flexible Server** (with forced SSL connections).
- **Pragmatic Testing Strategy:** Uses an in-memory SQLite database for blazing-fast automated test execution, while utilizing a Dockerized MySQL setup for local development to mirror the production environment.
- **Performance Optimized:** Uses `prefetch_related` and `select_related` to eliminate N+1 query problems, ensuring sub-second response times.
- **Mobile-First Design:** A fully responsive UI built with **Tailwind CSS** and **Alpine.js** for interactive components like the mobile navigation.

---

## 🛠️ Tech Stack

**Backend & Framework:**
- Python 3.14, Django 6.0
- **HTMX** (For dynamic, no-reload interactivity)
- **Alpine.js** (For lightweight frontend logic)
- `django-environ` (For robust 12-factor app configuration)
- Gunicorn (WSGI HTTP Server)

**Database & Storage:**
- Production & Local Dev: **MySQL** (Azure Flexible Server / Docker)
- Automated Testing: **SQLite** (For fast, isolated test runs)
- Media Storage: **Azure Blob Storage** (via `django-storages`)

**Infrastructure & DevOps:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Azure Container Registry (ACR) & Azure Container Instances (ACI)
- Azure CLI & Bash scripting

---

## ⚙️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/VaahtoluotoTuomas/django-community-tool-library.git](https://github.com/VaahtoluotoTuomas/django-community-tool-library.git)
   cd django-community-tool-library
   ```

2. **Environment Variables:**
   Create a `.env` file in the project root. The project uses `django-environ` to manage settings. In local development, the database will default to standard localhost settings, but you can override them if needed.
   ```env
   DEBUG=True
   SECRET_KEY=your-local-secret-key-here
   ```

3. **Start the Local Database with Docker:**
   Ensure you have Docker Desktop running, then spin up the local MySQL container to mirror production:
   ```bash
   docker compose up -d
   ```

4. **Set up the virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Run migrations and populate seed data (optional):**
   ```bash
   python manage.py migrate
   python seed_data.py
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   *Note: Local development defaults to `FileSystemStorage` for media. Azure Blob Storage requires specific environment variables to be configured and `DEBUG` set to `False`.*

---

## 🚀 Deployment

The project includes a robust deployment pipeline to Azure:

1. **Continuous Integration:** Code pushed to the `main` branch triggers a **GitHub Actions** workflow that builds the Docker image and pushes it to Azure Container Registry.
2. **Configuration Injection:** The repository includes a `deploy.example.sh` template. To deploy, copy this file to `deploy.sh` (which is gitignored), fill in your production secrets (such as the SSL-enforced `DATABASE_URL`), and run the script. It handles the final deployment to Azure Container Instances.