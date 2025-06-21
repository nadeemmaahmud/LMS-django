from django.shortcuts import render
from .models import Enrollment, Batch

def enrolls(request):
    enroll = Enrollment.objects.all()
    return render(request, 'enrolls.html', {'enrolls': enroll})
