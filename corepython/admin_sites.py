from django.contrib.admin import AdminSite


class DirectorAdminSite(AdminSite):
    site_header = 'Страница директора'
    site_title = 'Директор'
    index_title = 'Менеджмент школой'

class StudentAdminSite(AdminSite):
    site_header = 'Страница студента'
    site_title = 'Студент'
    index_title = 'Мои оценки и расписание'

class TeacherAdminSite(AdminSite):
    site_header = 'Страница учителя'
    site_title = 'Учитель'
    index_title = 'Рабочее стол'


director_site = DirectorAdminSite(name='director_admin')
teacher_site = TeacherAdminSite(name='teacher_admin')
student_site = StudentAdminSite(name='student_admin')