from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskAPIView.as_view(), name='tasks-api'),
    path('tasks/<int:pk>/', views.TaskAPIView.as_view(), name='task-detail-api'),
]