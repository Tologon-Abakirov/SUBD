from django.urls import path
from . import views

urlpatterns = [
    path('', views.Unitlist, name='Unitlist'),
    path('<int:pk>/', views.Unitdetail, name='Unitdetail'),
    path('new/', views.Unitcreate, name='Unitcreate'),
    path('<int:pk>/edit/', views.Unitedit, name='Unitedit'),
    path('<int:pk>/delete/', views.Unitdelete, name='Unitdelete'),
]
