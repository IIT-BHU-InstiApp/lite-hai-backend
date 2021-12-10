from django.urls import path
from .views import(AcademicScheduleView, ProffsAndHODsView, StudyMaterialsView)

urlpatterns = [path('academics/academic-schedule/<int:pk>/',
                    AcademicScheduleView.as_view()),
               path('academics/study-materials/',
                    StudyMaterialsView.as_view()),
               path('academics/proffs/<int:pk>', ProffsAndHODsView.as_view()), ]
