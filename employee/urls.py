from django.urls import path
from . import views

urlpatterns=[
    path('employee/',views.employee, name='employee'),
    path('employee/Information',views.Employee_Information, name='employee_information'),
    path('employee/list',views.employeelist, name='employeelist'),
    path('DTR/',views.Dtr, name='dtr'),
    path('DTR/Upload_punches',views.Upload_Punches, name='upload_punches'),
    path('DTR/Employees',views.Dtr_Employees, name='dtr_employee'),
    path('DTR/<pk>/Employees_punch_filter',views.Dtr_emp_punch_filter, name='dtr_emp_punch_filter'),
    path('DTR/Departments',views.Dtr_Department, name='dtr_department'),
    # path('DTR/Departments_group/<dpt>',views.department_group_dtr, name='department_group_dtr'),
    
    path('DTR/Departments<pk>filter',views.department_report_filter, name='department_report_filter'),
    path('DTR/Late_Undertime/<pk>',views.department_dtr_late_undertime, name='department_dtr_late_undertime'),
]

