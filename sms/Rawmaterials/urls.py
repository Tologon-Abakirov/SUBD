from django.urls import path
from . import views

urlpatterns = [
    path('', views.rawlist, name='rawlist'),
    path('<int:pk>/', views.rawdetail, name='rawdetail'),
    path('new/', views.rawcreate, name='rawcreate'),
    path('<int:pk>/edit/', views.rawedit, name='rawedit'),
    path('<int:pk>/delete/', views.rawdelete, name='rawdelete'),
]