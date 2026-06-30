from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import smtplib
from email.mime.text import MIMEText

import os

from sqlalchemy.sql.functions import user

EMAIL_ADDRESS = os.environ.get("TICKET_EMAIL")
EMAIL_PASSWORD = os.environ.get("TICKET_EMAIL_PASSWORD")

def send_email(to_address, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_address

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("EMAIL SENT OK")
    except Exception as e:
        print("EMAIL FAILED:", repr(e))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
db = SQLAlchemy(app)


# ---------- DATABASE MODEL ----------
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False)   # Low / Medium / High
    category = db.Column(db.String(20), nullable=False)   # Hardware / Software / Network
    status = db.Column(db.String(20), default='Open')     # Open / In-Progress / Resolved
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------- ROUTES ----------

# Home page: show the "create ticket" form
@app.route('/')
def index():
    return render_template('create_ticket.html')


# Handle form submission
@app.route('/create', methods=['POST'])
def create_ticket():
    new_ticket = Ticket(
        title=request.form['title'],
        description=request.form['description'],
        priority=request.form['priority'],
        category=request.form['category'],
        email=request.form['email']
    )
    db.session.add(new_ticket)
    db.session.commit()

    send_email(new_ticket.email, "Ticket Received", f"Your ticket #{new_ticket.id} ('{new_ticket.title}') has been received.")

    return redirect(url_for('view_tickets'))

# Admin view: list all tickets
@app.route('/tickets')
def view_tickets():
    all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('tickets.html', tickets=all_tickets)

@app.route('/dashboard')
def dashboard():
    status_counts = db.session.query(Ticket.status, db.func.count(Ticket.id)).group_by(Ticket.status).all()
    priority_counts = db.session.query(Ticket.priority, db.func.count(Ticket.id)).group_by(Ticket.priority).all()

    status_labels = [row[0] for row in status_counts]
    status_values = [row[1] for row in status_counts]

    priority_labels = [row[0] for row in priority_counts]
    priority_values = [row[1] for row in priority_counts]

    return render_template('dashboard.html',
                            status_labels=status_labels, status_values=status_values,
                            priority_labels=priority_labels, priority_values=priority_values)


# Update ticket status (called from a dropdown/button on the admin page)
@app.route('/update_status/<int:ticket_id>', methods=['POST'])
def update_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = request.form['status']
    db.session.commit()

    if ticket.status == 'Resolved':
        send_email(ticket.email, "Ticket Resolved", f"Your ticket #{ticket.id} ('{ticket.title}') has been resolved.")

    return redirect(url_for('view_tickets'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # creates tickets.db and the Ticket table if they don't exist
    app.run(debug=True)