from django.urls import path
from . import views

urlpatterns = [
    path('', views.ppayment_list, name='ppayment_list'),
    # path('<int:pk>/', views.credit_payment_detail, name='credit_payment_detail'),
    #path('new/', views.credit_payment_create, name='credit_payment_create'),
    #path('<int:pk>/edit/', views.credit_payment_edit, name='credit_payment_edit'),
    #path('<int:pk>/delete/', views.credit_payment_delete, name='credit_payment_delete'),
]
