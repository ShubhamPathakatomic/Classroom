from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TeacherViewSet,
    StudentViewSet,
    ClassroomViewSet,
    SubjectViewSet,
    DepartmentViewSet,
    BuildingFloorViewSet,
    MarkViewSet,
)


router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'buildingfloors', BuildingFloorViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'marks', MarkViewSet)


urlpatterns = [  
    path('', include(router.urls)),             
]