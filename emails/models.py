from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Email(models.Model):
    name_eng = models.CharField('Email name in English', max_length=100)
    name_esp = models.CharField('Email name in Spanish', max_length=100)
    category = models.ForeignKey(Category, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text="Choose a category!  Can't see a relevant category?  Click 'Add a new email category' in the menu on the left."
        )

    def __str__(self):
        return self.name_eng + ', ' + self.name_esp

    def get_absolute_url(self):
        return reverse('email_detail', args=[str(self.id)])

class EmailTranslation(models.Model):
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)

    LANGUAGES = (
        ('EN', 'English'),
        ('FR', 'French'),
        ('ES', 'Spanish'),
        ('DE', 'German'),
        ('NE', 'Dutch'),
        ('IT', 'Italian'),
    )

    language = models.CharField(
        max_length = 2,
        choices = LANGUAGES,
        blank = True,
        default = 'EN',
        help_text = 'Specify a language'
        )
    content = models.TextField(max_length=2000)




    

