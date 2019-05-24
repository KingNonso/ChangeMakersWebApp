from django.db import models
from django.urls import reverse

from .icons import icon

ICONS = icon()
icon_help = 'Select an Icon that best tells the story: <a href="http://nucleus.amazyne.com/ui-7-stroke-icons.html">Preview Icons Here</a>'

class About(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=50, null=True, blank=True, choices=ICONS, help_text=icon_help)
    position = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'About IFA/ Thematic Areas'

    def get_absolute_url(self):
        return reverse('cms:about')


class Contact(models.Model):
    address = models.TextField()
    phone = models.TextField(help_text="Use comma to separate items")
    email = models.TextField(help_text="Use comma to separate items")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone

    def get_email(self):
        return self.email.split(",")

    def get_phone(self):
        return self.phone.split(",")


    class Meta:
        verbose_name_plural = 'Contact Details'

    def get_absolute_url(self):
        return reverse('cms:contact')


class Enquiry(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'Enquiries'
