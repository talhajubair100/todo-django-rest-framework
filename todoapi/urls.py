from django.urls import path
from .views import *

urlpatterns = [
    path("", ListTodo, name="list-todo"),
    path("<int:pk>", DetailTodo, name="detail-todo"),
    path("create", CreateTodo, name="create-todo"),
    path("update/<int:pk>", UpdateTodo, name="update-todo"),
    path("delete/<int:pk>", DeleteTodo, name="delete-todo"),
    path("toggle/<int:pk>", ToggleCompletedStatus, name="toggle-todo")
]
