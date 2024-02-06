from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingredients_list, name='ingredients_list'),
    path('<int:pk>/', views.ingredients_detail, name='ingredients_detail'),
    path('new/', views.ingredients_create, name='ingredients_create'),
    path('<int:pk>/edit/', views.ingredients_edit, name='ingredients_edit'),
    path('<int:pk>/delete/', views.ingredients_delete, name='ingredients_delete'),
]