from django.shortcuts import render, redirect
from datetime import date, timedelta, time
from django.http import JsonResponse
from .models import Lesson, Task

import requests
from bs4 import BeautifulSoup


def about(request):
    return render(request, 'main/about.html')

def parse(request):
    return render(request, 'main/parse.html')

def deadline(request):
    return render(request, 'main/deadline.html')

def calendar(request):
    return render(request, 'main/calendar.html')

def calendar2(request):
    return render(request, 'main/calendar2.html')

def get_start_of_week(today):
    start = today - timedelta(days=today.weekday())
    return start

def schedule_view(request, offset="0"):
    try:
        offset = int(offset)
    except ValueError:
        offset = 0

    today = date.today()  # Текущая дата

    # Определяем, сколько дней нужно отнять, чтобы получить понедельник этой недели
    start_of_week = today - timedelta(days=today.weekday())  # Понедельник текущей недели

    # Если offset больше 0, смещаем на нужное количество недель
    start_of_week += timedelta(weeks=offset)

    # Номер недели и чётность недели
    week_number = start_of_week.isocalendar()[1]  # Номер недели
    parity = (week_number % 2 == 0)  # Четность недели

    # Список дней недели с датами
    days = [
        {
            'date': start_of_week + timedelta(days=i),
            'day_name': day
        }
        for i, day in enumerate(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'])
    ]

    lessons = Lesson.objects.filter(week_parity=parity, user=request.user).order_by('day', 'start_time')

    # Сортируем уроки по дням недели
    lessons_by_day = {day['day_name']: [] for day in days}
    for lesson in lessons:
        lessons_by_day[lesson.day].append(lesson)

    context = {
        'days': days,  # Список дней с датами
        'lessons_by_day': lessons_by_day,
        'offset': offset,
        'parity': 'Чётная' if parity else 'Нечётная',
    }

    return render(request, 'main/schedule.html', context)

def add_lesson(request):
    if request.method == 'POST':
        # Получение данных из запроса
        subject = request.POST.get('subject')
        room = request.POST.get('room')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        lesson_type = request.POST.get('lesson_type')
        day = request.POST.get('day')
        week_parity = request.POST.get('week_parity') == 'true'  # Преобразование строки в boolean

        # Создание урока
        lesson = Lesson.objects.create(
            user=request.user,
            subject=subject,
            room=room,
            start_time=start_time,
            end_time=end_time,
            lesson_type=lesson_type,
            day=day,
            week_parity=week_parity
        )

        # Возврат JSON-ответа для AJAX-запросов
        return JsonResponse({'success': True, 'lesson_id': lesson.id})

    # Если метод GET — можно вернуть страницу добавления или редирект
    return redirect('schedule')

def delete_lesson(request, lesson_id):
    Lesson.objects.filter(id=lesson_id, user=request.user).delete()
    return JsonResponse({'success': True})

#Задания

def task_view(request, offset="0"):
    try:
        offset = int(offset)
    except ValueError:
        offset = 0

    today = date.today()  # Текущая дата

    # Определяем, сколько дней нужно отнять, чтобы получить понедельник этой недели
    start_of_week = today - timedelta(days=today.weekday())  # Понедельник текущей недели

    # Если offset больше 0, смещаем на нужное количество недель
    start_of_week += timedelta(weeks=offset)

    # Номер недели и чётность недели
    week_number = start_of_week.isocalendar()[1]  # Номер недели
    parity = (week_number % 2 == 0)  # Четность недели

    # Список дней недели с датами
    days = [
        {
            'date': start_of_week + timedelta(days=i),
            'day_name': day
        }
        for i, day in enumerate(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'])
    ]

    # Получаем задания для текущей недели
    tasks = Task.objects.filter(
        user=request.user,
        date__gte=start_of_week,
        date__lt=start_of_week + timedelta(days=7)
    ).order_by('date')

    # Группируем задания по дате
    tasks_by_day = {day['date']: [] for day in days}
    for task in tasks:
        tasks_by_day[task.date].append(task)

    context = {
        'days': days,  # Список дней с датами
        'tasks_by_day': tasks_by_day,
        'offset': offset,
        'parity': 'Чётная' if parity else 'Нечётная',
    }

    return render(request, 'main/tasks.html', context)

def add_task(request):
    if request.method == 'POST':
        # Получение данных из запроса
        subject = request.POST.get('subject')
        descriptions = request.POST.get('descriptions')
        date = request.POST.get('date')  # Получаем только дату
        
        # Создание задания
        task = Task.objects.create(
            subject=subject,
            descriptions=descriptions,
            user=request.user,
            date=date,  # Сохраняем только дату
        )

        # Возврат JSON-ответа для AJAX-запросов
        return JsonResponse({'success': True, 'task_id': task.id})

    # Если метод GET — можно вернуть страницу добавления или редирект
    return redirect('tasks')

def delete_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return JsonResponse({'success': True})

#парсинг

URL = "https://guap.ru/rasp/?g=319"

def parse_schedule():
    # Получаем HTML страницу
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Находим все теги h3 с днями недели
    days = soup.find_all('h3')
    
    for day in days:
        day_name = day.get_text(strip=True)
        
        # Пропускаем, если нет дней недели в расписании
        if day_name not in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
            continue
        
        # Находим все пары в этот день
        lessons = day.find_next_siblings('div')  # Находим все div'ы, идущие после h3
        
        for lesson in lessons:
            # Ищем время начала и конца пары
            time_tag = lesson.find('h4')
            if time_tag:
                start_time, end_time = parse_time(time_tag.get_text(strip=True))
            
            # Ищем тип недели (четная/нечетная)
            week_parity = True  # По умолчанию четная неделя
            if lesson.find('b', class_='dn'):
                week_parity = False
            elif lesson.find('b', class_='up'):
                week_parity = True
            else:
                week_parity = None  # Если ничего не указано, на обе недели
            
            # Получаем название предмета

            # Получаем аудиторию
            room_tag = lesson.find('em')
            if room_tag:
                room = room_tag.get_text(strip=True)
            
            # Ищем тип занятия
            lesson_type_tag = lesson.find('b')
            if lesson_type_tag:
                lesson_type = lesson_type_tag.get_text(strip=True)
            
            # Сохраняем данные в модель Lesson
            lesson_obj = Lesson(
                day=day_name[:2],  # Сохраняем только первые две буквы дня недели
                week_parity=week_parity,
                subject=subject,
                room=room,
                start_time=start_time,
                end_time=end_time,
                lesson_type=lesson_type
            )
            lesson_obj.save()

def parse_time(time_str):
    # Преобразуем строку времени в объекты time
    start_time_str, end_time_str = time_str.split(' - ')
    start_time = time(*map(int, start_time_str.split(':')))
    end_time = time(*map(int, end_time_str.split(':')))
    return start_time, end_time

def parse_view(request):
    group_value = "317"
    group_value1 = "12312"  # Инициализация переменной по умолчанию
    
    # Получаем группу пользователя
    if request.user.is_authenticated:
        group_value = request.user.group
        group_value1 = str(group_value)
    
    url = "https://guap.ru/rasp/?g=" + group_value1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем на ошибку HTTP

        soup = BeautifulSoup(response.text, 'html.parser')
        result_element = soup.find(class_='result')

        if result_element:
            # Удаляем элементы с классом 'legend'
            for legend in result_element.find_all(class_='legend'):
                legend.decompose()

            # Отправляем очищенный HTML в шаблон
            return render(request, 'main/parse.html', {'schedule_html': result_element.prettify() })
        else:
            return render(request, 'main/parse.html', {'schedule_html': 'Элемент с классом "result" не найден.'})

    except requests.exceptions.RequestException as e:
        # Обработка ошибок, например, при сетевых проблемах
        return render(request, 'main/parse.html', {'schedule_html': f'Ошибка при запросе: {str(e)}'})