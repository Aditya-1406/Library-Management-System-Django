📚 Library Management System

The Library Management System is a modern web-based application designed to automate and simplify daily library operations. It replaces manual record-keeping with an efficient digital solution that helps manage books, members, and transactions with accuracy and ease.

This system improves workflow efficiency, reduces administrative workload, and enhances the experience for both librarians and members.

✨ Key Features
📖 Book Management

Add, update, and delete books

Track real-time availability

Organize books by category and author

👤 Member Management

Register and manage library members

Update member details easily

View borrowing history

🔄 Issue & Return System

Issue books with automatic date recording

Auto-generate due dates

Update book status upon return

💰 Fine Management

Automatic fine calculation for late returns

Track fine payment status

Maintain transparency in penalties

📊 Admin Dashboard

View total books and members

Monitor issued and returned books

Quick overview of library activity

🔍 Search & Navigation

Search books and members instantly

Pagination for smooth browsing of large records

📧 Email Notifications

Fine payment confirmations

Improvised communication with members

🛠️ Technology Stack

Backend: Python & Django
Frontend: HTML, CSS, Bootstrap
Database: SQLite (default) — compatible with MySQL & PostgreSQL

📧 Email Notification Setup (Gmail)

To enable email notifications, Gmail requires an App Password instead of your regular account password.

✅ Step 1: Enable 2-Step Verification

Open your Google Account

Go to Security

Enable 2-Step Verification

✅ Step 2: Generate App Password

Navigate to Security → App Passwords

Select Mail as the app

Choose Other or your device name

Click Generate

Copy the 16-character password provided

⚙️ Django Email Configuration

Add the following settings in your settings.py:

EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your-email@gmail.com

EMAIL_HOST_PASSWORD = your-16-digit-app-password

Once configured, the system can send automated reminders and notifications.

🎯 Benefits

Reduces manual paperwork

Improves efficiency and accuracy

Enhances record management

Ensures timely book returns

Provides better communication with members

🏫 Ideal For

Schools

Colleges

Small & medium libraries

Training institutes