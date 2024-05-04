from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.create, name='create'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('profile/', views.profile_views, name='profile'),
    path('login/', views.login_view, name='login'),
]