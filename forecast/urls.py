from django.urls import path
from . import views

app_name = 'forecast'
urlpatterns = [
    path('', views.home, name='home'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('search_counts/', views.search_counts, name='search_counts'),
]
