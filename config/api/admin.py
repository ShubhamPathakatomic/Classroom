from django.contrib import admin
from .models import (
        Teacher,
        Classroom,
        Student,
        Subject,
        Department,
        BuildingFloor,
        Mark
    )

admin.site.register(Department)
admin.site.register(BuildingFloor)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Mark)
