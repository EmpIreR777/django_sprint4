from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<slug:username>/', views.ProfileDetailView.as_view(), name='profile'),
]
