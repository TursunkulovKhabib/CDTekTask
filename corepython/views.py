from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import HasReportAccess
from .serializers import CustomTokenObtainPairSerializer
from .services import ReportService
from .models import Student, Group


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class StudentReportView(APIView):
    permission_classes = [HasReportAccess]

    def get(self, request, student_id):
        if not Student.objects.filter(id=student_id).exists():
            return Response(
                {'error': 'Студент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        data = ReportService.get_student_report(student_id)
        return Response(data)


class GroupReportView(APIView):
    permission_classes = [HasReportAccess]

    def get(self, request, group_id):
        if not Group.objects.filter(id=group_id).exists():
            return Response(
                {'error': 'Группа не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        data = ReportService.get_group_report(group_id)
        return Response(data)


class MeView(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name(),
            'role': user.role,
            'has_report_access': user.has_perm('corepython.can_view_reports'),
            'student_id': getattr(getattr(user, 'student_profile', None), 'id', None),
        })