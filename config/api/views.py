from rest_framework import viewsets
from rest_framework.decorators import action # Import 'action' decorator
from rest_framework.response import Response # Import 'Response'
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction # Import transaction for atomicity
from rest_framework import status
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
from .filters import ( 
    DepartmentFilter,
    BuildingFloorFilter,
    TeacherFilter,
    ClassroomFilter,
    SubjectFilter,
    StudentFilter,
    MarkFilter,
)




class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().prefetch_related('teachers')
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = DepartmentFilter      

class BuildingFloorViewSet(viewsets.ModelViewSet):
    queryset = BuildingFloor.objects.all().prefetch_related('classrooms')
    serializer_class = BuildingFloorSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = BuildingFloorFilter   


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().select_related('department', 'classroom_assigned')
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = TeacherFilter         


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all().select_related('floor', 'teacher').prefetch_related('students')
    serializer_class = ClassroomSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = ClassroomFilter       


class StudentViewSet(viewsets.ModelViewSet):
    
    queryset = Student.objects.all().select_related('classroom__floor', 'classroom__teacher', 'primary_subject').prefetch_related('friends', 'marks')
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = StudentFilter  

    
    @action(detail=False, methods=['post'], url_path='assign-primary-subject-bulk')
    def assign_primary_subject_bulk(self, request):
        """
        Custom action to assign a primary subject to multiple students in bulk.
        Expects 'subject_id' (int) and optionally 'student_ids' (list of int).
        If 'student_ids' is not provided, it assigns the subject to ALL students.
        """
        subject_id = request.data.get('subject_id')
        student_ids = request.data.get('student_ids') # Optional list of student IDs

        if subject_id is None:
            return Response(
                {"detail": "Subject ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get the Subject object
            subject_obj = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            return Response(
                {"detail": f"Subject with ID {subject_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        updated_count = 0
        with transaction.atomic(): # Ensure atomicity for the bulk update
            if student_ids:
                # Update only specified students
                students_to_update = self.get_queryset().filter(id__in=student_ids)
                updated_count = students_to_update.update(primary_subject=subject_obj)
            else:
                # Update all students
                updated_count = self.get_queryset().update(primary_subject=subject_obj)
        
        return Response(
            {"message": f"Successfully assigned primary subject '{subject_obj.name}' to {updated_count} student(s)."},
            status=status.HTTP_200_OK
        )       


class SubjectViewSet(viewsets.ModelViewSet):
    
    queryset = Subject.objects.all().prefetch_related('primary_students', 'marks')
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = SubjectFilter         


class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.all().select_related('student', 'subject')
    serializer_class = MarkSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_class = MarkFilter            

