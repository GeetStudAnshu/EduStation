from django.shortcuts import render, redirect
from app.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from app.models import CustomUser


def BASE(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')

            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')

            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')

            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')


def doLogout(request):
    logout(request)
    return redirect('login')


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


@login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')
        print(profile_pic)
        try:
            customUser = CustomUser.objects.get(id=request.user.id)
            customUser.first_name = first_name
            customUser.last_name = last_name
            if password != None and password != "":
                customUser.set_password(password)
            if profile_pic != None and profile_pic != "":
                customUser.profile_pic = profile_pic
            customUser.save()
            messages.success(request, 'User Profile Updated!')
            return redirect('profile')
        except:
            messages.error(request, 'User Profile Update Failed!')

    return render(request, 'profile.html')