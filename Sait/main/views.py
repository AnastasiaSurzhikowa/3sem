from django.shortcuts import render, redirect
from datetime import date, timedelta, time
from django.http import JsonResponse
from .models import Lesson, Task

import requests
from bs4 import BeautifulSoup


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
