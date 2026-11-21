# SecureAuth – Secure Login System

A secure authentication web application built using Python and Flask. SecureAuth provides user registration, password hashing, login authentication, session management, CSRF protection, input validation, and rate limiting to help protect user accounts against common web attacks.

## Features

- User registration and login
- Password hashing using bcrypt
- Password strength validation
- SQLite database integration
- SQL injection protection using SQLAlchemy ORM
- CSRF protection using Flask-WTF
- Login rate limiting using Flask-Limiter
- Session-based authentication
- Protected dashboard
- Secure logout
- Duplicate email prevention
- Responsive dark-themed UI

## Technology Stack

- **Language:** Python
- **Backend:** Flask
- **Database:** SQLite
- **ORM:** Flask-SQLAlchemy / SQLAlchemy
- **Password hashing:** Flask-Bcrypt
- **CSRF protection:** Flask-WTF
- **Rate limiting:** Flask-Limiter
- **Frontend:** HTML, CSS
- **Configuration:** python-dotenv

## Project Structure

```text
secure-login-system/
├── app.py
├── database.py
├── requirements.txt
├── .env
├── .gitignore
├── instance/
│   └── users.db
├── templates/
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
└── static/
    └── style.css
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vamshi31-bodd/secure-login-system.git
cd secure-login-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_random_secret_key
COOKIE_SECURE=false
```

Generate a random secret key using:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Replace the placeholder with the generated value.

### 5. Run the application

```bash
python app.py
```

Open in your browser:

http://127.0.0.1:5000

## Application Routes

| Route | Description |
|---|---|
| `/` | Redirects to login or dashboard |
| `/register` | User registration |
| `/login` | User authentication |
| `/dashboard` | Protected user dashboard |
| `/logout` | Logs out the current user |

## Security Implementation

### Password Hashing
Passwords are hashed using bcrypt before being stored in the database. The original passwords are not stored.

### SQL Injection Prevention
Database interactions use SQLAlchemy ORM queries instead of building SQL statements by concatenating user input.

### CSRF Protection
Flask-WTF CSRF protection validates POST requests to help prevent cross-site request forgery.

### Rate Limiting
Flask-Limiter restricts repeated registration and login requests to reduce automated abuse and brute-force attempts.

### Session Management
The application uses Flask session cookies configured with HttpOnly and SameSite settings. Sessions are cleared on login and logout.

### Input Validation
Username, email and password inputs are validated before account creation.

## Security Testing

| Test | Result |
|---|---|
| User registration | Passed |
| Login with valid credentials | Passed |
| Login with invalid credentials | Passed |
| Protected dashboard access | Passed |
| Logout and session clearing | Passed |
| Bcrypt hash verification | Passed |
| SQL injection test input | Rejected |
| Repeated login rate limiting | Passed |

## Limitations & Future Improvements

- Add Two-Factor Authentication (2FA)
- Add email verification
- Implement password reset functionality
- Add stronger server-side security logging
- Use persistent rate-limit storage (Redis) instead of in-memory storage
- Add automated unit and integration tests
- Configure HTTPS and secure cookies for production deployment
- Add account lockout and alerting options

## Disclaimer

This project was developed for educational and cybersecurity learning purposes. It is a local demonstration application and has not been audited for production deployment.

## Author

**Vamshi**

Cybersecurity Projects Portfolio

