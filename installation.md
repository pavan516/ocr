# VIDEO REF: https://www.youtube.com/watch?v=i5JykvxUk_A
# STEPS TO REMEMBER
- python related installations
  - install python latest version (download & install in windows)
  - verify python is installed with command: python --version
  - create virtual environment using command: python -m venv .venv
  - to activate vitual directory use command: . .venv/Scripts/activate
  - install django using command: pip install django
  - install django framework using command: pip install djangorestframework
  - install django cors headers using command: pip install django-cors-headers
  - run command: django-admin > to view the list of sub-commands to run
  - create a new project using the command: django-admin startproject project-name
- project management (cd project-name)
  - to run server, use the command: python manage.py runserver (this should be inside the project)
  - for migration use command: python manage.py migrate (this should be inside the project)
  - create super user for admin panel, use command: python manage.py createsuperuser
  - --- @todo ---

# VIDEO REF: https://www.youtube.com/watch?v=WuOjWTnnrfw
# STEPS TO REMEMBER
- python related installations
  - install python latest version (download & install in windows)
  - verify python is installed with command: python --version
  - install django using command: pip install django
  - install django framework using command: pip install djangorestframework
  - install django cors headers using command: pip install django-cors-headers (not to allow different domain requests)
  - create a new project using the command: django-admin startproject project-name
- project management
  - to run server, use the command: python manage.py runserver (this should be inside the project)
  - to create new app, use command: python manage.py startapp app-name
  - we need to install mysql using command: pip install pymysql
  - to connect to mongo DB, we need to install below items
    - pip install djongo
    - pip install dnspython
  - to use mongo, installed to resolve few ssues, pip install pymongo==3.12.3
- project modifications
  - inside settings.py => on INSTALLED_APPS add below keys
    - rest_framework
    - corsheaders
    - app.apps.AppConfig (reason: we created new application name called app)
  - inside settings.py => on MIDDLEWARE add below keys
    - corsheaders.middleware.CorsMiddleware
  - add `CORS_ORIGIN_ALLOW_ALL = True` inside settings.py above MIDDLEWARE
- application development
  - create tables from models by using command: python manage.py makemigrations app-name
  - when tables created inside migrations folder
    - we need to migrate using command: python manage.py migrate app-name
