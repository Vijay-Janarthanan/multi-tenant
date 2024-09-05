# Multi-Tenant SaaS app
A scalable authentication and authorization service designed for multi-tenant SaaS applications, managing users, roles, and organizations with secure access and seamless integration. Supports role-based access control, user management, and API endpoints for efficient multi-organizational workflows.
## Clone Project
```bash
git clone https://github.com/Vijay-Janarthanan/multi-tenant.git
```

## Installation
1. Make sure you have Python installed. If not [Click here](https://www.python.org/downloads/) to install Python.
2. DB used here is Postgres. [Click here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) to download Postgres.
3. Now lets create a Virtual environment.
```bash
python -m venv venv
```
4. Activate the Virtual environment.
```bash
venv\Scripts\activate
```
5. Let's Install all the requirements.
```bash
pip install -r requirement.txt
```
6. Go to the Settings file inside multi-tenant folder and change the Database variable according to your db username, password.
7. I have used brevo for mail service api. You can create an account and setup the api key in settings file.
8. Also create a secret key for Fernet Encryption and JWT Encryption and setup in settings file.
9. Make a migration to create the required tables for the models.
```
python manage.py migrate
```
10. Run the Django Webserver
```
python manage.py runserver
```
11. Import the attached Postman export file and check the services

