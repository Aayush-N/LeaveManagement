from django.contrib import admin
from .models import LeaveType
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, LeaveTaken, TempLeaveType

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class MyUserAdmin(UserAdmin):
    inlines = [
        UserProfileInline,
    ]

admin.site.register(LeaveType)
admin.site.register(TempLeaveType)
admin.site.register(LeaveTaken)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)