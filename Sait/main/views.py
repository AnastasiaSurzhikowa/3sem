from django.shortcuts import render, redirect
from datetime import date, timedelta, time, datetime
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

#парсинг

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.http import JsonResponse
from .models import Lesson

def parse_schedule(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)

    url = "https://guap.ru/rasp/?g=319"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({'error': f'Failed to fetch the schedule: {e}'}, status=500)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Ищем div с классом "result"
    result_div = soup.find('div', class_='result')
    if not result_div:
        return JsonResponse({'error': 'No schedule data found in the result section.'}, status=404)

    # Словарь для преобразования дня недели
    day_map = {
        "Понедельник": "ПН",
        "Вторник": "ВТ",
        "Среда": "СР",
        "Четверг": "ЧТ",
        "Пятница": "ПТ",
        "Суббота": "СБ",
        "Воскресенье": "ВС",
    }

    # Находим все теги h3 внутри div с классом result
    days = result_div.find_all("h3")
    if not days:
        return JsonResponse({'error': 'No schedule data found on the page.'}, status=404)

    # Игнорируем первый тег h3
    if days:
        days[0].decompose()  # Удаляем первый h3

    created_count = 0

    for day in days:
        day_name = day_map.get(day.text.strip(), None)
        if not day_name:
            continue

        lessons = day.find_next_siblings("h4")
        for lesson in lessons:
            # Игнорируем элементы с тегом legend
            if lesson.find("legend"):
                continue

            time_info = lesson.text.strip()
            try:
                # Разделяем начало и конец времени
                time_range = time_info.split(" (")[1].replace(")", "").split("–")
                start_time = datetime.strptime(time_range[0].strip(), "%H:%M").time()
                end_time = datetime.strptime(time_range[1].strip(), "%H:%M").time()
            except Exception as e:
                print(f"Ошибка при обработке времени: {e}")
                continue

            study_info = lesson.find_next("div", class_="study")
            if not study_info:
                continue

            subject = study_info.find("b").next_sibling.strip().strip('–" ')
            room = study_info.find("em").text.strip()
            lesson_type = study_info.find("b").text.strip()

            # Проверка четности недели
            week_parity_tag = study_info.find("b", class_="dn")
            week_parity = "Б"  # None для обычной недели
            if week_parity_tag:
                week_parity = "Н"  # Нечетная неделя
            elif study_info.find("b", class_="up"):
                week_parity = "Ч"  # Четная неделя

            # Проверяем, существует ли уже такой урок
            if not Lesson.objects.filter(
                user=request.user,
                day=day_name,
                start_time=start_time,
                end_time=end_time,
            ).exists():
                # Создаём новый урок, если его ещё нет
                Lesson.objects.create(
                    user=request.user,
                    day=day_name,
                    start_time=start_time,
                    end_time=end_time,
                    subject=subject,
                    room=room,
                    lesson_type=lesson_type,
                    week_parity=week_parity,
                )
                created_count += 1

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