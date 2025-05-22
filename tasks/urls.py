from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListAPIView.as_view(), name='tasks-api'),
    path('tasks/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail-api'),
]