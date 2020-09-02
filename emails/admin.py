from django.contrib import admin
from .models import Category, EmailTranslation, Email

class EmailTranslationInline(admin.TabularInline):
	model = EmailTranslation

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
	list_display = ('name_eng', 'name_esp', 'category')

	inlines = [EmailTranslationInline]

# Register your models here.
admin.site.register(Category)
admin.site.register(EmailTranslation)

