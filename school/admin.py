from django.contrib import admin
from school.models import *

# Register your models here.


class StudentGuardianInstanceInline(admin.TabularInline):
    model = StudentAndGuardian
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    inlines = [
        StudentGuardianInstanceInline,
    ]

    search_fields = [
        'first_name',
        'last_name'
    ]


class GuardianAdmin(admin.ModelAdmin):
    inlines = [
        StudentGuardianInstanceInline,
    ]

    search_fields = [
        'first_name',
        'last_name'
    ]

admin.site.register(Student,StudentAdmin)
admin.site.register(Guardian,GuardianAdmin)

admin.site.register(PickupSpot)
admin.site.register(GuardianPickupSpot)


admin.site.register(Relation)
admin.site.register(StudentAndGuardian)
admin.site.register(SchoolDetails)
admin.site.register(GuardiansLocation)
admin.site.register(NearestParents)
admin.site.register(PickedUpDroppedOff)