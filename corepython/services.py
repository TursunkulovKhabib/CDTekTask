from django.db import connection
from django.db.models import Avg

from .models import Grade


class ReportService:
    @staticmethod
    def get_student_report(student_id: int) -> list[dict]:
        return list(
            Grade.objects
            .filter(student_id=student_id)
            .select_related('student__user', 'student__group', 'subject')
            .values(
                'student__user__last_name',
                'student__user__first_name',
                'student__group__name',
                'subject__name',
            )
            .annotate(avg_grade=Avg('value'))
            .order_by(
                '-student__group__name',
                '-student__user__last_name',
                '-student__user__first_name',
            )
        )

    # Попробовал переписать на Grade.objects.raw
    @staticmethod
    def get_group_report(group_id: int) -> list[dict]:
        sql = """
              SELECT gr.id, 
                     g.name        AS group_name, 
                     s.name        AS subject_name, 
                     AVG(gr.value) AS avg_grade
              FROM corepython_grade gr
              INNER JOIN corepython_student st ON gr.student_id = st.id
              INNER JOIN corepython_group g ON st.group_id = g.id
              INNER JOIN corepython_subject s ON gr.subject_id = s.id
              WHERE g.id = %s
              GROUP BY g.name, s.name
              ORDER BY s.name 
           """
        results = Grade.objects.raw(sql, [group_id])
        return [
            {
                'group_name': row.group_name,
                'subject_name': row.subject_name,
                'avg_grade': row.avg_grade,
            }
            for row in results
        ]