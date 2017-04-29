from django.shortcuts import render
from django.http import HttpResponse
import time


def index(request):
    return HttpResponse("Hello, world. You're at the views index. It is currently " + time.strftime("%c"))
# Create your views here.
