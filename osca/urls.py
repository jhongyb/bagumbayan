
from django.urls import path
from . import views


urlpatterns=[
    path('OSCA/',views.osca,name='osca'),
    path('OSCA/NEW',views.newosca,name='newosca'),
    path('OSCA/MASTERLIST',views.oscamasterlist,name='oscamasterlist'),
    path('OSCA/UPDATE/r<pk>f',views.updatesenior,name='updatesenior'),
    path('OSCA/DELETE/r<pk>f',views.deletesenior,name='deletesenior')
]
from django.urls import path
from . import views


urlpatterns=[
    path('OSCA/',views.osca,name='osca'),
    path('OSCA/NEW',views.newosca,name='newosca'),
    path('OSCA/MASTERLIST',views.oscamasterlist,name='oscamasterlist'),
    path('OSCA/UPDATE/r<pk>f',views.updatesenior,name='updatesenior'),
    path('OSCA/DELETE/r<pk>f',views.deletesenior,name='deletesenior'),
    path('OSCA/FIGURE/',views.oscabarangayfigure,name='oscabarangayfigure'),

    #REPORTS
    path('OSCA/REPORTS/',views.Senior_All,name='senior_all'),
    path('OSCA/REPORTS/BRGYLIST<pk>FILTER',views.Senior_listby_barangay,name='Senior_listby_barangay'),
    path('OSCA/REPORTS/ALL_FIGURES',views.Senior_Figures,name='senior_figures'),
    path('OSCA/REPORTS/BRGY<pk>FILTER',views.Senior_Figures_barangay,name='Senior_Figures_barangay'),
    path('OSCA/REPORTS/80ABOVED',views.senior_80above,name='senior_80above'),

]