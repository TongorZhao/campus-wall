from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('hot/', views.hot_view, name='hot'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('tag/<slug:slug>/', views.tag_view, name='tag'),
    path('search/', views.search_view, name='search'),
    path('create/', views.post_create_view, name='create'),
    path('<int:pk>/', views.post_detail_view, name='detail'),
    path('<int:pk>/edit/', views.post_edit_view, name='edit'),
    path('<int:pk>/delete/', views.post_delete_view, name='delete'),
    path('<int:pk>/like/', views.post_like_toggle, name='like_toggle'),
    path('<int:pk>/favorite/', views.post_favorite_toggle, name='favorite_toggle'),
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
    path('my/favorites/', views.my_favorites_view, name='my_favorites'),
    path('my/posts/', views.my_posts_view, name='my_posts'),
]
