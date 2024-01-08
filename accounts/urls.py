from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.signup_page, name='signup_page')
]