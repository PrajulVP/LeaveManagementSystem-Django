from django.shortcuts import render, redirect, get_object_or_404
from .models import student, teacher, leave 
from django.contrib.auth import logout
from .forms import AddForm, TeacherForm, LeaveForm


# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
 

def student_login(request):
    return render(request, 'studentlogin.html')


def student_log(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cr = student.objects.filter(username=username, password=password)
        if cr:
            student_details=student.objects.get(username=username, password=password)
            
            username = student_details.username
            password = student_details.password

            request.session['username']=username
            request.session['password']=password

            return redirect('std_page')
        else:
            return render(request,'studentlogin.html')
    else:
        return render(request,'home.html')
    

def std_page(request):
    username = request.session['username']
    password = request.session['password']
    return render(request, 'studentpage.html',{'username':username,'password':password})


def std_details(request):
    username = request.session.get('username')
    std = student.objects.get(username=username)
    return render(request,'stddetails.html',{'std':std})


def update(request,pk):
    cr = student.objects.get(id=pk)
    form = AddForm(instance = cr)
    if request.method == "POST":
        form = AddForm(request.POST,instance = cr)
        if form.is_valid:
          form.save()
          return redirect("std_details")
    return render(request,'update.html',{'forms':form})


def add_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            username = request.session.get('username')
            Student = student.objects.get(username=username)
            leave = form.save(commit=False)
            leave.student = Student
            leave.save()
            return redirect('std_page')
    else:
        form = LeaveForm()
    return render(request, 'addleavereq.html', {'form': form})


def stdview_status(request):
    leaves = leave.objects.all()
    return render(request,'leavestatus.html',{'leaves':leaves})


def student_logout(request):
    logout(request)
    return redirect('student_login')


def teacher_reg(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registration successful... Your account is pending for approval!"
            return render(request, 'teacherreg.html', {'form': form, 'message': message})
    else:
        form = TeacherForm()
    return render(request, 'teacherreg.html', {'form': form})



def teacher_login(request):
    return render(request, 'teacherlogin.html')


def teacher_log(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cr = teacher.objects.filter(username=username, password=password)
        if cr:
            details = teacher.objects.get(username=username, password=password)
            
            username = details.username
            password = details.password
            department = details.department

            request.session['username']= username
            request.session['password']= password
            request.session['department']= department

            return redirect('teacher_page')
        else:
            return render(request,'teacherlogin.html')
    else:
        return render(request,'home.html')


def teacher_page(request):
    username = request.session['username']
    password = request.session['password']
    return render(request, 'teacherpage.html',{'username':username,'password':password})


def view_std(request):
    department = request.session.get('department') 
    if department:
        queryset = student.objects.filter(department=department)
        return render(request, 'viewstudent.html', {'students': queryset, 'department': department})
    else:
        return render(request, 'error_page.html', {'error_message': 'Department not found in session'})


def view_req(request):
        leaves = leave.objects.filter(status='Pending')
        return render(request, 'viewleavereq.html',{'leaves':leaves})
    

def approve_leave(request, username):
    Student = get_object_or_404(student, username=username)
    leave_request = leave.objects.filter(student=Student, status='Pending').first()
        
    if leave_request:
        leave_request.status = 'Approved'
        leave_request.save()
        return redirect('view_req')
    else:
        return render(request, 'teacherpage.html')


def teacher_logout(request):
    logout(request)
    return redirect('teacher_login')