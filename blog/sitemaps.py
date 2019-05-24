from django.contrib.sitemaps import Sitemap
from .models import Media


class MediaSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Media.published.all()

    def lastmod(self, obj):
        return obj.updated
