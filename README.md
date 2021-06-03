# Common email tool

## Intro
A user based Django web application for multi-lingual teams that allows assigned users to login, create common email templates and add translations.

## Features
- A team member can add a commonly used email template such as welcoming a new customer, a pricing template etc.
- Any other team member who is fluent in another language can go in and add a translation to any commonly used email templates.
- At the moment the base language is in English and the translations can be in French, Spanish, Italian, German or Dutch. Looking to expand this.
- Only logged in users can access the app.
- All emails and translations are created on the front end. Only the site admins can access '/admin'
- The app admin can assign priveliges - to only read email templates or to be able to add translations.

## Tools
- Full test suite using TestCase
- Django user authentication system implemented.
- **from django.forms.models import inlineformset_factory** implemented to allow the user to add extra email translations.

### To Do
- [ ] Change id to slug for 'Email' in emails.models.py
- [ ] Add more languages to the 'EmailTranslation' object in emails.models.py (Maybe using django-countries or something similar.)

## Getting Started
Setting up Django:
```virtualenv multi-language-email-template-manager -p python3```

```cd multi-language-email-template-manager```

```source bin/activate```

```pip install Django```

```django-admin startproject emailtemplatemanager```

```python manage.py migrate```

```python manage.py startapp emails```

Add code from 'emails' app directory, 'templates' directory, settings.py from 'emailtemplatemanager'

Install python-decouple
```pip install python-decouple```

See [PythonDecouple](https://pypi.org/project/python-decouple/) for setting up a '.env' file for separating secret app information.
See 'settings.py' to see how 'from decouple import config' is used.

After all code is setup, run...

```python manage.py makemigrations```

```python manage.py migrate```

```python manage.py createsuperuser```

See it in action!
```python manage.py runserver```


## Screenshots

**LogIn Page**
![login](https://github.com/richardgourley/multi-language-email-template-manager/blob/master/screenshots/login.png)

**Dashboard Page**
![dashboard](https://github.com/richardgourley/multi-language-email-template-manager/blob/master/screenshots/dashboard.png)

## Related
Wagtail beginners setup guide:
https://github.com/richardgourley/django-wagtail-stepbystep

Deploying Wagtail to PythonAnywhere:
https://github.com/texperience/wagtail-pythonanywhere-quickstart




