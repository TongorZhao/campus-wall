from django.urls import path
from . import views

app_name = 'messages'

urlpatterns = [
    path('', views.conversation_list_view, name='list'),
    path('new/<str:username>/', views.start_conversation_view, name='start'),
    path('<int:pk>/', views.conversation_detail_view, name='detail'),
    path('<int:pk>/send/', views.send_message_view, name='send'),
    path('<int:pk>/read/', views.mark_conversation_read_view, name='mark_read'),
]
