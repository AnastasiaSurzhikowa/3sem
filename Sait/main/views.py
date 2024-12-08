from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.http import JsonResponse
from .models import Lesson


def about(request):
    return render(request, 'main/about.html')

def testpic(request):
    return render(request, 'main/testpic.html')

def calendar(request):
    return render(request, 'main/calendar.html')

def mainpage(request):
    return render(request, 'main/mainpage.html')

def contact(request):
    return render(request, 'main/about.html')

def deadline(request):
    return render(request, 'main/deadline.html')

def calendar2(request):
    return render(request, 'main/calendar2.html')

def get_start_of_week(today):
    start = today - timedelta(days=today.weekday())
    return start

def schedule_view1(request, offset="0"):
    """Обрабатывает отображение расписания."""
    try:
        offset = int(offset)  # Преобразуем строку в число
    except ValueError:
        offset = 0  # Если значение некорректное, сбросить на 0

    today = date(2024, 12, 8)  # Начальная точка (суббота)
    start_of_week = today + timedelta(weeks=offset)
    parity = (offset % 2 == 0)  # Четность недели: True = четная, False = нечетная

    # Список дней недели
    days = [
        (start_of_week + timedelta(days=i), day)
        for i, day in enumerate(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'])
    ]

    # Получаем все уроки для нужной недели и сортируем их по дням недели и времени
    lessons = Lesson.objects.filter(week_parity=parity).order_by('day', 'start_time')

    # Создаем словарь для уроков по дням недели
    lessons_by_day = {day: [] for day in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']}
    for lesson in lessons:
        lessons_by_day[lesson.day].append(lesson)

    # Передаем в контекст словарь с уроками по дням
    context = {
        'days': days,
        'lessons_by_day': lessons_by_day,  # Здесь уже передаются уроки для каждого дня
        'offset': offset,  # Передаём текущий offset в шаблон
        'parity': 'Чётная' if parity else 'Нечётная',  # Четность недели
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
    Lesson.objects.filter(id=lesson_id).delete()
    return JsonResponse({'success': True})



def schedule_view(request):
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
            return render(request, 'main/contact.html', {'schedule_html': result_element.prettify() })
        else:
            return render(request, 'main/contact.html', {'schedule_html': 'Элемент с классом "result" не найден.'})

    except requests.exceptions.RequestException as e:
        # Обработка ошибок, например, при сетевых проблемах
        return render(request, 'main/contact.html', {'schedule_html': f'Ошибка при запросе: {str(e)}'})
