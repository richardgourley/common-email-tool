from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Email

class EmailForm(ModelForm):
	class Meta:
		model = Email
		fields = '__all__'

