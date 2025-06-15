import os
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from . models import Course, Category

from decimal import Decimal
from sslcommerz_python_api import SSLCSession

def home(request):
    return render(request, 'index.html')

def courses(request):
    categoryes = Category.objects.all() 
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses':courses, 'categoryes':categoryes})

def course_details(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "course_details.html", {'course':course})

def payment(request):
    mypayment = SSLCSession(
    sslc_is_sandbox=True,
    sslc_store_id=os.environ.get('sslc_store_id'),
    sslc_store_pass=os.environ.get('sslc_store_pass')
    )

    status_url = request.build_absolute_uri('sslc/status')

    mypayment.set_urls(
    success_url=status_url,
    fail_url=status_url,
    cancel_url=status_url,
    ipn_url=status_url
    )

    enroll = Course.objects.get(request, id=id)

    mypayment.set_product_integration(
    total_amount=Decimal(enroll.price),
    currency='BDT',
    product_category=enroll.category,
    product_name=enroll.title,
    num_of_item=2,
    shipping_method='YES',
    product_profile='None'
    )

    mypayment.set_customer_info(
    name='Nadim Mahmud',
    email='nadeemmaahmud@email.com',
    address1='Chakipara, Bagha',
    address2='Rajshahi, Bangladesh',
    city='Rajshahi', postcode='6280',
    country='Bangladesh',
    phone='01715666904'
    )

    mypayment.set_shipping_info(
    shipping_to='demo customer',
    address='demo address',
    city='Dhaka',
    postcode='1209',
    country='Bangladesh'
    )

    ''' If you want to post some additional values
    mypayment.set_additional_values(
    value_a='cusotmer@email.com',
    value_b='portalcustomerid',
    value_c='1234',
    value_d='uuid'
    )'''

    response_data = mypayment.init_payment()

    # You can Print the response data
    print(response_data)

    return redirect(response_data['GatewayPageURL'])

def payment_status(request):
    return HttpResponse('Payment status page')