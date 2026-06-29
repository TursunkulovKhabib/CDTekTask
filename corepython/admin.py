from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .admin_sites import director_site, teacher_site, student_site
from .models import CustomUser, Group, Subject, Student, Grade


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Роль в системе', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Роль в системе', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count')
    search_fields = ('name',)

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Кол-во студентов'


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('name',)
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'group', 'get_username')
    list_filter = ('group',)
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'group')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'user__last_name'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Логин'


class GradeAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'get_group', 'subject', 'value', 'date')
    list_filter = ('subject', 'student__group', 'value')
    search_fields = ('student__user__first_name', 'student__user__last_name')
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            'student__user', 'student__group', 'subject'
        )
        if hasattr(request, 'teacher_filter') and request.teacher_filter:
            qs = qs.filter(subject__teacher=request.user)
        return qs

    def get_student(self, obj):
        return obj.student.user.get_full_name()
    get_student.short_description = 'Студент'
    get_student.admin_order_field = 'student__user__last_name'

    def get_group(self, obj):
        return obj.student.group
    get_group.short_description = 'Группа'



director_site.register(CustomUser, CustomUserAdmin)
director_site.register(Group, GroupAdmin)
director_site.register(Subject, SubjectAdmin)
director_site.register(Student, StudentAdmin)
director_site.register(Grade, GradeAdmin)


class TeacherGradeAdmin(GradeAdmin):

    def get_queryset(self, request):
        return (
            super(GradeAdmin, self).get_queryset(request)
            .select_related('student__user', 'student__group', 'subject')
            .filter(subject__teacher=request.user)
        )

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.subject.teacher == request.user

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.subject.teacher == request.user


class TeacherGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_count')

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Кол-во студентов'

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('teacher')
            .filter(teacher=request.user)
        )

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


teacher_site.register(Group, TeacherGroupAdmin)
teacher_site.register(Subject, TeacherSubjectAdmin)
teacher_site.register(Grade, TeacherGradeAdmin)



class StudentGradeAdmin(admin.ModelAdmin):
    list_display = ('subject', 'value', 'date')
    list_filter = ('subject',)
    date_hierarchy = 'date'

    def get_queryset(self, request):
        return (
            Grade.objects
            .select_related('subject', 'student__user')
            .filter(student__user=request.user)
        )

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')

    def get_queryset(self, request):
        try:
            student_group = request.user.student_profile.group
            return (
                Subject.objects
                .select_related('teacher')
                .filter(grade__student__group=student_group)
                .distinct()
            )
        except Student.DoesNotExist:
            return Subject.objects.none()

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


student_site.register(Grade, StudentGradeAdmin)
student_site.register(Subject, StudentSubjectAdmin)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Grade, GradeAdmin)