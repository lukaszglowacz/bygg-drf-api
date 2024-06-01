from django.urls import path
from .views import EmployeeList, EmployeeDetail
from .views import EmployeeMonthlySummaryPDF

urlpatterns = [
    path('', EmployeeList.as_view(), name='employee-list'),
    path('<int:pk>/', EmployeeDetail.as_view(), name='employee-detail'),
    path('<int:id>/monthly-summary-pdf/', EmployeeMonthlySummaryPDF.as_view(), name='employee-monthly-summary-pdf'),
]
