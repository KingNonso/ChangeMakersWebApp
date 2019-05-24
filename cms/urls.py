from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('project/', views.HomeView.as_view(), name='project'),
    path('gallery/', views.HomeView.as_view(), name='gallery'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
