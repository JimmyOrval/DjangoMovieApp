"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('get_movies/', views.get_movies, name='get_movies'),
    path('show_movie_details/<int:movie_id>/', views.show_movie_details, name='show_movie_details'),
    path('update_movie/<int:movie_id>/', views.update_movie, name='update_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
]
