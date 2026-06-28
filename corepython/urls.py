from django.urls import path
from .views import (
    CustomTokenObtainPairView,
    StudentReportView,
    GroupReportView,
    MeView,
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('me/', MeView.as_view(), name='me'),

    path('reports/student/<int:student_id>/', StudentReportView.as_view(), name='report_student'),
    path('reports/group/<int:group_id>/', GroupReportView.as_view(), name='report_group'),
]