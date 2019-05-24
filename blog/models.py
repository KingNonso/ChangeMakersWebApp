from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField

from taggit.managers import TaggableManager
from .utils import unique_slug_generator
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_list_by_category',
                        args=[self.slug])


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Media(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'published'),
    )
    title = models.CharField(max_length=255)
    body = HTMLField('Content')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True, blank=True, default=None)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date')
    date = models.DateTimeField(default=timezone.now)
    top_story = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authors', on_delete=models.SET_NULL, null=True, blank=True, help_text="Leave author field blank if you want it to appear as 'Admin' ")
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-top_story', '-date']
        verbose_name_plural = 'Media - News & Events'

    def get_absolute_url(self):
        return reverse('blog:detail',
                       args=[self.date.year,
                             self.date.month,
                             self.date.day,
                             self.slug])

    objects = models.Manager()  # the default Manager
    published = PublishedManager()  # custom Manager

    def get_author(self):
        return self.author.get_full_name


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    # # make slug if not defined
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    # Make sure only one top story per time
    if instance.top_story and instance.status == 'published':
        qs_exists = Media.objects.filter(top_story=1, status='published').exists()
        if qs_exists:
            Media.objects.filter(top_story=1, status='published').update(top_story=0)


pre_save.connect(rl_pre_save_receiver, sender=Media)


class Image(models.Model):
    image = models.ImageField(upload_to='blog')
    description = models.CharField('Image Description', max_length=255, null=True, blank=True)
    primary = models.BooleanField('Set as Primary Image', default=False)
    media = models.ForeignKey('Media', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description if self.description else 'Image'

    def image_tag(self):
        return u'<img src="%s" width="200px" height="200px" />' % self.image.url
        image_tag.short_description = 'Image'
        image_tag.allow_tags = True

    class Meta:
        ordering = ['media']
        verbose_name_plural = 'Image Gallery'


class Video(models.Model):
    video = models.URLField(help_text="Add a youtube link to the video")
    description = models.CharField('Video Description', max_length=255, null=True, blank=True)
    media = models.ForeignKey('Media', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description if self.description else 'Video'

    def video_tag(self):
        return u'<iframe src="%s" width="200px" height="200px"></iframe>' % self.video
        video_tag.short_description = 'Video'
        video_tag.allow_tags = True

    class Meta:
        ordering = ['media']
        verbose_name_plural = 'Video Gallery'


class Comment(models.Model):
    post = models.ForeignKey(Media, on_delete=models.CASCADE,
                             related_name='comments')
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name='commentors', blank=True, null=True)
    name = models.CharField(max_length=80,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField('Comment')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.get_commentor_name(), self.post)

    def get_commentor_name(self):
    	name = self.member.get_full_name() if self.member else self.name
    	return name
