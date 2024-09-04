Create a virtual environment by using below command

python3 -m venv venv




Install required libraries

pip install Django
pip install djangorestframework
pip install psycopg2-binary
pip install rest_framework_simplejwt




Start a Djang Project using below command

django-admin startproject multi_tenant




Create an app inside the project folder

py manage.py startapp tenants





Run the Django server

py manage.py runserver