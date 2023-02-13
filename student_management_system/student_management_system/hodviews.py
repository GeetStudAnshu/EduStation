from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import Courses, SessionYearModel, CustomUser, Students, Staffs, Subjects, NotificationStaffs, LeaveReportStaff, FeedBackStaffs, NotificationStudent, FeedBackStudent, LeaveReportStudent, Attendance, AttendanceReport, Stud_Fee, Transport



@login_required(login_url='/')
def HOME(request):
    stud_count = Students.objects.all().count()
    fac_count = Staffs.objects.all().count()
    course_count = Courses.objects.all().count()
    subject_count = Subjects.objects.all().count()

    student_gender_male = Students.objects.filter(gender='Male').count()
    student_gender_female = Students.objects.filter(gender='Female').count()
    student_gender_other = Students.objects.filter(gender='Others').count()

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_code)
        student_count_list_in_subject.append(student_count)

    # //Staff Attendance Data Goes Here
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []

    staffs = Staffs.objects.all()
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # //Student Attendance Data Goes Here
    student_attendance_present_list = []
    student_attendance_leave_list = []
    student_name_list = []
    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves)
        student_name_list.append(student.admin.first_name)

    context = {
        'stud_count': stud_count,
        'subject_count': subject_count,
        'course_count': course_count,
        'fac_count': fac_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
        'student_gender_other': student_gender_other,
        'student_count_list_in_course': student_count_list_in_course,
        'course_name_list': course_name_list,
        'subject_list': subject_list,
        'student_count_list_in_subject': student_count_list_in_subject,
        'student_attendance_present_list': student_attendance_present_list,
        'student_attendance_leave_list': student_attendance_leave_list,
        'student_name_list': student_name_list,
        'staff_name_list': staff_name_list,
        'staff_attendance_leave_list': staff_attendance_leave_list,
        'staff_attendance_present_list': staff_attendance_present_list,
    }
    return render(request, 'hod/home.html', context)


@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Courses.objects.all()
    session_year = SessionYearModel.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already in use!')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already in use!')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            course = Courses.objects.get(id=course_id)
            session_year = SessionYearModel.objects.get(id=session_year_id)

            student = Students(
                admin=user,
                address=address,
                session_year_id=session_year,
                course_id=course,
                gender=gender,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + " is Successfully Added!")
            return redirect('add_student')

    context = {
        'course': course,
        'session_year': session_year,
    }

    return render(request, 'hod/add_student.html', context)


@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Students.objects.all()

    context = {
        'student': student,
    }

    return render(request, 'hod/view_student.html', context)


@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    student = Students.objects.filter(id=id)
    course = Courses.objects.all
    session_year = SessionYearModel.objects.all

    context = {
        'student': student,
        'course': course,
        'session_year': session_year
    }
    return render(request, 'hod/edit_student.html', context)


@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        # print(student_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id=student_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        user.save()

        student = Students.objects.get(admin=student_id)
        student.address = address
        student.gender = gender

        course = Courses.objects.get(id=course_id)
        student.course_id = course

        session_year = SessionYearModel.objects.get(id=session_year_id)
        student.session_year_id = session_year

        student.save()
        messages.success(request, 'Details Updated Successfully!')
        return redirect('view_student')
    return render(request, 'hod/edit_student.html')


@login_required(login_url='/')
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request, 'Details Deleted Successfully!')
    return redirect('view_student')


@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course_fees = request.POST.get('course_fees')
        course = Courses(
            course_name=course_name,
            course_fees=course_fees,
        )
        course.save()
        messages.success(request, 'Course Saved to the System!')
        return redirect('add_course')
    return render(request, 'hod/add_course.html')


@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Courses.objects.all()

    context = {
        'course': course
    }
    return render(request, 'hod/view_course.html', context)


@login_required(login_url='/')
def EDIT_COURSE(request, id):
    course = Courses.objects.get(id=id)

    context = {
        'course': course
    }
    return render(request, 'hod/edit_course.html', context)


