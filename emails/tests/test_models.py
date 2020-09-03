from django.test import TestCase
from emails.models import Email, Category
from django.urls import reverse

'''
CATEGORY MODEL TESTS
'''
class CategoryModelTests(TestCase):
    # Any objects not going to be modified
    @class_method
    def setUpTestData(cls):
        Category.objects.create(name="Company Introductions")
    
    # Run once for every class function (eg. a fresh object before each class method is run)
    def setUp(self):
        pass

    def test_max_length(self):
        category1 = Category.objects.get(id=1)
        self.assertEqual(category1._meta.get_field('name').max_length, 100)

    def test_verbose_name_plural(self):
        category1 = Category.objects.get(id=1)
        self.assertEqual(category1._meta.verbose_name_plural, 'Categories')

    def test_string(self):
        category1 = Category.objects.get(id=1)
        self.assertEqual(str(category1), 'Company Introductions')

    def test_absolute_url(self):
        category1 = Category.objects.get(id=1)
        self.assertEqual(category1.get_absolute_url(), 'emails/category/1')

class EmailModelTests(TestCase):
    @class_method
    def setUpTestData(cls):
        category1 = Category.objects.create(name="Company Introductions")
        Email.object.create(name_eng="Welcome", name_esp="Bienvenido", category=category1)

    def test_max_length_name_eng_name_esp(self):
        email1 = Email.objects.get(id=1)
        self.assertEqual(email1._meta.get_field('name_eng').max_length, 100)
        self.assertEqual(email1._meta.get_field('name_esp').max_length, 100)

    def test_string(self):
        email1 = Email.objects.get(id=1)
        self.assertEqual(str(email1), 'Welcome, Bienvenido')

    def test_absolute_url(self):
        email1 = Email.objects.get(id=1)
        self.assertEqual(email1.get_absolute_url(), 'emails/email/1')

    def test_category_help_text(self):
        email1 = Email.objects.get(id=1)
        self.assertEqual(
            email1._meta.get_field('category').help_text,
            "Choose a category!  Can't see a relevant category?  Click 'Add a new email category' in the menu on the left."
        )

    def test_category_field_null_is_true(self):
        email1 = Email.objects.get(id=1)
        self.assertTrue(email1._meta.get_field('category').null)

class EmailTranslationModelTests(TestCase):
    @class_method
    def setUpTestData(cls):
        category1 = Category.objects.create(name="Company Introductions")
        email1 = Email.objects.create(name_eng="Welcome", name_esp="Bienvenido", category=category1)
        EmailTranslation.objects.create(
            email=email1,
            language='ES',
            content = 'Bienvenido'
        )

    def test_email_null_set_true(self):
        email_translation1 = EmailTranslation.objects.get(id=1)
        self.assertTrue(email_translation1._meta.get_field('email').null)

    def test_language_max_length(self):
        email_translation1 = EmailTranslation.objects.get(id=1)
        self.assertEqual(email_translation1._meta.get_field('language').max_length, 2)

    def test_count_language_options(self):
        email_translation1 = EmailTranslation.objects.get(id=1)
        self.assertEqual(len(email_translation1._meta.get_field('language').choices), 6)

    def test_default_language(self):
        email_translation1 = EmailTranslation.objects.get(id=1)
        self.assertEqual(email_translation1._meta.get_field('language').default, 'EN')

    def test_language_help_text(self):
        email_translation1 = EmailTranslation.objects.get(id=1)
        self.assertEqual(
            email_translation1._meta.get_field('language').help_text,
            'Specify a language'
        )

    def test_content_max_length(self):
        email_translation1 = EmailTranslation.objects.get(id=1)
        self.assertEqual(email_translation1._meta.get_field('content').max_length, 2000)




