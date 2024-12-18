from django.shortcuts import render, redirect
from datetime import date, timedelta, time, datetime
from django.http import JsonResponse
from .models import Lesson, Task, Event

import requests
import re
from bs4 import BeautifulSoup

def get_start_of_week(today):
    start = today - timedelta(days=today.weekday())
    return start

def schedule_view(request, offset="0"):
    try:
        offset = int(offset)
    except ValueError:
        offset = 0

    today = date.today()

    # Начало недели
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week += timedelta(weeks=offset)

    # Номер недели и чётность
    week_number = start_of_week.isocalendar()[1]
    parity = (week_number % 2 == 0)

    days = [
        {'date': start_of_week + timedelta(days=i), 'day_name': day}
        for i, day in enumerate(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'])
    ]

    # Уроки для текущей недели
    if parity:
        lessons = Lesson.objects.filter(week_parity__in=['Ч', 'Б'], user=request.user)
    else:
        lessons = Lesson.objects.filter(week_parity__in=['Н', 'Б'], user=request.user)

    lessons_by_day = {day['day_name']: [] for day in days}
    for lesson in lessons:
        lessons_by_day[lesson.day].append(lesson)

    context = {
        'days': days,
        'lessons_by_day': lessons_by_day,
        'offset': offset,
        'parity': 'Чётная' if parity else 'Нечётная',
    }

    return render(request, 'main/schedule.html', context)

def add_lesson(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        room = request.POST.get('room')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        lesson_type = request.POST.get('lesson_type')
        day = request.POST.get('day')
        week_parity = request.POST.get('week_parity')  # 'Ч', 'Н', 'Б'

        # Добавление пары
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

        return JsonResponse({'success': True, 'lesson_id': lesson.id})

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

#Дедлайны

def event_view(request, offset="0"):
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
    events = Event.objects.filter(
        user=request.user,
        date__gte=start_of_week,
        date__lt=start_of_week + timedelta(days=7)
    ).order_by('date')

    # Группируем задания по дате
    events_by_day = {day['date']: [] for day in days}
    for event in events:
        events_by_day[event.date].append(event)

    context = {
        'days': days,  # Список дней с датами
        'events_by_day': events_by_day,
        'offset': offset,
        'parity': 'Чётная' if parity else 'Нечётная',
    }

    return render(request, 'main/deadline.html', context)

def add_event(request):
    if request.method == 'POST':
        # Получение данных из запроса
        subject = request.POST.get('subject')
        descriptions = request.POST.get('descriptions')
        date = request.POST.get('date')  # Получаем только дату
        
        # Создание задания
        event = Event.objects.create(
            subject=subject,
            descriptions=descriptions,
            user=request.user,
            date=date,  # Сохраняем только дату
        )

        # Возврат JSON-ответа для AJAX-запросов
        return JsonResponse({'success': True, 'event_id': event.id})

    # Если метод GET — можно вернуть страницу добавления или редирект
    return redirect('events')

def delete_event(request, event_id):
    Event.objects.filter(id=event_id).delete()
    return JsonResponse({'success': True})

def parse_schedule(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)
    
    if request.method == 'POST' and request.user.is_authenticated:
        # Очистить все записи модели Lesson для текущего пользователя
        Lesson.objects.filter(user=request.user, is_parse =True).delete()

    group_value = "31745345234" 
    # Получаем группу пользователя
    if request.user.is_authenticated:
        group_value = str(request.user.group)
    
    url = "https://guap.ru/rasp/?g=" + group_value

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch the schedule: {e}'}, status=500)

    soup = BeautifulSoup(response.content, 'html.parser')

    result_div = soup.find('div', class_='result')
    if not result_div:
        return JsonResponse({'error': 'No schedule data found in the result section.'}, status=404)

    day_map = {
        "Понедельник": "ПН",
        "Вторник": "ВТ",
        "Среда": "СР",
        "Четверг": "ЧТ",
        "Пятница": "ПТ",
        "Суббота": "СБ",
        "Воскресенье": "ВС",
    }

    days = result_div.find_all("h3")
    if not days:
        return JsonResponse({'error': 'No schedule data found on the page.'}, status=404)

    if days:
        if str(days[0]) == (str("вне сетки расписания (—)")):
            days[0].decompose()

    created_count = 0

    for day in days:
        day_name = day_map.get(day.text.strip(), None)
        if not day_name:
            continue

        # Сохраняем все элементы до следующего h3 (новый день недели)
        current = day.find_next_sibling()
        while current and current.name != "h3":
            if current.name == "h4":
                # Извлекаем информацию о времени
                time_info = current.text.strip()
                time_range = re.findall(r"(\d{1,2}:\d{2})–(\d{1,2}:\d{2})", time_info)
                if time_range:
                    start_time, end_time = time_range[0]
                    start_time = datetime.strptime(start_time, "%H:%M").time()
                    end_time = datetime.strptime(end_time, "%H:%M").time()
                else:
                    current = current.find_next_sibling()
                    continue

                # Обрабатываем все теги <div class="study">, которые следуют за <h4>
                study_element = current.find_next_sibling()
                while study_element and study_element.name == "div" and "study" in study_element.get("class", []):
                    study_info = study_element

                    # Извлекаем данные из study_info
                    week_parity = (
                        "Ч" if study_info.find("b", class_="up") else
                        "Н" if study_info.find("b", class_="dn") else
                        "Б"
                    )
                    if study_info.find("b").text.strip() in ["▼", "▲"]:
                        lesson_type = study_info.find("b").find_next("b").text.strip()
                        subject = study_info.find("b").find_next("b").next_sibling.strip().strip('–" ') if study_info.find("b") else "Неизвестно"
                    else:
                        lesson_type = study_info.find("b").text.strip() if study_info.find("b") else "Неизвестно"
                        subject = study_info.find("b").next_sibling.strip().strip('–" ') if study_info.find("b") else "Неизвестно"
                    room = study_info.find("em").text.strip().strip('–" ') if study_info.find("em") else "Неизвестно"

                    # Проверяем существование записи перед созданием
                    if not Lesson.objects.filter(
                        user=request.user,
                        day=day_name,
                        start_time=start_time,
                        end_time=end_time,
                        week_parity=week_parity,
                    ).exists():
                        Lesson.objects.create(
                            user=request.user,
                            day=day_name,
                            start_time=start_time,
                            end_time=end_time,
                            subject=subject,
                            room=room,
                            is_parse=True,
                            lesson_type=lesson_type,
                            week_parity=week_parity,
                        )
                        created_count += 1

                    study_element = study_element.find_next_sibling()  # Переход к следующему элементу

            current = current.find_next_sibling()

    return JsonResponse({
        'success': 'Schedule parsed successfully.',
        'created': created_count,
    }, status=200)

def clear_lessons(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # Очистить все записи модели Lesson для текущего пользователя
        Lesson.objects.filter(user=request.user).delete()
        return JsonResponse({'success': 'Все занятия успешно удалены!'})
    
    return JsonResponse({'error': 'Ошибка запроса или недостаточно прав.'}, status=400)
