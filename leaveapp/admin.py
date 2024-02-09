from django.contrib import admin
from .models import student, teacher

# Register your models here.

admin.site.register(student)

class teacherAdmin(admin.ModelAdmin):
    list_display = ['firstname','lastname','username','password','email','age','phonenumber','address','department','approved']
    list_filter = ['approved']
    actions = ['approve_staff']

    def approve_staff(self, request, queryset):
        queryset.update(approved=True)
    approve_staff.short_description = "Approve selected staff members"

admin.site.register(teacher, teacherAdmin)