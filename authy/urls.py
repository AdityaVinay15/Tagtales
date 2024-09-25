from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as authViews
from authy import views
from authy.views import Signup
app_name='authy'
urlpatterns = [
    # path('signin/', authViews.LoginView.as_view(template_name='signin.html'), name='signin'),
    path('signup/',Signup, name='signup'),
    path('signin/', views.Signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('profile/',views.profile_view,name='profile_view'),
    
    path('generate-otp/', views.generate_otp, name='generate_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('changepassword/', views.password_change, name='password_change'),
    path('viewblogs/', authViews.LoginView.as_view(template_name='viewblogs.html'), name='viewblogs'),
]

