from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('details/<int:id>/', views.post_detail, name='post_detail')
]
