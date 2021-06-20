from django.contrib import admin
from school.models import Student, Guardian, Relation,StudentAndGuardian, SchoolDetails, GuardiansLocation,NearestParents

# Register your models here.

admin.site.register(Student)
admin.site.register(Guardian)
admin.site.register(Relation)
admin.site.register(StudentAndGuardian)
admin.site.register(SchoolDetails)
admin.site.register(GuardiansLocation)
admin.site.register(NearestParents)