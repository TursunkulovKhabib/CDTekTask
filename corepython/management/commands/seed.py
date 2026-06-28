from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from corepython.models import CustomUser, Group, Subject, Student, Grade


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write('Очистка старых данных...')
        Grade.objects.all().delete()
        Student.objects.all().delete()
        Subject.objects.all().delete()
        Group.objects.all().delete()
        CustomUser.objects.all().delete()

        director = CustomUser.objects.create(
            username='director',
            password=make_password('12345678'),
            first_name='Иван',
            last_name='Иванов',
            role='director',
            is_staff=True,
            is_superuser=True,
        )

        teacher1 = CustomUser.objects.create(
            username='teacher1',
            password=make_password('12345678'),
            first_name='Мария',
            last_name='Петрова',
            role='teacher',
            is_staff=True,
        )

        teacher2 = CustomUser.objects.create(
            username='teacher2',
            password=make_password('12345678'),
            first_name='Алексей',
            last_name='Сиденкевич',
            role='teacher',
            is_staff=True,
        )

        student_user1 = CustomUser.objects.create(
            username='student1',
            password=make_password('12345678'),
            first_name='Анна',
            last_name='Иванова',
            role='student',
            is_staff=True,
        )

        student_user2 = CustomUser.objects.create(
            username='student2',
            password=make_password('12345678'),
            first_name='Пётр',
            last_name='Ослов',
            role='student',
            is_staff=True,
        )

        student_user3 = CustomUser.objects.create(
            username='student3',
            password=make_password('12345678'),
            first_name='Елена',
            last_name='Ленина',
            role='student',
            is_staff=True,
        )

        group_a = Group.objects.create(name='Группа А')
        group_b = Group.objects.create(name='Группа Б')

        math = Subject.objects.create(name='Математика', teacher=teacher1)
        physics = Subject.objects.create(name='Физика', teacher=teacher1)
        infa = Subject.objects.create(name='Информатика', teacher=teacher2)
        english = Subject.objects.create(name='Английский', teacher=teacher2)

        s1 = Student.objects.create(user=student_user1, group=group_a)
        s2 = Student.objects.create(user=student_user2, group=group_a)
        s3 = Student.objects.create(user=student_user3, group=group_b)

        grades_data = [
            (s1, math, 5), (s1, math, 4), (s1, math, 5),
            (s1, physics, 3), (s1, physics, 4),
            (s1, infa, 5), (s1, infa, 5),
            (s1, english, 4), (s1, english, 3),

            (s2, math, 3), (s2, math, 3), (s2, math, 4),
            (s2, physics, 5), (s2, physics, 5),
            (s2, infa, 4), (s2, infa, 3),
            (s2, english, 5), (s2, english, 4),

            (s3, math, 4), (s3, math, 5),
            (s3, physics, 3), (s3, physics, 3),
            (s3, infa, 5), (s3, infa, 4),
            (s3, english, 4), (s3, english, 5),
        ]

        for student, subject, value in grades_data:
            Grade.objects.create(student=student, subject=subject, value=value)

        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Permission

        ct = ContentType.objects.get_for_model(CustomUser)
        perm, _ = Permission.objects.get_or_create(
            codename='view_reports',
            content_type=ct,
            defaults={'name': 'Can view reports'},
        )
        director.user_permissions.add(perm)
        teacher1.user_permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('''
Тестовые данные созданы!
        '''))