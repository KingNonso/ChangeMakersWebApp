from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector, TrigramSimilarity)
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (DetailView, ListView, YearArchiveView, MonthArchiveView, 
DayArchiveView, DateDetailView, CreateView, DeleteView, UpdateView)

from taggit.models import Tag

from .forms import CommentForm, SearchForm, AdminCreateForm
from .models import Category, Media
from accounts.models import Member


class BlogListView(ListView):
    template_name = 'blog/list.html'
    model = Media
    context_object_name = 'stories'  # Default: object_list
    paginate_by = 2

    def get_queryset(self):
        word = self.kwargs
        queryset = Media.published.order_by('-id')
        if 'category' in word:
            query = word['category']
            queryset = Media.published.filter(category__slug=query).order_by('-id')

        if 'tag' in word:
            tag = word['tag']
            tag = get_object_or_404(Tag, slug=tag)
            queryset = Media.published.filter(tags__in=[tag])

        search = self.request.GET.get('q')
        if search:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data['q']
                search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                search_query = SearchQuery(query)

                queryset = Media.published.annotate(
                    rank=SearchRank(search_vector, search_query),
                    similarity=TrigramSimilarity('title', query) + TrigramSimilarity('body', query),
                # ).order_by('-rank')
                ).filter(similarity__gt=0.01).order_by('-rank')


        return queryset


    def get_context_data(self, *args, **kwargs):
        word = self.kwargs
        context = super(BlogListView, self).get_context_data(*args, **kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        tags = Tag.objects.all()
        context['tags'] = tags
        if 'category' in word:
            query = word['category']
            context['category'] = query

        if 'tag' in word:
            tag = word['tag']
            context['tag'] = tag

        search = self.request.GET.get('q')
        if search:
            context['search'] = search

        extra = {
            'active_page': 'blog',
        }
        context.update(extra)
        return context

class BlogDetailView(DateDetailView):
    template_name = 'blog/blog_detail.html'
    model = Media
    context_object_name = 'story'  # Default: object_list
    date_field = 'date'

    def get_queryset(self):
        queryset = Media.published.order_by('-id')
        return queryset

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Write Your Logic here
            new_comment = comment_form.save(commit=False)
            self.object = self.get_object()
            new_comment.post = super(BlogDetailView, self).get_object()
            if request.POST['member']:
                new_comment.member = Member.objects.get(pk=request.POST['member'])
            # Save the comment to the database
            new_comment.save()

            context = context = self.get_context_data(**kwargs)
            extra = {
                'new_comment': True,
            }
            context.update(extra)
            print(context)

            return render(request, 'blog/blog_detail.html', context=context)

        else:
            self.object = self.get_object()
            context = super(BlogDetailView, self).get_context_data(*args, **kwargs)
            return context

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_seen = timezone.now()
        obj.views = int(obj.views or 0) + 1
        obj.save()
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(BlogDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        comments = self.get_object().comments.filter(active=True)
        # List of similar posts
        post_tags_ids = self.get_object().tags.values_list('id', flat=True)
        similar_posts = Media.published.filter(tags__in=post_tags_ids).exclude(id=self.get_object().id)
        similar_posts = similar_posts.annotate(same_tags=Count(
            'tags')).order_by('-same_tags', '-date')[:3]

        comment_form = CommentForm()

        extra = {
            'comments': comments,
            'active_page': 'blog',
            'form': comment_form,
            'similar_posts': similar_posts,
        }
        context.update(extra)
        return context

class YearArchive(YearArchiveView):
    template_name = 'blog/list_year_archive.html'
    model = Media
    date_field = 'date'
    make_object_list = True
    paginate_by = 50

class MonthArchive(MonthArchiveView):
    template_name = 'blog/list_month_archive.html'
    model = Media
    date_field = 'date'
    make_object_list = True
    paginate_by = 50

class DayArchive(DayArchiveView):
    template_name = 'blog/list_day_archive.html'
    model = Media
    date_field = 'date'
    make_object_list = True
    paginate_by = 2


class AdminPostListView(ListView):
    model = Media
    template_name = "blog/admin/post_list.html"
    context_object_name = 'stories'  # Default: object_list
    paginate_by = 20

class AdminPostCreateView(CreateView):
    model = Media
    template_name = "blog/admin/create_post.html"
    form_class = AdminCreateForm
    # success_url = reverse_lazy('blog:post_list')

class AdminPostUpdateView(UpdateView):
    model = Media
    template_name = "blog/admin/create_post.html"
    fields = '__all__'
    success_url = reverse_lazy('blog:post_list')

class AdminPostDeleteView(DeleteView):
    model = Media
    success_url = reverse_lazy('blog:post_list')

''' Category Actions '''
class AdminCategoryCreateView(CreateView):
    model = Category
    template_name = "blog/admin/create_category.html"
    fields = '__all__'
    success_url = reverse_lazy('blog:category_list')

class AdminCategoryListView(ListView):
    model = Category
    template_name = "blog/admin/category_list.html"

class AdminCategoryDetailView(DetailView):
    model = Category
    template_name = "blog/admin/category_detail.html"

class AdminCategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('blog:category_list')
