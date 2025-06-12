from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class BuildingFloor(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()

    class Meta:
        verbose_name = "Building Floor"
        verbose_name_plural = "Building Floors"
        unique_together = ('name', 'level')
        ordering = ['level']
    
    def __str__(self):
        return f"{self.name} - Level {self.level}"

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    def __str__(self):
        return self.name
    

class Classroom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    floor = models.ForeignKey(BuildingFloor, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.OneToOneField(Teacher, on_delete=models.SET_NULL,null=True,blank=True, related_name='classroom_assigned')

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
    

    primary_subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL, 
        null=True, blank=True,    
        related_name='primary_students' 
    )
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    def __str__(self):
        return self.name
    

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='marks')
    score = models.PositiveIntegerField(
        help_text="Score out of 100",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('student', 'subject')
    
    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.score}"