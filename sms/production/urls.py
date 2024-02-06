from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='production_list'),
    path('<int:pk>/', views.detail, name='production_detail'),
    path('new/', views.create, name='production_create'),
    path('<int:pk>/edit/', views.edit, name='production_edit'),
    path('<int:pk>/delete/', views.delete, name='production_delete'),
]