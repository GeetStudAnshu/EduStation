from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username', 'user_type']


admin.site.register(CustomUser, UserModel)
admin.site.register(Courses)
admin.site.register(SessionYearModel)
admin.site.register(Students)
admin.site.register(Staffs)
admin.site.register(Subjects)
admin.site.register(NotificationStaffs)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationStudent)
admin.site.register(FeedBackStudent)
admin.site.register(LeaveReportStudent)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(StudentResult)
admin.site.register(Stud_Fee)
admin.site.register(Transport)
