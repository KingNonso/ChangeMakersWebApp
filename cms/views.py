from django.contrib import messages
from django.views.generic import CreateView, ListView, TemplateView
from django.shortcuts import get_object_or_404

from blog.models import Media

from .forms import EnquiryForm
from .models import About, Contact


class HomeView(TemplateView):
    template_name = 'cms/home.html'

    def get_queryset(self):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        top_story = Media.objects.filter(top_story=1).first()
        # filter by date published
        latest_3_story = Media.objects.exclude(top_story=1).order_by('-id')[:3]
        about_us = About.objects.filter(position=1).first()

        context = {
            'active_page': 'home',
            'top_story': top_story,
            'latest_3_story': latest_3_story,
            'about_us': about_us,
        }
        return context


class ContactView(CreateView):
    template_name = 'cms/contact.html'
    form_class = EnquiryForm
    success_url = '/contact/'

    def form_valid(self, form):
        instance = form.save()
        messages.success(self.request, 'Form submission successful')
        return super(ContactView, self).form_valid(form)

    def get_queryset(self):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super(ContactView, self).get_context_data(*args, **kwargs)
        contact = Contact.objects.first()
        form_class = EnquiryForm

        context = {
            'active_page': 'contact',
            'contact': contact,
            'form': form_class
        }
        return context


class AboutView(ListView):
    template_name = 'cms/about.html'

    def get_queryset(self):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super(AboutView, self).get_context_data(*args, **kwargs)
        about_us = About.objects.filter(section=1).order_by('position')

        context = {
            'active_page': 'about',
            'about_us': about_us,
        }
        return context
