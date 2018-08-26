from django.urls import path

from . import views

urlpatterns = [
    path('topStories/', views.topStories, name='topStories'),
    path('', views.index, name='index'),
]