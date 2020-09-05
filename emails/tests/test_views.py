from django.test import TestCase, Client
from emails.models import Email, Category, EmailTranslation
from django.urls import reverse
from django.contrib.auth.models import User, Permission

class IndexTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user1.save()

    def test_user_logged_in(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'test_user1')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/accounts/login/?next=/emails/')

    def test_index_page_if_logged_in(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'emails/index.html')

    def test_num_emails_in_response_context(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('index'))
        self.assertTrue('num_emails' in response.context)
        self.assertTrue('num_emailtranslations' in response.context)

class EmailDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user2 = User.objects.create_user(username='test_user2', password='iO**pgf!!2')
        cls.test_user3 = User.objects.create_user(username='test_user3', password='2y!tyY!!*i')
        cls.test_user1.save()
        cls.test_user2.save()
        cls.test_user3.save()

        perm_can_view_email = Permission.objects.get(name="Can view email")
        cls.test_user2.user_permissions.add(perm_can_view_email)
        cls.test_user2.save()

        perm_can_change_email = Permission.objects.get(name="Can change email")
        cls.test_user3.user_permissions.add(perm_can_view_email)
        cls.test_user3.user_permissions.add(perm_can_change_email)
        cls.test_user3.save()

        cls.category1 = Category.objects.create(name="Company Introductions")
        cls.email1 = Email.objects.create(name_eng="Welcome", name_esp="Bienvenido", category=cls.category1)
        EmailTranslation.objects.create(
            email=cls.email1,
            language='ES',
            content = 'Bienvenido'
        )

    def test_user1_cant_view_emails(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_detail', args=(self.email1.id,)))
        self.assertEqual(response.status_code, 403)

    def test_user2_can_view_emails(self):
        login = self.client.login(username='test_user2', password='iO**pgf!!2')
        response = self.client.get(reverse('email_detail', args=(self.email1.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertFalse('Edit this email/ Add a translation' in str(response.content))

    def test_user3_can_see_edit_email(self):
        login = self.client.login(username='test_user3', password='2y!tyY!!*i')
        response = self.client.get(reverse('email_detail', args=(self.email1.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Edit this email / Add a translation" in str(response.content))

    def test_correct_template_used(self):
        login = self.client.login(username='test_user3', password='2y!tyY!!*i')
        response = self.client.get(reverse('email_detail', args=(self.email1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'email_detail.html')

class EmailListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user1.save()
        cls.category1 = Category.objects.create(name="Company Introductions")
        cls.email1 = Email.objects.create(name_eng="Welcome", name_esp="Bienvenido", category=cls.category1)
        EmailTranslation.objects.create(
            email=cls.email1,
            language='ES',
            content = 'Bienvenido'
        )

    def test_not_logged_in(self):
        response = self.client.get(reverse('all_emails'))
        self.assertRedirects(response, '/accounts/login/?next=/emails/all/')

    def test_logged_in(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('all_emails'))
        self.assertEqual(response.status_code, 200)

    def test_email_appears_in_list(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('all_emails'))
        self.assertTrue("Welcome" in str(response.content))

class EmailCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name="Company Introductions")
        cls.email1 = Email.objects.create(name_eng="Welcome", name_esp="Bienvenido", category=cls.category1)
        EmailTranslation.objects.create(
            email=cls.email1,
            language='ES',
            content = 'Bienvenido'
        )

        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user2 = User.objects.create_user(username='test_user2', password='Yui*!v4G6!')
        cls.test_user1.save()
        cls.test_user2.save()

        perm_can_add_email = Permission.objects.get(name="Can add email")
        cls.test_user1.user_permissions.add(perm_can_add_email)
        cls.test_user1.save()

    def test_user2_cant_view_create_email(self):
        login = self.client.login(username='test_user2', password='Yui*!v4G6!')
        response = self.client.get(reverse('email_create'))
        self.assertEqual(response.status_code, 403)

    def test_user1_can_view_create_email(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_create'))
        self.assertEqual(response.status_code, 200)

    def test_email_form_and_formset_in_context(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_create'))
        self.assertTrue(response.context['form'])
        self.assertTrue(response.context['formset'])

    '''
    Formset refers to emailtranslations related to this email
    '''
    def test_html_email_form_formset(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_create'))
        self.assertTrue('Choose a category!' in str(response.content))
        self.assertTrue('Specify a language' in str(response.content))

    def test_formset_length(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_create'))
        self.assertEqual(len(response.context['formset']), 3)

    def test_correct_template_used(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_create'))
        self.assertTemplateUsed(response, 'emails/email_create.html')

class EmailUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name="Company Introductions")
        cls.email1 = Email.objects.create(name_eng="Welcome", name_esp="Bienvenido", category=cls.category1)
        EmailTranslation.objects.create(
            email=cls.email1,
            language='ES',
            content = 'Bienvenido'
        )
        EmailTranslation.objects.create(
            email=cls.email1,
            language='EN',
            content = 'Welcome'
        )

        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user2 = User.objects.create_user(username='test_user2', password='Yui*!v4G6!')
        cls.test_user1.save()
        cls.test_user2.save()

        perm_can_change_email = Permission.objects.get(name="Can change email")
        cls.test_user1.user_permissions.add(perm_can_change_email)
        cls.test_user1.save()

    def test_user2_cant_view_update_email(self):
        login = self.client.login(username='test_user2', password='Yui*!v4G6!')
        response = self.client.get(reverse('email_update', args=(self.email1.id,)))
        self.assertEqual(response.status_code, 302)

    def test_user1_can_view_update_email(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_update', args=(self.email1.id,)))
        self.assertEqual(response.status_code, 200)

    '''
    Formset length should be 5....
    2 emailtranslations related to this email + 3 blank ones for adding email translations
    '''
    def test_formset_length_is_5(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_update', args=(self.email1.id,)))
        self.assertEqual(len(response.context['formset']), 5)

    def test_email_names_in_html(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_update', args=(self.email1.id,)))
        self.assertTrue("Welcome" in str(response.content))
        self.assertTrue("Bienvenido" in str(response.content))

    def test_correct_template_used(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('email_update', args=(self.email1.id,)))
        self.assertTemplateUsed(response, 'emails/email_update.html')
        self.assertTrue(response.status_code, 200)

class CategoryCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user2 = User.objects.create_user(username='test_user2', password='Yui*!v4G6!')
        cls.test_user1.save()
        cls.test_user2.save()

        perm_can_add_category = Permission.objects.get(name="Can add category")
        cls.test_user1.user_permissions.add(perm_can_add_category)
        cls.test_user1.save()

    def test_user_2_cant_access_add_category(self):
        login = self.client.login(username='test_user2', password='Yui*!v4G6!')
        response = self.client.get(reverse('category_create'))
        self.assertEqual(response.status_code, 403)

    def test_user_1_can_access_add_category(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_create'))
        self.assertEqual(response.status_code, 200)

    def test_add_category_page_html(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_create'))
        self.assertTrue("Create a new email template category", str(response.content))
        self.assertTrue("Name:", str(response.content))

    def test_correct_template_used(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_create'))
        self.assertTemplateUsed(response, 'emails/category_form.html')
        self.assertTrue(response.status_code, 200)

class CategoryUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name="Company Introductions")

        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user2 = User.objects.create_user(username='test_user2', password='Yui*!v4G6!')
        cls.test_user1.save()
        cls.test_user2.save()

        perm_can_change_category = Permission.objects.get(name="Can change category")
        cls.test_user1.user_permissions.add(perm_can_change_category)
        cls.test_user1.save()

    def test_user_2_cant_access_change_category(self):
        login = self.client.login(username='test_user2', password='Yui*!v4G6!')
        response = self.client.get(reverse('category_update', args=(self.category1.id,)))
        self.assertTrue(response.status_code, 403)

    def test_user_1_can_access_change_category(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_update', args=(self.category1.id,)))
        self.assertTrue(response.status_code, 200)

    def test_update_category_page_html(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_update', args=(self.category1.id,)))
        self.assertTrue("Update this email category", str(response.content))
        self.assertTrue("Name:", str(response.content))
        # Test category name appears in update name field
        self.assertTrue("Company Introductions:", str(response.content))

    def test_correct_template_used(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_update', args=(self.category1.id,)))
        self.assertTemplateUsed(response, 'emails/category_update.html')
        self.assertTrue(response.status_code, 200)

class CategoryListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name="Company Introductions")
        cls.category2 = Category.objects.create(name="Company Information")

        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user1.save()

    def test_not_logged_in_redirects(self):
        response = self.client.get(reverse('all_categories'))
        self.assertRedirects(response, '/accounts/login/?next=/emails/allcategories/')

    def test_logged_in_accesses_page(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('all_categories'))
        self.assertEqual(response.status_code, 200)

    def test_category_names_appear_html(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('all_categories'))
        self.assertTrue("Company Introductions" in str(response.content))
        self.assertTrue("Company Information" in str(response.content))

    def test_correct_template_used(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('all_categories'))
        self.assertTemplateUsed(response, 'category_list.html')
        self.assertTrue(response.status_code, 200)

class CategoryDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(username='test_user1', password='X$G123**3!')
        cls.test_user2 = User.objects.create_user(username='test_user2', password='Yui*!v4G6!')
        cls.test_user1.save()
        cls.test_user2.save()

        perm_can_change_category = Permission.objects.get(name="Can change category")
        perm_can_view_category = Permission.objects.get(name="Can view category")
        
        cls.test_user1.user_permissions.add(perm_can_change_category)
        cls.test_user1.user_permissions.add(perm_can_view_category)
        cls.test_user2.user_permissions.add(perm_can_view_category)
        
        cls.test_user1.save()
        cls.test_user2.save()

        cls.category1 = Category.objects.create(name="Company Introductions")

        cls.email1 = Email.objects.create(name_eng="Welcome", name_esp="Bienvenido", category=cls.category1)
        cls.email2 = Email.objects.create(name_eng="Hello", name_esp="Hola", category=cls.category1)
        cls.email3 = Email.objects.create(name_eng="Goodbye", name_esp="Adios", category=cls.category1)
        

    def test_user_1_can_see_update_category(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_detail', args=(self.category1.id,)))
        self.assertTrue("Update this category" in str(response.content))

    def test_user_2_cant_see_update_category(self):
        login = self.client.login(username='test_user2', password='Yui*!v4G6!')
        response = self.client.get(reverse('category_detail', args=(self.category1.id,)))
        self.assertFalse("Update this category" in str(response.content))

    def test_emails_appear_in_page(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_detail', args=(self.category1.id,)))
        self.assertTrue("Welcome" in str(response.content))
        self.assertTrue("Hello" in str(response.content))
        self.assertTrue("Goodbye" in str(response.content))

    def test_category_name_appears_in_page(self):
        login = self.client.login(username='test_user2', password='Yui*!v4G6!')
        response = self.client.get(reverse('category_detail', args=(self.category1.id,)))
        self.assertTrue("CATEGORY NAME: Company Introductions" in str(response.content))

    def test_correct_template_used(self):
        login = self.client.login(username='test_user1', password='X$G123**3!')
        response = self.client.get(reverse('category_detail', args=(self.category1.id,)))
        self.assertTemplateUsed(response, 'category_detail.html')
        self.assertTrue(response.status_code, 200)





        

















        









