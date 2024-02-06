from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='position_list'),
    path('<int:pk>/', views.detail, name='position_detail'),
    path('new/', views.create, name='position_create'),
    path('<int:pk>/edit/', views.edit, name='position_edit'),
    path('<int:pk>/delete/', views.delete, name='position_delete'),
]