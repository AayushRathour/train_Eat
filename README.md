# Railway Food Delivery System

A full-stack web application for ordering food during train journeys. Built with Django and MySQL.

## Features

- User authentication (User & Admin roles)
- Train/Station-based food search
- Real-time train location simulation
- Order tracking system
- Rating and review system
- Admin panel for vendor management
- Responsive design with modern UI/UX

## Tech Stack

- Frontend: HTML5, CSS3, Vanilla JavaScript
- Backend: Django 5.0.2
- Database: MySQL
- Additional: FontAwesome icons, Bootstrap 5

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   DB_NAME=railway_food
   DB_USER=your-mysql-user
   DB_PASSWORD=your-mysql-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. Create MySQL database:
   ```sql
   CREATE DATABASE railway_food;
   ```

6. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Run development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
railway_food/
├── manage.py
├── requirements.txt
├── .env
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/
│   ├── orders/
│   ├── vendors/
│   └── trains/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── templates/
    ├── base.html
    ├── home.html
    └── components/
```

## Development Guidelines

1. Follow PEP 8 style guide for Python code
2. Use meaningful variable and function names
3. Comment complex logic
4. Keep templates DRY (Don't Repeat Yourself)
5. Use Django's built-in security features
6. Test thoroughly before committing

## License

This project is created for educational purposes. 