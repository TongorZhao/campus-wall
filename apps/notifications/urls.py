from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list_view, name='list'),
    path('read/<int:pk>/', views.mark_read_view, name='mark_read'),
    path('read-all/', views.mark_all_read_view, name='mark_all_read'),
    path('delete/<int:pk>/', views.delete_notification_view, name='delete'),
    path('report/', views.report_view, name='report'),
    path('api/count/', views.unread_count_api, name='unread_count'),
]
