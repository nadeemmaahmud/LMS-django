import os
from django.contrib.auth import get_backends
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from . models import Course, Category
from enrollment.models import Enrollment, Batch
from users.models import CustomUser
from django.urls import reverse
from decimal import Decimal
from sslcommerz_python_api import SSLCSession
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login

def home(request):
    return render(request, 'index.html')

def courses(request):
    categories = Category.objects.all() 
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses, 'categories': categories})

def course_details(request, id):
    course = get_object_or_404(Course, id=id)
    already_enrolled = False
    if request.user.is_authenticated:
        already_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    return render(request, "course_details.html", {'course': course, 'already_enrolled': already_enrolled})

def payment(request, id):
    mypayment = SSLCSession(
    sslc_is_sandbox=True,
    sslc_store_id=os.environ.get('sslc_store_id'),
    sslc_store_pass=os.environ.get('sslc_store_pass')
    )

    status_url = request.build_absolute_uri(reverse('payment_status', kwargs={'id': id}))

    mypayment.set_urls(
    success_url=status_url,
    fail_url=status_url,
    cancel_url=status_url,
    ipn_url=status_url
    )

    course = get_object_or_404(Course, id=id)

    mypayment.set_product_integration(
    total_amount=Decimal(course.price),
    currency='BDT',
    product_category=course.category,
    product_name=course.title,
    num_of_item=2,
    shipping_method='YES',
    product_profile='None'
    )

    user = get_object_or_404(CustomUser, id=request.user.id)

    mypayment.set_customer_info(
    name=user,
    email=user.email if user.email else 'N/A',
    address1=user.address_line_1 if user.address_line_1 else 'N/A',
    address2=user.address_line_1 if user.address_line_1 else 'N/A',
    city='N/A',
    postcode='N/A',
    country='N/A',
    phone='01715666904',
    )

    mypayment.set_shipping_info(
    shipping_to='demo customer',
    address='demo address',
    city='Dhaka',
    postcode='1209',
    country='Bangladesh'
    )

    
    mypayment.set_additional_values(
    value_a=user.id,
    #value_b='portalcustomerid',
    #value_c='1234',
    #value_d='uuid'
    )

    response_data = mypayment.init_payment()

    gateway_url = response_data.get('GatewayPageURL')
    if gateway_url:
        return redirect(gateway_url)
    else:
        error_message = response_data.get('failedreason', 'Payment gateway initialization failed. Please try again later.')
        return HttpResponse(error_message, status=500)

@csrf_exempt
def payment_status(request, id):
    if request.method == "POST":
        status = request.POST.get('status')
        
        if status == 'VALID':
            user = request.POST.get('value_a')
            user = get_object_or_404(CustomUser, id=user)
            course = get_object_or_404(Course, id=id)
            batch = get_object_or_404(Batch, number=0)
            
            enrollment = Enrollment.objects.create(user=user, course=course, batch=batch)
            enrollment.save()
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user)
        else:
            print(f"Payment failed for course ID: {id}. Status: {status}")
    else:
        print("Invalid request method. Only POST requests are allowed.")

    return redirect('enrolls')