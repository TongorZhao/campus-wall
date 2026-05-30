from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('follow/<str:username>/', views.follow_toggle_view, name='follow_toggle'),
    path('followers/', views.followers_list_view, name='followers_list'),
    path('following/', views.following_list_view, name='following_list'),
]
