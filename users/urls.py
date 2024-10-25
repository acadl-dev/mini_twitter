# urls.py (users app)

from django.urls import path
from . import views

urlpatterns = [
    path('follow-unfollow/<str:username>/', views.follow_unfollow, name='follow-unfollow'),
]
