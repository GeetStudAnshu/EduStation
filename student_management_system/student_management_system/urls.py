
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views, hodviews, staffviews, studentviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('get_user_details/', views.get_user_details, name="get_user_details"),

    path('profile', views.PROFILE, name='profile'),
    path('profile/update', views.PROFILE_UPDATE, name='profile_update'),

    path('HOD/Home', hodviews.HOME, name='admin_home'),
    path('HOD/Student/Add',hodviews.ADD_STUDENT, name='add_student'),
    path('HOD/Student/View',hodviews.VIEW_STUDENT, name='view_student'),
    path('HOD/Student/Edit/<str:id>',hodviews.EDIT_STUDENT, name='edit_student'),
    path('HOD/Student/Update', hodviews.UPDATE_STUDENT, name='update_student'),
    path('HOD/Student/Delete/<str:admin>', hodviews.DELETE_STUDENT, name='delete_student'),



    path('HOD/Course/Add', hodviews.ADD_COURSE, name='add_course'),
    path('HOD/Course/View', hodviews.VIEW_COURSE, name='view_course'),
    path('HOD/Course/Edit/<str:id>', hodviews.EDIT_COURSE, name='edit_course'),
    path('HOD/Course/Update', hodviews.UPDATE_COURSE, name='update_course'),
    path('HOD/Course/Delete/<str:id>', hodviews.DELETE_COURSE, name='delete_course'),

    path('HOD/Staff/Add', hodviews.ADD_STAFF, name='add_staff'),
    path('HOD/Staff/View', hodviews.VIEW_STAFF, name='view_staff'),
    path('HOD/Staff/Edit/<str:id>', hodviews.EDIT_STAFF, name='edit_staff'),
    path('HOD/Staff/Update', hodviews.UPDATE_STAFF, name='update_staff'),
    path('HOD/Staff/Delete/<str:admin>', hodviews.DELETE_STAFF, name='delete_staff'),

    path('HOD/Subject/Add', hodviews.ADD_SUBJECT, name='add_subject'),
    path('HOD/Subject/View', hodviews.VIEW_SUBJECT, name='view_subject'),
    path('HOD/Subject/Edit/<str:id>', hodviews.EDIT_SUBJECT, name='edit_subject'),
    path('HOD/Subject/Update', hodviews.UPDATE_SUBJECT, name='update_subject'),
    path('HOD/Subject/Delete/<str:id>', hodviews.DELETE_SUBJECT, name='delete_subject'),

    path('HOD/Session/Add', hodviews.ADD_SESSION, name='add_session'),
    path('HOD/Session/View', hodviews.VIEW_SESSION, name='view_session'),
    path('HOD/Session/Edit/<str:id>', hodviews.EDIT_SESSION, name='edit_session'),
    path('HOD/Session/Update', hodviews.UPDATE_SESSION, name='update_session'),
    path('HOD/Session/Delete/<str:id>', hodviews.DELETE_SESSION, name='delete_session'),

    path('HOD/Staff/Send_Notification', hodviews.STAFF_SEND_NOTIFICATION, name='staff_send_notification'),
    path('HOD/Staff/Save_Notification', hodviews.SAVE_STAFF_NOTIFICATION, name='save_staff_notification'),

    path('HOD/Staff/Leave_View', hodviews.STAFF_LEAVE_VIEW, name='staff_leave_view'),
    path('HOD/Staff/Approve_Leave/<str:id>', hodviews.STAFF_APPROVE_LEAVE, name='staff_approve_leave'),
    path('HOD/Staff/Reject_Leave/<str:id>', hodviews.STAFF_REJECT_LEAVE, name='staff_reject_leave'),

    path('HOD/Staff/Feedback', hodviews.STAFF_FEEDBACK, name='staff_feedback_reply'),
    path('HOD/Staff/Feedback_Save', hodviews.STAFF_FEEDBACK_SAVE, name='staff_feedback_reply_save'),

    path('HOD/Student/Send_Notification', hodviews.STUD_SEND_NOTIFICATION, name='stud_send_notification'),
    path('HOD/Student/Save_Notification', hodviews.STUD_SAVE_NOTIFICATION,name='save_stud_notification'),


    path('HOD/Student/Feedback', hodviews.STUDENT_FEEDBACK, name='stud_feedback_reply'),
    path('HOD/Student/Feedback_Save', hodviews.STUDENT_FEEDBACK_SAVE, name='stud_feedback_reply_save'),


    path('HOD/Student/Leave_View', hodviews.STUD_LEAVE_VIEW, name='stud_leave_view'),
    path('HOD/Student/Approve_Leave/<str:id>', hodviews.STUD_APPROVE_LEAVE, name='stud_approve_leave'),
    path('HOD/Student/Reject_Leave/<str:id>', hodviews.STUD_REJECT_LEAVE, name='stud_reject_leave'),

    path('HOD/View_Attendance', hodviews.VIEW_ATTENDANCE, name='view_attendance'),

    path('HOD/Student/Collect_Fees', hodviews.COLLECT_FEES, name='collect_fees'),
    path('HOD/Student/View_Paid', hodviews.VIEW_PAID, name='view_paid'),

    path('HOD/Add_Vehicle', hodviews.ADD_TRANSPORT, name='add_transport'),
    path('HOD/View_Vehicle', hodviews.VIEW_TRANSPORT, name='view_transport'),
    path('HOD/Edit_Vehicle/<str:id>', hodviews.EDIT_TRANSPORT, name='edit_transport'),
    path('HOD/Update_Vehicle', hodviews.UPDATE_TRANSPORT, name='update_transport'),
    path('HOD/Delete_Vehicle/<str:admin>', hodviews.DELETE_TRANSPORT, name='delete_transport'),

