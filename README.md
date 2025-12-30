# Culina AI - Cooking Assistant Chat Application

A production-ready Django-based AI chat application powered by Google Gemini API, designed to help users with cooking recipes, meal planning, and food-related questions.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2.9-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

- **AI-Powered Cooking Assistant**: Get instant help with recipes, cooking tips, and meal planning
- **Modern UI**: Beautiful, responsive chat interface with smooth animations
- **Production-Ready**: Secure, scalable, and optimized for deployment
- **Real-time Chat**: Interactive chat experience with typing indicators
- **Error Handling**: Comprehensive error handling and logging
- **Environment-Based Configuration**: Easy configuration via environment variables

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Commands Reference](#commands-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Virtual environment (recommended)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd GitProjects/backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Copy the example (if available) or create manually
cp .env.example .env
```

Edit `.env` and add your configuration (see [Configuration](#configuration) section).

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Logging
LOG_LEVEL=INFO
DJANGO_LOG_LEVEL=WARNING

# Production Security (set to True for HTTPS)
SECURE_SSL_REDIRECT=False
```

### Generating Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Production Configuration

For production deployment, set:

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
LOG_LEVEL=WARNING
```

## 🎯 Usage

### Development Mode

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to `http://127.0.0.1:8000/`

3. Start chatting with Culina AI about cooking, recipes, or meal planning!

### Example Queries

- "How do I make chocolate chip cookies?"
- "What's a good vegetarian dinner recipe?"
- "How long should I cook pasta?"
- "Give me meal prep ideas for the week"

## 📡 API Documentation

### Chat API Endpoint

**Endpoint:** `GET /api/chat/`

**Parameters:**
- `message` (string, required): The user's message/question

**Example Request:**
```bash
curl "http://127.0.0.1:8000/api/chat/?message=How%20do%20I%20make%20pasta?"
```

**Example Response:**
```json
{
  "response": "Here's how to make pasta:\n\nStep 1: Boil water in a large pot...\n\nStep 2: Add salt to the water..."
}
```

**Error Responses:**

- `400 Bad Request`: Missing or empty message
  ```json
  {
    "response": "Please provide a message."
  }
  ```

- `500 Internal Server Error`: Server error
  ```json
  {
    "response": "An error occurred while processing your request. Please try again."
  }
  ```

## 📁 Project Structure

```
backend/
├── chat_app/                    # Main application
│   ├── __init__.py
│   ├── admin.py                 # Django admin configuration
│   ├── agent.py                 # AI agent (Gemini API integration)
│   ├── apps.py                  # App configuration
│   ├── models.py                # Database models
│   ├── urls.py                  # URL routing
│   ├── views.py                 # HTTP request handlers
│   ├── static/
│   │   └── chat_app/
│   │       ├── script.js        # Frontend JavaScript
│   │       └── style.css        # Styling
│   └── templates/
│       └── chat_app/
│           └── index.html       # Main HTML template
├── chat_backend/                # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Django settings (production-ready)
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database (development)
├── recipe_ai.log                # Application logs
└── .env                         # Environment variables (not in git)
```

## 🚀 Deployment

### Production Checklist

1. **Set Environment Variables:**
   - `DEBUG=False`
   - `SECRET_KEY` (generate new one)
   - `ALLOWED_HOSTS` (your domain)
   - `GEMINI_API_KEY` (your API key)

2. **Collect Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Configure Web Server:**
   - Use Gunicorn or uWSGI for production
   - Configure Nginx as reverse proxy
   - Set up SSL/HTTPS

5. **Security Settings:**
   - All security headers are automatically enabled when `DEBUG=False`
   - HSTS, XSS protection, and content type sniffing protection enabled

### Example Gunicorn Command

```bash
gunicorn chat_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/backend/staticfiles/;
    }
}
```

## 📝 Commands Reference

### Development Commands

```bash
# Start development server
python manage.py runserver

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Open Django shell
python manage.py shell

# Run tests
python manage.py test
```

### Production Commands

```bash
# Collect static files for production
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Check deployment settings
python manage.py check --deploy
```

## 🐛 Troubleshooting

### Common Issues

**1. GEMINI_API_KEY not found**
- Ensure `.env` file exists in `backend` directory
- Verify `GEMINI_API_KEY` is set in `.env`
- Restart the development server after adding environment variables

**2. ModuleNotFoundError**
- Activate your virtual environment
- Run `pip install -r requirements.txt`

**3. Database errors**
- Run `python manage.py migrate`
- Check database file permissions

**4. Static files not loading**
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py

**5. CORS errors (if accessing from different domain)**
- Add domain to `ALLOWED_HOSTS` in settings.py
- For API access, consider adding django-cors-headers

### Logging

Logs are written to:
- Console output (development)
- `recipe_ai.log` file (all environments)

Check logs for detailed error information:
```bash
tail -f recipe_ai.log
```

## 🔒 Security

- **Secret Key**: Never commit `SECRET_KEY` to version control
- **API Keys**: Keep `GEMINI_API_KEY` secure and private
- **Environment Variables**: Use `.env` file (not committed to git)
- **HTTPS**: Always use HTTPS in production
- **Security Headers**: Automatically enabled in production mode
- **CSRF Protection**: Enabled by default in Django

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - Web framework
- [Google Gemini API](https://ai.google.dev/) - AI capabilities
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Font Awesome](https://fontawesome.com/) - Icons

## 📧 Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Made with ❤️ for cooking enthusiasts**

