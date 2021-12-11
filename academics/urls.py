from django.urls import path
from .views import(AcademicScheduleView, ProfsAndHODsView, StudyMaterialsView)

urlpatterns = [path('academics/academic-schedule/<str:dept>/<int:year>/',
                    AcademicScheduleView.as_view()),
               path('academics/study-materials/<str:dept>/',
                    StudyMaterialsView.as_view()),
               path('academics/profs/<str:dept>/', ProfsAndHODsView.as_view()), ]
