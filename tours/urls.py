# tours/urls.py
# URL patterns for the tours module

from django.urls import path
from .views import tour_list, tour_detail, tour_book

app_name = 'tours'

urlpatterns = [
    path('', tour_list, name='list'),
    # ensure the book URL is checked before the generic detail URL
    path('<slug:slug>/book/', tour_book, name='book'),
    path('<slug:slug>/', tour_detail, name='detail'),
]
