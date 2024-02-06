from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='rawSale_list'),
    path('<int:pk>/', views.detail, name='rawSale_detail'),
    path('new/', views.create, name='rawSale_create'),
    path('<int:pk>/edit/', views.edit, name='rawSale_edit'),
    path('<int:pk>/delete/', views.delete, name='rawSale_delete'),
]