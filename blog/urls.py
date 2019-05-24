from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .feeds import LatestMediaFeed

admin = [
    path('category/delete/<pk>/', views.AdminCategoryDeleteView.as_view(), name='delete_category'),
    path('category/create/', views.AdminCategoryCreateView.as_view(), name='create_category'),
    path('category/<slug>/', views.AdminCategoryDetailView.as_view(), name='category_detail'),
    path('category/', views.AdminCategoryListView.as_view(), name='category_list'),
    path('posts/delete/<pk>/', views.AdminPostDeleteView.as_view(), name='post_delete'),
    path('posts/update/<pk>/', views.AdminPostUpdateView.as_view(), name='post_update'),
    path('posts/new/', views.AdminPostCreateView.as_view(), name='post_create'),
    path('posts/', views.AdminPostListView.as_view(), name='post_list'),
    path('', TemplateView.as_view(template_name='blog/admin/index.html'), name='admin'),
]


urlpatterns = [
    path('', views.BlogListView.as_view(), name='index'),
    path('category/<slug:category>/', views.BlogListView.as_view(),    name='post_list_by_category'),
    path('tag/<tag>/', views.BlogListView.as_view(), name='post_list_by_tag' ),
    path('<int:year>/', views.YearArchive.as_view(), name="article_year_archive"),
    path('<int:year>/<int:month>/', views.MonthArchive.as_view(month_format='%m'), name="article_month_archive"),
    path('<int:year>/<int:month>/<int:day>/', views.DayArchive.as_view(month_format='%m'), name="article_day_archive"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.BlogDetailView.as_view(month_format='%m'), name='detail'),
    path('admin/', include(admin)),
    path('feed/', LatestMediaFeed(), name='media_feed')
]
