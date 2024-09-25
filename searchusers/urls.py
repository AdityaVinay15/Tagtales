from django.urls import path

from searchusers.views import search_profiles, user_profile_view
app_name='searchusers'

urlpatterns = [

    path('', search_profiles, name='search_profiles'),
    path('profile/<str:username>/', user_profile_view, name='user_profile_view'),
]