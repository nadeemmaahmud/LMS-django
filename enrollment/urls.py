from django.urls import path
from .views import enrolls

urlpatterns = [
    path('', enrolls, name="enrolls"),
]
