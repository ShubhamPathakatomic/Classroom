from rest_framework import serializers
from .models import (
    Teacher,
    Student,
    Classroom,
    Subject,
    Department,
    BuildingFloor,
    Mark
)

class SimpleDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class SimpleBuildingFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingFloor
        fields = ['id', 'name', 'level']

class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']

class SimpleClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name']

class SimpleSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    teachers = SimpleTeacherSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = ['id', 'name', 'teachers']

class BuildingFloorSerializer(serializers.ModelSerializer):
    classrooms = SimpleClassroomSerializer(many=True, read_only=True)
    class Meta:
        model = BuildingFloor
        fields = ['id', 'name', 'level', 'classrooms']

class TeacherSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    classroom_assigned = SimpleClassroomSerializer(read_only=True) 

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'department', 'classroom_assigned']


class ClassroomSerializer(serializers.ModelSerializer):
    floor = serializers.PrimaryKeyRelatedField(queryset=BuildingFloor.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), allow_null=True)

    students = SimpleStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'floor', 'teacher', 'students']

class SubjectSerializer(serializers.ModelSerializer):
    students_enrolled = SimpleStudentSerializer(many=True, read_only=True)
    marks = serializers.StringRelatedField(many=True, read_only=True) 

    class Meta:
        model = Subject
        fields = ['id', 'name', 'students_enrolled', 'marks']

class StudentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True, required=False)
    friends = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True, required=False)

    marks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'name', 'classroom', 'subjects', 'friends', 'marks']

class MarkSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Mark
        fields = ['id', 'student', 'subject', 'score']
