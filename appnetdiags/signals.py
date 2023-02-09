from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.core import signals
from django.http import JsonResponse, HttpRequest, HttpResponse
import time


@receiver(post_save, sender=Sector)
def post_save_sector(**kwargs):
    print('Группа создана')

@receiver(signals.request_finished)
def request_finished_hook(**kwargs):
    # time.sleep(5)
    print('Запрос выполнен')
    data1 = {'name': 'Name'}
    return JsonResponse(data1,safe=False)

