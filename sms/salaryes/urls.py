from django.urls import path
from . import views

urlpatterns = [
    path('', views.salary_list, name='salary_list'),
    path('<int:pk>/', views.salary_detail, name='salary_detail'),
    path('new/', views.salary_create, name='salary_create'),
    path('<int:pk>/edit/', views.salary_edit, name='salary_edit'),
    path('<int:pk>/delete/', views.salary_delete, name='salary_delete'),
    path('<int:pk>/issue/', views.update_salary_given_status, name='update_salary_given_status'),
    path('/allissue', views.issue_unissued_salaries, name='issue_unissued_salaries'),
]
