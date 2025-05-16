from django.http import HttpResponse
from django.urls import path

def hello(request):
    return HttpResponse("Hello from Django!")

urlpatterns = [
    path("", hello),
]