from rest_framework.permissions import BasePermission


class HasReportAccess(BasePermission):
    message = 'Нет доступа к отчётам. Обратитесь к администратору.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_perm('corepython.can_view_reports')
        )