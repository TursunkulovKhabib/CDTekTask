from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        DIRECTOR = 'director', 'Директор'
        TEACHER = 'teacher', 'Учитель'
        STUDENT = 'student', 'Студент'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'

    @property
    def is_director(self):
        return self.role == self.Role.DIRECTOR

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название группы')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Subject(models.Model):

    name = models.CharField(max_length=100, verbose_name='Название предмета')
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': CustomUser.Role.TEACHER},
        related_name='subjects',
        verbose_name='Учитель',
    )

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Role.STUDENT},
        related_name='student_profile',
        verbose_name='Пользователь',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='Группа',
    )

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f'{self.user.get_full_name()} — {self.group}'


class Grade(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Студент',
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='Предмет',
    )
    value = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка',
    )
    date = models.DateField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['student', 'subject']),
        ]
        permissions = [
            ('can_view_reports', 'Может просматривать отчёты'),
        ]

    def __str__(self):
        return f'{self.student} | {self.subject} | {self.value}'