# ############################################################################################################

    path('Staff/Home', staffviews.HOME, name='staff_home'),

    path('Staff/Notification', staffviews.NOTIFICATION, name='notification'),
    path('Staff/mark_as_done/<str:status>', staffviews.STAFF_NOTIFICATION_MARK_AS_DONE, name='staff_notification_mark_as_done'),

    path('Staff/Apply_Leave', staffviews.STAFF_APPLY_LEAVE, name='staff_apply_leave'),
    path('Staff/save_leave', staffviews.STAFF_SAVE_LEAVE, name='staff_save_leave'),

    path('Staff/Feedback', staffviews.STAFF_FEEDBACK, name='staff_feedback'),
    path('Staff/Feedback_Save', staffviews.SAVE_FEEDBACK, name='staff_save_feedback'),

    path('Staff/Take_Attendance', staffviews.STAFF_TAKE_ATTENDANCE, name='staff_take_attendance'),
    path('Staff/Save_Attendance', staffviews.STAFF_SAVE_ATTENDANCE, name='staff_save_attendance'),
    path('Staff/View_Attendance', staffviews.STAFF_VIEW_ATTENDANCE, name='staff_view_attendance'),

    path('Staff/Add_Result', staffviews.STAFF_ADD_RESULT, name='staff_add_result'),
    path('Staff/Save_Result', staffviews.STAFF_SAVE_RESULT, name='staff_save_result'),

# ############################################################################################################

    path('Student/Home', studentviews.HOME, name='student_home'),

    path('Student/Notification', studentviews.NOTIFICATION, name='stud_notification'),
    path('Student/mark_as_done/<str:status>', studentviews.STUD_NOTIFICATION_MARK_AS_DONE, name='stud_notification_mark_as_done'),

    path('Student/Feedback', studentviews.STUD_FEEDBACK, name='stud_feedback'),
    path('Student/Feedback_Save', studentviews.SAVE_FEEDBACK, name='stud_save_feedback'),

    path('Student/Apply_Leave', studentviews.STUD_APPLY_LEAVE, name='stud_apply_leave'),
    path('Student/Save_Leave', studentviews.STUD_SAVE_LEAVE, name='stud_save_leave'),

    path('Student/View_Attendance', studentviews.STUDENT_VIEW_ATTENDANCE, name='student_view_attendance'),

    path('Student/View_Result', studentviews.STUDENT_VIEW_RESULT, name='student_view_result'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
