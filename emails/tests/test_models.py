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

