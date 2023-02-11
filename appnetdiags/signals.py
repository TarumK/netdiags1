from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import render
#from .views import *
from .models import *
from django.core import signals
from django.http import JsonResponse, HttpRequest, HttpResponse, request
import time
from django.conf import settings
from django.db.models.signals import post_save



@receiver(post_save, sender=Sector)
def post_save_sector(**kwargs):
    print('Группа создана')
    # return HttpResponse("<script>alert('sdfsdfs');</script>")
    return {"message": "Группа создана"}

@receiver(signals.request_finished)
def request_finished_hook(sender, **kwargs):
    # time.sleep(5)
    print('Запрос выполнен')
    data1 = {"status": "1"}
    return {"message": "Группа создана"}

    # return render(request, 'index.html', {"data1": data1}, content_type="application/x-javascript")
    # return data1
    # return
    # return JsonResponse(data1,safe=False)


