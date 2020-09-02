from django.shortcuts import render, get_object_or_404

from .models import Email, EmailTranslation, Category

from django.forms.models import inlineformset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import EmailForm

# VIEWS

@login_required
def index(request):
    num_emails = Email.objects.all().count()
    num_emailtranslations = EmailTranslation.objects.all().count()
    return render(request, 'emails/index.html', 
        {"num_emails":num_emails,
        "num_emailtranslations":num_emailtranslations,
        })

class EmailDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'emails.view_email'
    model = Email
    template_name = 'email_detail.html'

class EmailListView(LoginRequiredMixin, generic.ListView):
    model = Email
    template_name = 'email_list.html'

class EmailCreate(PermissionRequiredMixin, generic.TemplateView):
    template_name = 'emails/email_create.html'
    permission_required = 'emails.add_email'

    def get(self, request, *args, **kwargs):
        email_form = EmailForm()
        EmailTranslationFormSet = inlineformset_factory(Email, EmailTranslation, fields=('language', 'content',))
        formset = EmailTranslationFormSet()

        context = {"form":email_form, "formset":formset}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        email_form = EmailForm(data=request.POST)
        EmailTranslationFormSet = inlineformset_factory(Email, EmailTranslation, fields=('language', 'content',))
        formset = EmailTranslationFormSet(data=request.POST)
        if email_form.is_valid() and formset.is_valid():
            email = email_form.save()
            emailtranslations = formset.save(commit=False)
            for emailtranslation in emailtranslations:
                emailtranslation.email = email 
                emailtranslation.save()
            return HttpResponseRedirect(reverse('email_detail', args=[str(email.id)]))
        context = {"form":email_form, "formset":formset}
        return self.render_to_response(context)

@permission_required('emails.change_email')
def email_update(request, pk):
    obj = get_object_or_404(Email, pk=pk)
    email_form = EmailForm(request.POST or None, instance = obj)

    EmailTranslationFormSet = inlineformset_factory(Email, EmailTranslation, fields=('language', 'content',))
    formset = EmailTranslationFormSet(request.POST or None, instance = obj)

    if email_form.is_valid() and formset.is_valid():
        email = email_form.save()
        emailtranslations = formset.save(commit=False)
        for emailtranslation in emailtranslations:
                emailtranslation.email = email 
                emailtranslation.save()
        return HttpResponseRedirect(reverse('email_detail', args=[str(email.id)]))

    context = {'form': email_form, "formset":formset}
    return render(request, 'emails/email_update.html', context)

class CategoryCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'emails.add_category'
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('all_emails')

class CategoryUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'emails.change_category'
    model = Category
    fields = '__all__'
    template_name = 'emails/category_update.html'
    success_url = reverse_lazy('all_categories')

class CategoryList(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'category_list.html'

class CategoryDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'emails.view_category'
    model = Category
    template_name = 'category_detail.html'


