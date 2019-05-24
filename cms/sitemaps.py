from django.contrib.sitemaps import Sitemap
from .models import About, Contact


class AboutSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.9

    def items(self):
        return About.objects.all()

    def lastmod(self, obj):
        return obj.updated

class ContactSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.9

    def items(self):
        return Contact.objects.all()

    def lastmod(self, obj):
        return obj.updated
