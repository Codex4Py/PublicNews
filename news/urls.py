from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from . import views
from .views import search_news, submit_link
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_us, name='contact'),
    path('contact/success/', lambda request: render(request, 'contact_success.html'), name='contact_success'),
    path('news/', views.news_list, name='news_list'),
    path('post/<int:pk>/', views.news_detail, name='news_detail'),
    path('post/new/', views.news_create, name='news_create'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('search/', search_news, name='search_news'),
    path('submit-link/', submit_link, name='submit_link'),
    path('news/<int:pk>/comment/', views.add_comment, name='add_comment'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urls.py


