from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Staffs, Courses, NotificationStaffs, LeaveReportStaff, FeedBackStaffs, Subjects, SessionYearModel, Attendance, AttendanceReport, Students, StudentResult
from django.contrib import messages


def HOME(request):
    staff = get_object_or_404(Staffs, admin=request.user)
    # total_students = Students.objects.filter(course_id=staff.course).count()
    # print(total_students)
    total_leave = LeaveReportStaff.objects.filter(staff_id=staff).count()
    subjects = Subjects.objects.filter(staff_id=staff)
    total_subject = subjects.count()
    attendance_list = Attendance.objects.filter(subject_id__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject_id=subject).count()
        subject_list.append(subject.subject_code)
        attendance_list.append(attendance_count)

    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    final_course = []
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    students_count = Students.objects.filter(course_id__in=final_course).count()

    # spline-chart-1
    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(student_id=student.id).count()
        student_list.append(student.admin.first_name + " " + student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
    print(student_list, student_list_attendance_present)
    context = {
        'students_count': students_count,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list,
        'student_list': student_list,
        'student_list_attendance_present': student_list_attendance_present,
    }

    return render(request, 'staff/home.html', context)


@login_required(login_url='/')
def NOTIFICATION(request):
    staff = Staffs.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        notification = NotificationStaffs.objects.filter(staff_id = staff_id)
        context = {
            'notification':notification,
        }
        return render(request, 'staff/notification.html',context)


@login_required(login_url='/')
def STAFF_NOTIFICATION_MARK_AS_DONE(request, status):
    notification = NotificationStaffs.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notification')


@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff = Staffs.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id

        staff_leave_history = LeaveReportStaff.objects.filter(staff_id = staff_id)

        context = {
            'staff_leave_history':staff_leave_history,
        }
        return render(request, 'staff/apply_leave.html', context)


@login_required(login_url='/')
def STAFF_SAVE_LEAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_reason = request.POST.get('leave_reason')
        staff = Staffs.objects.get(admin = request.user.id)
        leave = LeaveReportStaff(
            staff_id = staff,
            leave_date = leave_date,
            leave_message = leave_reason,
        )
        leave.save()
        messages.success(request, 'Leave has been applied!')
        return redirect('staff_apply_leave')


@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    staff_id = Staffs.objects.get(admin = request.user.id)
    feedback_history = FeedBackStaffs.objects.filter(staff_id = staff_id)
    context = {
        'feedback_history':feedback_history,
    }
    return render(request, 'staff/staff_feedback.html', context)


@login_required(login_url='/')
def SAVE_FEEDBACK(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        staff = Staffs.objects.get(admin = request.user.id)
        feedback = FeedBackStaffs (
            staff_id = staff,
            feedback = feedback,
            feedback_reply = "",
        )
        feedback.save()
        messages.success(request, 'Feedback has been sent!')
        return redirect('staff_feedback')


def STAFF_TAKE_ATTENDANCE(request):
    staff_id = Staffs.objects.get(admin=request.user.id)

    subject = Subjects.objects.filter(staff_id=staff_id)
    session_year = SessionYearModel.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subjects.objects.get(id=subject_id)
            get_session_year = SessionYearModel.objects.get(id=session_year_id)

            subject = Subjects.objects.filter(id=subject_id)
            for i in subject:
                student_id = i.course_id.id
                students = Students.objects.filter(course_id=student_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'action': action,
        'students': students,
    }
    return render(request, 'staff/take_attendance.html', context)


def STAFF_SAVE_ATTENDANCE(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        students_id = request.POST.getlist('students_id')
        get_subject = Subjects.objects.get(id=subject_id)
        get_session_year = SessionYearModel.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id = get_subject,
            attendance_date = attendance_date,
            session_year_id = get_session_year,
        )
        attendance.save()

        for i in students_id:
            stud_id = i
            int_stud = int(stud_id)
            p_students = Students.objects.get(id = int_stud)
            attendance_report = AttendanceReport(
                student_id = p_students,
                attendance_id = attendance,
                status = True,
            )
            attendance_report.save()
        messages.success(request, 'Attendance(s) are recorded!')
    return redirect('staff_take_attendance')


def STAFF_VIEW_ATTENDANCE(request):
    staff_id = Staffs.objects.get(admin = request.user.id)
    subject = Subjects.objects.filter(staff_id = staff_id)
    session_year = SessionYearModel.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subjects.objects.get(id = subject_id)
            get_session_year = SessionYearModel.objects.get(id = session_year_id)

            attendance = Attendance.objects.filter(subject_id = get_subject, attendance_date = attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = AttendanceReport.objects.filter(attendance_id = attendance_id)



    context = {
        'subject':subject,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'attendance_date':attendance_date,
        'attendance_report':attendance_report,
    }
    return render(request, 'staff/view_attendance.html', context)


def STAFF_ADD_RESULT(request):
    staff = Staffs.objects.get(admin=request.user.id)
    subjects = Subjects.objects.filter(staff_id=staff)
    session_year = SessionYearModel.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    assignment_marks = None


    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subjects.objects.get(id=subject_id)
            get_session = SessionYearModel.objects.get(id=session_year_id)

            subjects = Subjects.objects.filter(id=subject_id)
            for i in subjects:
                stud_id = i.course_id.id
                students = Students.objects.filter(course_id=stud_id)
    context = {
        'subjects': subjects,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'students': students,
    }

    return render(request, 'staff/add_result.html', context)


def STAFF_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        stud_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('Exam_mark')

        total = int(assignment_mark) + int(Exam_mark)

        get_student = Students.objects.get(admin=stud_id)
        get_subject = Subjects.objects.get(id=subject_id)

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, stud_id=get_student)
            result.subject_assignment_marks = assignment_mark
            result.subject_exam_marks = Exam_mark
            result.total = total
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('staff_add_result')
        else:
            result = StudentResult(student_id=get_student, subject_id=get_subject, subject_exam_marks=Exam_mark,
                                   subject_assignment_marks=assignment_mark, total=total)
            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('staff_add_result')