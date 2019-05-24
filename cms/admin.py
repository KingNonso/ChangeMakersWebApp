from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import About, Contact, Enquiry


class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'position')
    search_fields = ['title', 'description']





admin.site.register(About, AboutAdmin)
admin.site.register(Contact)
admin.site.register(Enquiry)



AdminSite.site_header = 'Change Makers Site Administration'
AdminSite.site_title = 'Change Makers Admin'
AdminSite.index_title = 'Change Makers Site Admin Dashboard'
