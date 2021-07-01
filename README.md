# Email Template Translations Dashboard

## Intro
A bespoke Django dashboard application. It doesn't use the /admin page except for the superuser to add users and assign permissions.

Team members can add email templates in a base language and other team members can add translations.

It was written for a company that has:
1. Many common emails that they send to customers.
2. Team members that speak different languages.

Team members can be given different permission levels.

Team members can login and create email templates in a base language.  Other team members can add a translation of the email into another language.

The end result is that the company has an accessible database of common emails that are translated into different languges

## Features

- The app is pluggable -> everything is under one url. Visit '127.0.0.1:8000/emails/' instead of '127.0.0.1:8000' when you run the server.

- This version was written for a company that has two main languages, hence the titles of the emails are both in English and Spanish. This can be adapted.

- Team members can be given different permission levels.

- Team members can login and create email templates in a base language.  Other team members can add a translation of the email into another language.

- Team members can create categories and assign the email templates into different categories.

- At the moment the base language is in English and the translations can be in French, Spanish, Italian, German or Dutch. This can be adapted.

- Only logged in users can access the app.

- Only the site admins can access '/admin' to manage users.

- The app admin can assign priveliges - 
  - read emails
  - add translations

## Tools

- Test suite written with TestCase

- inlineformset_factory
  - used to allow multiple translations to be added to an email template.

- Django user authentication system implemented.

- Permission levels applied to function based views and class based views.
  - login_required
  - permission_required
  - LoginRequiredMixin
  - PermissionRequiredMixin

## Getting Started
Setting up Django:
```virtualenv commonemailtool -p python3```

```cd commonemailtool```

```source bin/activate```

```pip install Django```

```django-admin startproject commonemailtool```

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
Go to:
``` 127.0.0.1:8000/emails/ ```

### To Do
- [ ] Change id to slug for 'Email' in emails.models.py
- [ ] Add more languages to the 'EmailTranslation' object in emails.models.py (Maybe using django-countries or something similar.)

## Screenshots

**LogIn Page**
![login](https://github.com/richardgourley/multi-language-email-template-manager/blob/master/screenshots/login.png)

**Dashboard Home Page**
![dashboard_home](https://github.com/richardgourley/multi-language-email-template-manager/blob/master/screenshots/dashboardhome.png)

**Dashboard Page**
![dashboard](https://github.com/richardgourley/multi-language-email-template-manager/blob/master/screenshots/dashboard.png)





