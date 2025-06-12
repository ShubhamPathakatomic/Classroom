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
    department = SimpleDepartmentSerializer(read_only=True)
    classroom_assigned = SimpleClassroomSerializer(read_only=True) 

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'department', 'classroom_assigned']


class ClassroomSerializer(serializers.ModelSerializer):
    floor = SimpleBuildingFloorSerializer(read_only=True)
    teacher = SimpleTeacherSerializer(read_only=True)
    students = SimpleStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'floor', 'teacher', 'students']

class SubjectSerializer(serializers.ModelSerializer):

    primary_students = SimpleStudentSerializer(many=True, read_only=True) 
    marks = serializers.StringRelatedField(many=True, read_only=True) 

    class Meta:
        model = Subject
        fields = ['id', 'name', 'primary_students', 'marks']

class StudentSerializer(serializers.ModelSerializer):
    classroom = SimpleClassroomSerializer(read_only=True)
    
 
    primary_subject = SimpleSubjectSerializer(read_only=True) 

    primary_subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='primary_subject',
        write_only=True,         
        allow_null=True          
    )
    
   
    
    friends = SimpleStudentSerializer(many=True, read_only=True)
    marks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Student
       
        fields = ['id', 'name', 'classroom', 'primary_subject', 'primary_subject_id', 'friends', 'marks']

class MarkSerializer(serializers.ModelSerializer):
    student = SimpleStudentSerializer(read_only=True)
    subject = SimpleSubjectSerializer(read_only=True)

    class Meta:
        model = Mark
        fields = ['id', 'student', 'subject', 'score']
