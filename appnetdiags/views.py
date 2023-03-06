from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import Sector, Server, Log
from .forms import MyForm
from ping3 import ping, verbose_ping
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from matplotlib import pyplot as plt
# import appnetdiags.signals
import time



def index(request):
    message=""
    # host_list = []
    if request.method == "POST":
# Если нажата кнопка "Отправить", то из POST-потока формы получаем количество отправляемых пакетов
# и размер пакета
        packet_count = int(request.POST.get('packet_count'))
        packet_size = int(request.POST.get('packet_size'))
        # server_name = request.POST.get('server_name')
        # # host_list = t_s
# Поочередно, в цикле выбираем хосты из глобального списка серверов t_s,
# закрепленных за подразделением и стравливаем (передаем) ее на вход
# в качестве аргумента функции hostping()
        for host in t_s:
            print(host)
            list_vozrata = hostping(host, packet_count, packet_size)
# Возвращаем из функции hostping количество вернувшихся пакетов, среднее время отклика и т.д.
            ping_count1 = list_vozrata[0]
            average1 = list_vozrata[1]
            current_host = host
# Создаем экземпляр класса модели Log, где накапливаются данные по доступности хостов
# записываем в таблицу логов данные
            log = Log()
            log.log_host = host
            log.log_ping_count = ping_count1
            log.log_ping_size = packet_size
            log.log_average = average1
            log.save()
            # message = "Запрос завершен"
# Создаем экземпляр формы, связанной с моделю Log для передачи его в шаблон index.html
# в качестве параметра функции прорисовки render()
#         form = MyForm(request.POST)
            form = MyForm()

    else:
# Это часть отрабатывает, если мы просто запустили хомячок-домашнюю страницу и ничего не передали
# Проше говоря, не нажали на кнопку submit "Запустить тест"
        ping_count1 = 0
        average1 = 0
        current_host = []
        form = MyForm()

        allrec = Log.objects.all()
        paginator = Paginator(allrec, 12)
        page_number = request.GET.get('page')
        items = paginator.get_page(page_number)


        return render(request, 'index.html', {'allrec': allrec, 'form': form, 'items': items})
# Выбираем все записи логов, пользуясь ORM-кой, а не чистым SQL. Типа, это SELECT * FROM Log
    allrec = Log.objects.all()
    paginator = Paginator(allrec, 12)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    context = {'allrec': allrec, 'form': form, 'items': items, 'ping_count1': ping_count1,
               'packet_size': packet_size, 'average1': average1,
                'host': current_host, "message": message}

# Отрисовываем шаблон с данными, полученными с функциональных представлений вьюхи
    return render(request, 'index.html', context=context )


def get_server_list(request, sector_id):
    global t_s
    servers = Server.objects.filter(sector=sector_id)
    server_list = []
    t_s = []
    for server in servers:
        server_list.append({'id': server.id, 'name': server.name})
        t_s.append(server.name)
    print ('spisok serverov', t_s)
    print(type(t_s))
    return JsonResponse(server_list, safe=False)

def hostping(host, packet_count, packet_size):
    average = 0
    time_response = 0
    ping_count = packet_count         #Количество отправляемых пакетов

    lost_count = 0          #Количество потерянных пакетов
    # size_package = 128       #Размер отправляемых пакетов в байтах
    for count in range(1, ping_count + 1):
        time_response = ping(host, size=packet_size, unit='s')
        # time.sleep(0.1)
        if time_response is not False:
            average = average + time_response
        else:
            lost_count += 1
    sr = average/ping_count
    return [ping_count, sr, packet_size]

def log_chart(request):
    servers = Server.objects.all()
    for server in servers:
        logs = Log.objects.filter(log_host=server)
        avg_time = []
        date_value = []
        for log in logs:
            avg_time.append(log.log_average)
            date_value.append(log.log_date.hour)
        print(avg_time)
        plt.plot(date_value, avg_time)
        plt.xlabel('Дата и время')
        plt.ylabel('Ср. время отклика')
        plt.title('Диаграмма доступности веб-серверов')
    plt.show()
    return HttpResponseRedirect('/')
def about(request):
    return render(request, 'about.html')

def feedback(request):
    return render(request, 'feedback.html')