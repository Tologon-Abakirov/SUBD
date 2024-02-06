from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='budget_list'),
    path('<int:pk>/', views.detail, name='budget_detail'),
    path('new/', views.create, name='budget_create'),
    path('<int:pk>/edit/', views.edit, name='budget_edit'),
    path('<int:pk>/delete/', views.delete, name='budget_delete'),
]