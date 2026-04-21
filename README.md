# Lainaamo - Community Tool Library

Lainaamo is a modern, web-based tool-sharing platform built with Django. It’s designed for communities, housing associations, or maker spaces to manage a shared inventory of tools, allowing users to browse, borrow, and track their loans in real-time.

The project focuses on a clean user experience, performance optimization, and a robust backend.

## Current Project State

The application is currently a fully functional MVP (Minimum Viable Product). The core logic for inventory management and the borrowing/returning workflow is stable and optimized.

### Current Features:
- **User Authentication:** Complete registration and login system.
- **Tool Inventory:** A beautifully styled grid view of tools with real-time availability indicators (Green for available, Red for borrowed).
- **Dynamic Tool Details:** Individual pages for each tool showing descriptions, manufacturers, tags, and current loan status.
- **Smart Borrowing Logic:** Prevents double-borrowing. If a tool is out, the "Borrow" button is disabled and shows who has it.
- **Loan Management:** A dedicated "My Loans" page where users can track active loans and return tools with a single click.
- **Image Support:** Full integration for tool images via Django's media handling.
- **Performance Optimized:** Implemented `prefetch_related` and `select_related` to eliminate N+1 query problems, ensuring the database stays fast even as the inventory grows.
- **UI/UX:** Built with a custom Tailwind CSS theme, featuring responsive cards, automated auto-hiding alerts, and a consistent component-based design.

---

## 🛠️ Tech Stack
- **Backend:** Python 3.x, Django 5.x
- **Database:** MySQL (Local development with Docker)
- **Frontend:** Tailwind CSS, Django Templates
- **Media Handling:** Pillow

---

## 🗺️ Roadmap & Future Plans

The project is moving towards a more interactive "Single Page App" feel by integrating lightweight JavaScript frameworks.

### Phase 1: UX & Mobile Polishing (Upcoming)
- [ ] **Mobile Navigation:** Implementation of a responsive "hamburger" menu using **Alpine.js**.
- [X] **Late Return Indicators:** Visual cues (Red color coding) for loans that have passed their due date.

### Phase 2: Interactivity with HTMX
- [ ] **Instant Search:** A real-time search bar to find tools without page reloads.
- [ ] **Category Filtering:** Dynamic filtering based on tags (e.g., "Gardening", "Power Tools").
- [ ] **Inline Returns:** Using HTMX to update the loan list instantly when a tool is returned, removing the need for full-page redirects.

### Phase 3: More Features
- [ ] **Borrowing History:** A view for users to see their past completed loans.
- [ ] **Test Scripts:** Writing test scripts for the application

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VaahtoluotoTuomas/django-community-tool-library.git
   ```

2. **Start the Database with Docker:**
   Ensure you have Docker Desktop running, then spin up the MySQL container:
   ```bash
   docker compose up -d
   ```

3. **Install dependencies and run migrations:**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```