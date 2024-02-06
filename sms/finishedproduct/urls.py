from django.urls import path
from . import views

urlpatterns = [
    path('', views.Finishs_list, name='Finishs_list'),
    path('<int:pk>/', views.Finishs_detail, name='Finishs_detail'),
    path('new/', views.Finishs_create, name='Finishs_create'),
    path('<int:pk>/edit/', views.Finishs_edit, name='Finishs_edit'),
    path('<int:pk>/delete/', views.Finishs_delete, name='Finishs_delete'),
]