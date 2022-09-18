from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .algorithm import dataExtraction, defineTime, timeIndex, searching
from .models import faculty_details

# Create your views here.
def login(request):
    return render(request, 'main/login.html', {})

@login_required(login_url='/login')
def home(request):
    numbers = range(8, 18)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    depts = ["Computer Science and Engineering", "Electrical and Communications Engineering", "Mechanical Engineering", "Civil Engineering", "Biotechnology Engineering", "Chemical Engineering"]
    dayIndex = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
    context = {'numbers': numbers, 'days': days, 'depts': depts}

    if request.method == 'POST':
        # reqDept = request.POST['department']
        reqDayIndex = dayIndex[request.POST['requested_day']]
        reqTime = timeIndex(defineTime(request.POST))
        querySet = faculty_details.objects.all()

        context['eligibleEmps'] = searching(querySet, reqDayIndex, reqTime)

    return render(request, 'main/home.html', context)

@login_required(login_url='/login')
def fileInput(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        path = "media/"+ str(uploaded_file.name)
        dataExtraction(path)
        fs.delete(name)
        return HttpResponseRedirect('/')

    return render(request, 'main/fileInput.html', {})