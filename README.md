# IT Helpdesk Ticketing System

A Flask-based IT support ticketing system that mirrors core workflows found in real-world ITSM tools like ServiceNow and Zendesk — built to deepen my understanding of how service desk software actually works, end to end.

## Problem It Solves

Without a centralized system, IT support requests get lost in emails or chat messages, nobody has visibility into what's resolved versus pending, and there's no record of response times. This project solves that by giving every request a unique ticket, a status, and a full lifecycle — from submission to resolution.

## Features

- **Ticket Submission** — Users submit requests with a title, description, priority (Low/Medium/High), and category (Hardware/Software/Network)
- **Status Tracking** — Tickets move through a three-stage workflow: Open → In-Progress → Resolved
- **Admin Dashboard (List View)** — A central table view for support agents to see all tickets and update status in real time
- **Automated Email Notifications** — Users automatically receive an email when their ticket is created and again when it's marked Resolved, built using Python's `smtplib` and Gmail SMTP
- **Data Dashboard** — Live charts (built with Chart.js) visualizing ticket volume by status and by priority, pulled directly from the database

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, Jinja2 templating
- **Visualization:** Chart.js
- **Email Integration:** smtplib (Gmail SMTP)

## What I Learned

- Structuring a Flask application around a relational data model (tickets with status, priority, and category fields)
- Implementing real email notifications via SMTP, including handling authentication securely with environment variables instead of hardcoded credentials
- Writing aggregate SQL queries (grouped counts) and feeding that data into front-end visualizations
- Debugging real deployment issues: template path resolution, environment variable scoping, and SMTP authentication failures

## Running It Locally

1. Clone this repository
2. Create a virtual environment and install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set environment variables for email functionality:
   - `TICKET_EMAIL` — your Gmail address
   - `TICKET_EMAIL_PASSWORD` — a Gmail App Password (not your regular password)
4. Run the app:
   ```
   python app.py
   ```
5. Visit `http://127.0.0.1:5000` to submit a ticket, `/tickets` for the admin view, and `/dashboard` for the charts

## Future Improvements

- User authentication for agents vs. requesters
- Ticket assignment to specific support agents
- SLA breach alerts based on time-since-creation
- Search and filtering on the admin ticket list
