# Multi Language Email Template Manager

## What's this Django project all about?
Imagine working in a company where you have a multi-lingual team that sends numerous emails to clients every day in different languages.
Now, imagine if a lot of those emails were very similar in content, even if in different languages.

The idea for this app is that team members can login and contribute to a database of translations of commonly sent emails.

A team member can add a translation in their language to any existing email.
They can create new email templates for other team members to add translations to.
They can also assign categories to emails.

**So, if the French speaker, or the Italian speaker, or the Portuguese member of the team is away from the office, the other team members can easily access a template of a common email in that language and keep communication flowing with customers!**

The app admin has different privelige levels such as the ability to add email translations or simply to be able to read email translations.

***The main login for staff members and all email translation CRUD operations are performed on the front end.  Only the assigned admins can use /admin to set priveliges.***

## Interesting, useful but lesser used Django tools included...
- **from django.forms.models import inlineformset_factory**
  - The aim was to avoid limiting the number of email translations allowed per email.  Using inlineformset_factory allows the app users to create unlimited translations.

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

See ### [PythonDecouple](https://pypi.org/project/python-decouple/) for setting up a '.env' file for separating secret app information.
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

### A FEW THINGS STILL TO DO
- [ ] Change id to slug for 'Email' in emails.models.py
- [ ] Add more languages to the 'EmailTranslation' object in emails.models.py (Maybe using django-countries or something similar.)



