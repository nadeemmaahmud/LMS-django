from django.urls import path
from . views import home, courses, course_details, payment, payment_status

urlpatterns = [
    path('', home, name="home"),
    path('courses/', courses, name="courses"),
    path('course_details/<int:id>/', course_details, name="course_details"),
    path('payment/<int:id>/', payment, name="payment"),
    path('payment/sslc/status/<int:id>', payment_status, name="payment_status")
]
