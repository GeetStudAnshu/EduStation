from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import Attendance, Courses, Students, NotificationStudent, FeedBackStudent, LeaveReportStudent, Subjects, AttendanceReport, \
    StudentResult


@login_required(login_url='/')
def HOME(request):
    student_obj = Students.objects.get(admin=request.user.id)
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    subjects = Subjects.objects.filter(course_id=student_obj.course_id)
    subjects_count = Subjects.objects.filter(course_id=student_obj.course_id).count()
    leaves_taken = LeaveReportStudent.objects.filter(student_id=student_obj, leave_status=1).count()
    feedbacks_given = FeedBackStudent.objects.all().count()


    # Fetch the subject exam and assignment marks with subject names for the logged-in student
    results = StudentResult.objects.filter(student_id=student_obj.id).select_related('subject_id')

    # Extract the subject exam marks and subject names from the results
    subject_exam_marks = [result.subject_exam_marks for result in results]
    subject_assignment_marks = [result.subject_assignment_marks for result in results]
    subject_names = [result.subject_id.subject_code for result in results]

    # For Attendance Data PIE CHART
    data_present = []
    data_leave = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_2 = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,
                                                                   student_id=student_obj.id).count()
        data_leave_count = LeaveReportStudent.objects.filter(student_id=student_obj, leave_status=1).count()
        data_present.append(attendance_present_2)
        data_leave.append(data_leave_count)

    # For Attendance Per Subject
    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    data_present_2 = []

    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,
                                                                   student_id=student_obj.id).count()
        subject_name.append(subject.subject_code)
        data_present_2.append(attendance_present_count)
    context = {
        'student_obj': student_obj,
        'feedbacks_given': feedbacks_given,
        'attendance_present': attendance_present,
        'subjects_count': subjects_count,
        'leaves_taken': leaves_taken,
        'data_leave_count': data_leave_count,
        'data_leave': data_leave,
        'total_subjects': total_subjects,
        'subject_name': subject_name,
        'data_present_2': data_present_2,
        'subject_names': subject_names,
        'subject_exam_marks': subject_exam_marks,
        'subject_assignment_marks': subject_assignment_marks,
    }
    return render(request, 'student/home.html', context)


@login_required(login_url='/')
def NOTIFICATION(request):
    stud = Students.objects.filter(admin=request.user.id)
    for i in stud:
        stud_id = i.id
        notification = NotificationStudent.objects.filter(student_id=stud_id)
        context = {
            'notification': notification,
        }
        return render(request, 'student/notification.html', context)


@login_required(login_url='/')
def STUD_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = NotificationStudent.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('stud_notification')


@login_required(login_url='/')
def STUD_FEEDBACK(request):
    stud_id = Students.objects.get(admin=request.user.id)
    feedback_history = FeedBackStudent.objects.filter(student_id=stud_id)
    context = {
        'feedback_history': feedback_history,
    }
    return render(request, 'student/stud_feedback.html', context)


@login_required(login_url='/')
def SAVE_FEEDBACK(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        stud = Students.objects.get(admin=request.user.id)
        feedback = FeedBackStudent(
            student_id=stud,
            feedback=feedback,
            feedback_reply="",
        )
        feedback.save()
        messages.success(request, 'Feedback has been sent!')
        return redirect('stud_feedback')


@login_required(login_url='/')
def STUD_APPLY_LEAVE(request):
    stud = Students.objects.filter(admin=request.user.id)
    for i in stud:
        stud_id = i.id

        student_leave_history = LeaveReportStudent.objects.filter(student_id=stud_id)

        context = {
            'student_leave_history': student_leave_history,
        }
        return render(request, 'student/apply_leave.html', context)


@login_required(login_url='/')
def STUD_SAVE_LEAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_reason = request.POST.get('leave_reason')
        stud = Students.objects.get(admin=request.user.id)
        leave = LeaveReportStudent(
            student_id=stud,
            leave_date=leave_date,
            leave_message=leave_reason,
        )
        leave.save()
        messages.success(request, 'Leave has been applied!')
        return redirect('stud_apply_leave')


def STUDENT_VIEW_ATTENDANCE(request):
    student = Students.objects.get(admin=request.user.id)
    subjects = Subjects.objects.filter(course_id=student.course_id)
    action = request.GET.get('action')

    get_subject = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subjects.objects.get(id=subject_id)

            # attendance = Attendance.objects.get(id = subject_id)
            attendance_report = AttendanceReport.objects.filter(student_id=student,
                                                                attendance_id__subject_id=subject_id)

    context = {
        'subjects': subjects,
        'action': action,
        'get_subject': get_subject,
        'attendance_report': attendance_report,
    }
    return render(request, 'student/view_attendance.html', context)


def STUDENT_VIEW_RESULT(request):
    mark = None
    student = Students.objects.get(admin=request.user.id)
    result = StudentResult.objects.filter(student_id=student)

    for i in result:
        assignment_mark = i.subject_assignment_marks
        exam_mark = i.subject_exam_marks

        mark = assignment_mark + exam_mark
        print(mark)

    context = {
        'result': result,
        'mark': mark,
    }
    return render(request, 'student/view_result.html', context)
