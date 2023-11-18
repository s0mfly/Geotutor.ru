from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='news-delete'),
]