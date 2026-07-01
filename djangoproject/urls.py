from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from corepython.admin_sites import director_site, teacher_site, student_site

urlpatterns = [
    # Три кабинета — отдельные AdminSite
    path('director/', director_site.urls),
    path('teacher/', teacher_site.urls),
    path('student/', student_site.urls),

    # Стандартный admin (для суперпользователя/разработки)
    path('admin/', admin.site.urls),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('corepython.urls')),
]