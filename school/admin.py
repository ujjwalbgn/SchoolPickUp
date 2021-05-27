from django.contrib import admin
from school.models import Student, Guardian, Relation,StudentAndGuardian

# Register your models here.

admin.site.register(Student)
admin.site.register(Guardian)
admin.site.register(Relation)
admin.site.register(StudentAndGuardian)