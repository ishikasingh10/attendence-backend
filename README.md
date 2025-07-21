# Attendance Backend

A robust Django-based backend for managing employee attendance using QR codes. This system enables secure check-in and check-out via dynamically generated QR codes, with RESTful APIs for integration and a live web interface for real-time monitoring.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Web Interface](#web-interface)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Employee Authentication**: Secure login for employees.
- **QR Code Generation**: Unique, time-limited QR codes for check-in and check-out.
- **Attendance Tracking**: Accurate daily logs of check-in and check-out times.
- **Live QR Display**: Real-time web dashboard for active QR codes.
- **RESTful API**: Endpoints for all core operations (login, attendance, QR management).
- **Password Reset**: Email-based password reset workflow.
- **Admin Panel**: Django admin for managing users, employees, and attendance records.
- **CORS Support**: Ready for cross-origin requests for frontend integration.

---

## Architecture

- **Backend**: Django 5.x, Django REST Framework
- **Database**: SQLite (default, easily swappable)
- **Web Server**: Gunicorn (for production)
- **Email**: SMTP (Mailtrap for development)
- **Static Files**: Managed via Django/Whitenoise

---

## Data Models

### Employee

| Field        | Type           | Description                |
|--------------|----------------|----------------------------|
| user         | OneToOne(User) | Linked Django user         |
| employee_id  | CharField      | Unique employee identifier |
| department   | CharField      | Department name            |

### Attendance

| Field          | Type         | Description                        |
|----------------|--------------|------------------------------------|
| employee       | ForeignKey   | Linked Employee                    |
| date           | DateField    | Date of attendance                 |
| check_in_time  | DateTime     | Check-in timestamp (nullable)      |
| check_out_time | DateTime     | Check-out timestamp (nullable)     |

### QRCodeSession

| Field      | Type         | Description                                  |
|------------|--------------|----------------------------------------------|
| token      | CharField    | Unique QR token                              |
| employee   | ForeignKey   | Linked Employee                              |
| mode       | CharField    | "checkin" or "checkout"                      |
| created_at | DateTime     | When QR was created                          |
| expires_at | DateTime     | When QR expires (default: 2 minutes)         |
| is_active  | Boolean      | Whether QR is still valid                    |

---

## API Endpoints

All endpoints are prefixed as shown below. Data is exchanged in JSON.

### 1. `POST /api/login/`
Authenticate an employee.
- **Request**: `{ "username": "...", "password": "..." }`
- **Response**: Employee details or error.

### 2. `GET /api/attendance/`
Get attendance logs for an employee.
- **Query Params**: `username`, optional `date` (YYYY-MM-DD) or `month` (YYYY-MM)
- **Response**: List of attendance records.

### 3. `POST /api/generate_qr/`
Generate a QR code for check-in or check-out.
- **Request**: `{ "username": "...", "mode": "checkin" | "checkout" }`
- **Response**: QRCodeSession details.

### 4. `POST /api/cancel_qr/`
Invalidate a QR code.
- **Request**: `{ "token": "..." }`
- **Response**: Status message.

### 5. `POST /api/mark_attendance/`
Mark attendance using a QR token.
- **Request**: `{ "token": "..." }`
- **Response**: Status, employee, mode, and timestamp.

### 6. `POST /api/reset_password/`
Initiate password reset (Django built-in).

### 7. `GET /api/reset/<uidb64>/<token>/`
Password reset confirmation (Django built-in).

---

## Web Interface

- **Live QR Dashboard**: `/`  
  Displays all active QR codes for employees, with real-time updates and expiry countdowns.
- **Error Page**: User-friendly error messages for invalid or expired QR codes.

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ishikasingh10/attendence-backend.git
   cd attendence-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the app**
   - API: `http://localhost:8000/api/`
   - Admin: `http://localhost:8000/admin/`
   - Live QR: `http://localhost:8000/`

---

## Configuration

- **Database**: Default is SQLite. To use PostgreSQL or others, update `DATABASES` in `core/settings.py`.
- **Email**: Uses Mailtrap for development. Set `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `EMAIL_PORT` in `core/settings.py` for production.
- **CORS**: All origins allowed by default (`CORS_ALLOW_ALL_ORIGINS = True`). Restrict in production.
- **Secret Key**: Change `SECRET_KEY` in production.

---

## Deployment

- **Production server**: Uses Gunicorn via `Procfile`.
- **Static files**: Use Whitenoise or configure a CDN.
- **Environment variables**: Set sensitive settings via environment variables in production.

**Example Heroku deployment:**
```bash
heroku create
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set EMAIL_HOST=...
heroku config:set EMAIL_HOST_USER=...
heroku config:set EMAIL_HOST_PASSWORD=...
heroku config:set EMAIL_PORT=...
git push heroku main
heroku run python manage.py migrate
heroku open
```

---

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. 