@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        fees = request.POST.get('fees')
        course = Courses.objects.get(id=course_id)
        course.course_name = name
        course.course_fees = fees
        course.save()
        messages.success(request, 'Course has been updated!')
        return redirect('view_course')

    return render(request, 'hod/edit_course.html')


@login_required(login_url='/')
def DELETE_COURSE(request, id):
    course = Courses.objects.get(id=id)
    course.delete()
    messages.success(request, 'Course Deleted Successfully!')
    return redirect('view_course')


@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Already Exists!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Already Exists!')
            return redirect('add_staff')

        else:
            user = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email,
                              profile_pic=profile_pic, user_type=2)
            user.set_password(password)
            user.save()

            staff = Staffs(
                admin=user,
                address=address,
                gender=gender
            )
            staff.save()
            messages.success(request, "Staff is Successfully Added!")
            return redirect('add_staff')

    return render(request, 'hod/add_staff.html')


@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staffs.objects.all()

    context = {
        'staff': staff,
    }
    return render(request, 'hod/view_staff.html', context)


@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staffs.objects.get(id=id)
    context = {
        'staff': staff,
    }
    return render(request, 'hod/edit_staff.html', context)


@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id=staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        staff = Staffs.objects.get(admin=staff_id)
        staff.address = address
        staff.gender = gender

        staff.save()
        messages.success(request, 'Details Updated Successfully!')
        return redirect('view_staff')

    return render(request, 'hod/edit_staff.html')


@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Details Deleted Successfully!')
    return redirect('view_staff')


@login_required(login_url='/')
def ADD_SUBJECT(request):
    course = Courses.objects.all()
    staff = Staffs.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Courses.objects.get(id = course_id)
        staff = Staffs.objects.get(id=staff_id)
        print(staff)

        subject = Subjects(
            subject_name = subject_name,
            subject_code = subject_code,
            course_id = course,
            staff_id = staff,
        )
        subject.save()
        messages.success(request, 'Subject Saved Successfully!')
        return redirect('add_subject')


    context = {
        'course':course,
        'staff':staff,
    }
    return render(request, 'hod/add_subject.html', context)


@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subjects.objects.all()

    context = {
        'subject': subject,
    }
    return render(request, 'hod/view_subject.html', context)


@login_required(login_url='/')
def EDIT_SUBJECT(request, id):
    subject = Subjects.objects.get(id=id)
    course = Courses.objects.all()
    staff = Staffs.objects.all()
    context = {
        'subject': subject,
        'course':course,
        'staff':staff,
    }
    return render(request, 'hod/edit_subject.html', context)


@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            subject.subject_code = subject_code

            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            staff = Staffs.objects.get(id=staff_id)
            subject.staff_id = staff

            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            return redirect('view_subject')

        except:
            messages.error(request, "Failed to Update Subject.")
            return redirect('edit_subject')


@login_required(login_url='/')
def DELETE_SUBJECT(request, id):
    subject = Subjects.objects.get(id=id)
    subject.delete()
    messages.success(request, 'Subject Deleted Successfully!')
    return redirect('view_subject')


@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = SessionYearModel(
            session_start_year = session_year_start,
            session_end_year = session_year_end,
        )
        session.save()
        messages.success(request, 'Session Stored Successfully!')
        return redirect('add_session')
    return render(request, 'hod/add_session.html')


@login_required(login_url='/')
def VIEW_SESSION(request):
    session = SessionYearModel.objects.all()

    context = {
        'session': session,
    }
    return render(request, 'hod/view_session.html', context)


@login_required(login_url='/')
def EDIT_SESSION(request, id):
    session = SessionYearModel.objects.filter(id = id)
    context = {
        'session': session,
    }
    return render(request, 'hod/edit_session.html', context)


@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_year_id = request.POST.get('session_id')
        start_date = request.POST.get('session_year_start')
        end_date = request.POST.get('session_year_end')

        session = SessionYearModel(
            id = session_year_id,
            session_start_year = start_date,
            session_end_year = end_date,
        )
        session.save()
        messages.success(request, 'Session Year(s) Altered Successfully!')

    return redirect('view_session')


