import django_filters
from .models import (
    Teacher,
    Student,
    Classroom,
    Subject,
    Department,
    BuildingFloor,
    Mark
)

class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = {
            'name': ['exact', 'icontains'],
        }

class BuildingFloorFilter(django_filters.FilterSet):
    class Meta:
        model = BuildingFloor
        fields = {
            'name': ['exact', 'icontains'],
            'level': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }

class TeacherFilter(django_filters.FilterSet):
    department_name = django_filters.CharFilter(field_name='department__name', lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = {
            'name': ['exact', 'icontains'],
            'department': ['exact'],
        }

class ClassroomFilter(django_filters.FilterSet):
    floor_level = django_filters.NumberFilter(field_name='floor__level')
    teacher_name = django_filters.CharFilter(field_name='teacher__name', lookup_expr='icontains')

    class Meta:
        model = Classroom
        fields = {
            'name': ['exact', 'icontains'],
            'floor': ['exact'],
            'teacher': ['exact'],
        }

class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = Subject
        fields = {
            'name': ['exact', 'icontains'],
        }

class StudentFilter(django_filters.FilterSet):
    classroom_name = django_filters.CharFilter(field_name='classroom__name', lookup_expr='icontains')

    primary_subject_name = django_filters.CharFilter(field_name='primary_subject__name', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = {
            'name': ['exact', 'icontains'],
            'classroom': ['exact'],

            'primary_subject': ['exact'], 
            'friends': ['exact'],
        }

class MarkFilter(django_filters.FilterSet):
    student_name = django_filters.CharFilter(field_name='student__name', lookup_expr='icontains')
    subject_name = django_filters.CharFilter(field_name='subject__name', lookup_expr='icontains')

    class Meta:
        model = Mark
        fields = {
            'score': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'student': ['exact'],
            'subject': ['exact'],
        }
