from django.contrib import admin
from school.models import *

# Register your models here.

admin.site.register(Student)
admin.site.register(Guardian)
admin.site.register(Relation)
admin.site.register(StudentAndGuardian)
admin.site.register(SchoolDetails)
admin.site.register(GuardiansLocation)
admin.site.register(NearestParents)
admin.site.register(PickedUpDroppedOff)