@login_required(login_url='/')
def DELETE_SESSION(request, id):
    session = SessionYearModel.objects.get(id=id)
    session.delete()
    messages.success(request, 'Session Year Deleted Successfully!')
    return redirect('view_session')


@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staffs.objects.all()
    see_notification = NotificationStaffs.objects.all().order_by('-id')[0:5]
    context = {
        'staff':staff,
        'see_notification':see_notification,
    }
    return render(request, 'hod/send_staff_notification.html', context)


@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staffs.objects.get(admin = staff_id)
        notification = NotificationStaffs(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request, 'Notification Sent!')
        return redirect('staff_send_notification')


@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
    leave_data = LeaveReportStaff.objects.all()

    context = {
        'leave_data':leave_data,
    }
    return render(request, 'hod/staff_leave.html', context)


@login_required(login_url='/')
def STAFF_APPROVE_LEAVE(request,id):
    leave = LeaveReportStaff.objects.get(id = id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


@login_required(login_url='/')
def STAFF_REJECT_LEAVE(request, id):
    leave = LeaveReportStaff.objects.get(id = id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    feedback = FeedBackStaffs.objects.all()

    context = {
        'feedback':feedback
    }
    return render(request, 'hod/staff_feedback.html', context)


@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = FeedBackStaffs.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        messages.success(request,'Reply has been sent!')
        return redirect('staff_feedback_reply')


@login_required(login_url='/')
def STUD_SEND_NOTIFICATION(request):
    student = Students.objects.all()
    see_notification = NotificationStudent.objects.all().order_by('-id')[0:5]
    context = {
        'student':student,
        'see_notification':see_notification,
    }
    return render(request, 'hod/stud_notification.html', context)


@login_required(login_url='/')
def STUD_SAVE_NOTIFICATION(request):
    if request.method == "POST":
        stud_id = request.POST.get('stud_id')
        message = request.POST.get('message')

        stud = Students.objects.get(admin=stud_id)
        notification = NotificationStudent(
            student_id=stud,
            message=message,
        )
        notification.save()
        messages.success(request, 'Notification Sent!')
        return redirect('stud_send_notification')

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    feedback = FeedBackStudent.objects.all()
    context = {
        'feedback': feedback
    }
    return render(request, 'hod/stud_feedback.html', context)

@login_required(login_url='/')
def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = FeedBackStudent.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        messages.success(request,'Reply has been sent!')
        return redirect('stud_feedback_reply')


@login_required(login_url='/')
def STUD_LEAVE_VIEW(request):
    leave_data = LeaveReportStudent.objects.all()

    context = {
        'leave_data': leave_data,
    }
    return render(request, 'hod/stud_leave.html', context)

@login_required(login_url='/')
def STUD_APPROVE_LEAVE(request, id):
    leave = LeaveReportStudent.objects.get(id=id)
    leave.leave_status = 1
    leave.save()
    return redirect('stud_leave_view')

@login_required(login_url='/')
def STUD_REJECT_LEAVE(request, id):
    leave = LeaveReportStudent.objects.get(id=id)
    leave.leave_status = 2
    leave.save()
    return redirect('stud_leave_view')


@login_required(login_url='/')
def VIEW_ATTENDANCE(request):

    subject = Subjects.objects.all()
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

            get_subject = Subjects.objects.get(id=subject_id)
            get_session_year = SessionYearModel.objects.get(id=session_year_id)

            attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = AttendanceReport.objects.filter(attendance_id=attendance_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report,
    }
    return render(request, 'hod/view_attendance.html', context)


@login_required(login_url='/')
def COLLECT_FEES(request):
    stud_id = Students.objects.all()
    if request.method == "POST":
        stud = request.POST.get('stud')
        fee_amt = request.POST.get('fee_amt')
        pay_meth = request.POST.get('pay_meth')
        fee_ref = request.POST.get('ref_num')
        student = Students.objects.get(id=stud)

        fees = Stud_Fee(
            stud_id=student,
            fee_amount=fee_amt,
            fee_type=pay_meth,
            fee_ref=fee_ref,
            fee_stat=1,
        )
        fees.save()
        messages.success(request, 'Fees Collected Successfully!')
        return redirect('collect_fees')
    context = {
        'stud_id': stud_id,
    }
    return render(request, 'hod/collect_fees.html', context)


@login_required(login_url='/')
def VIEW_PAID(request):
    fee_det = Stud_Fee.objects.all()
    context = {
        'fee_det': fee_det,
    }
    return render(request, 'hod/view_paid.html', context)


@login_required(login_url='/')
def ADD_TRANSPORT(request):

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cell_no = request.POST.get('cell_no')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        vehicle_no = request.POST.get('vehicle_no')
        vehicle_type = request.POST.get('vehicle_type')
        aadhar = request.FILES.get('aadhar')
        puc = request.FILES.get('puc')
        rc = request.FILES.get('rc')
        dl = request.FILES.get('dl')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already in use!')
            return redirect('add_transport')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already in use!')
            return redirect('add_transport')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=4
            )
            user.set_password(password)
            user.save()
        if Transport.objects.filter(cell_no=cell_no).exists():
            messages.warning(request, 'Phone Number Exists!')
            return redirect('add_transport')
        else:
            driver = Transport(
                admin=user,
                address=address,
                gender=gender,
                cell_no=cell_no,
                vehicle_no=vehicle_no,
                vehicle_type=vehicle_type,
                aadhar=aadhar,
                dl=dl,
                rc=rc,
                puc=puc,
            )
            driver.save()
            messages.success(request, user.first_name + "  " + user.last_name + " is Successfully Added!")
            return redirect('add_transport')

    return render(request, 'hod/add_transport.html')


@login_required(login_url='/')
def VIEW_TRANSPORT(request):
    transport = Transport.objects.all()

    context = {
        'transport':transport,
    }
    return render(request, 'hod/view_transport.html', context)


@login_required(login_url='/')
def UPDATE_TRANSPORT(request):
    if request.method == "POST":
        driver_id = request.POST.get('driver_id')
        #print(driver_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cell_no = request.POST.get('cell_no')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        vehicle_no = request.POST.get('vehicle_no')
        vehicle_type = request.POST.get('vehicle_type')
        aadhar = request.FILES.get('aadhar')
        dl = request.FILES.get('dl')
        rc = request.FILES.get('rc')
        puc = request.FILES.get('puc')

        driver = CustomUser.objects.get(id=driver_id)

        driver.first_name = first_name
        driver.last_name = last_name
        driver.email = email
        driver.username = username
        driver.save()

        if password != None and password != "":
            driver.set_password(password)
        if profile_pic != None and profile_pic != "":
            driver.profile_pic = profile_pic
        if dl != None and dl != "":
            driver.dl = dl
        if aadhar != None and aadhar != "":
            driver.aadhar = aadhar
        if puc != None and puc != "":
            driver.puc = puc
        if rc != None and rc != "":
            driver.rc = rc

        driver_info = Transport.objects.get(admin=driver_id)
        driver_info.address = address
        driver_info.gender = gender
        driver_info.cell_no = cell_no
        driver_info.vehicle_type = vehicle_type
        driver_info.vehicle_no = vehicle_no

        driver_info.save()
        messages.success(request, "Driver has been Updated!")
        return redirect('view_transport')
    return render(request, 'hod/edit_transport.html')


@login_required(login_url='/')
def EDIT_TRANSPORT(request, id):
    transport = Transport.objects.filter(id=id)

    context = {
        'transport':transport,
    }
    return render(request, 'hod/edit_transport.html', context)


@login_required(login_url='/')
def DELETE_TRANSPORT(request, admin):
    driver = CustomUser.objects.get(id=admin)
    driver.delete()
    messages.success(request, 'Details Deleted Successfully!')
    return redirect('view_transport')

