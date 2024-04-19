from django.urls import path
from . import views

urlpatterns = [
    path('', views.credit_list, name='credit_list'),
    #path('<int:pk>/', views.credit_detail, name='credit_detail'),
    path('new/', views.credit_create, name='credit_create'),
    path('<int:pk>/edit/', views.credit_edit, name='credit_edit'),
    path('<int:pk>/delete/', views.credit_delete, name='credit_delete'),
    path('<int:pk>/payment/', views.payment_list, name='credit_payment'),
    path('<int:pk>/paymentnow/', views.payment_list, name='credit_paymentnow'),
    path('<int:pk>/paymentnowow/', views.ppayment_list, name='credit_paymentnowow'),
    path('<int:pk>/pay/', views.update_credit_payments, name='update_credit_payments'),
]
