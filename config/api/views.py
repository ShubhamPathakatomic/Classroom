from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import (
    Teacher,
    Student,
    Classroom,
    Subject,
    Department,
    BuildingFloor,
    Mark
)
from .serializers import (
    TeacherSerializer,
    StudentSerializer,
    ClassroomSerializer,
    SubjectSerializer,
    DepartmentSerializer,
    BuildingFloorSerializer,
    MarkSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
  
    queryset = Department.objects.all().prefetch_related('teachers')
    serializer_class = DepartmentSerializer

class BuildingFloorViewSet(viewsets.ModelViewSet):
   
    queryset = BuildingFloor.objects.all().prefetch_related('classrooms')
    serializer_class = BuildingFloorSerializer

class TeacherViewSet(viewsets.ModelViewSet):
   
    queryset = Teacher.objects.all().select_related('department', 'classroom_assigned')
    serializer_class = TeacherSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
   
    queryset = Classroom.objects.all().select_related('floor', 'teacher').prefetch_related('students')
    serializer_class = ClassroomSerializer

class StudentViewSet(viewsets.ModelViewSet):
   
    queryset = Student.objects.all().select_related('classroom').prefetch_related('subjects', 'friends', 'marks')
    serializer_class = StudentSerializer

class SubjectViewSet(viewsets.ModelViewSet):
  
    queryset = Subject.objects.all().prefetch_related('students_enrolled', 'marks')
    serializer_class = SubjectSerializer

class MarkViewSet(viewsets.ModelViewSet):
   
    queryset = Mark.objects.all().select_related('student', 'subject')
    serializer_class = MarkSerializer
