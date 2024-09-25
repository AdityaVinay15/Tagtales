from django.contrib import admin
from django.urls import include, path
from viewblogs import views as vwviews
from .views import search_form, search_results,createpost
app_name='searchblogs'
urlpatterns = [
    path('', search_form, name='search_form'),
    path('createpost/',createpost,name='createpost'),
    path('results/', search_results, name='search_results'),
]