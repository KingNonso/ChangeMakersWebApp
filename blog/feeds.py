from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Media


class LatestMediaFeed(Feed):
    title = 'Inclusive Friends Association News Blog'
    link = '/blog/'
    description = 'For news and events about the Inclusive Friends Association - visit our blog'

    def items(self):
        return Media.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
