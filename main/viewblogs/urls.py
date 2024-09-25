from django.contrib import admin
from django.urls import include, path
from viewblogs import views as vwviews
from .views import PostListView
app_name = 'viewblogs'
urlpatterns = [

    # path('viewblogs/',vwviews.vblogs, name='viewblogs'),
    path('', PostListView.as_view(), name='view'),
    # path('viewblogs/', vwviews.LoginView.as_view(template_name='viewblogs.html'), name='viewblogs'),
    path('create_blog/', vwviews.create_blog, name='create_blog'),
]