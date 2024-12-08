document.addEventListener('DOMContentLoaded', () => {
    const prevWeekButton = document.getElementById('prev-week');
    const nextWeekButton = document.getElementById('next-week');

    // Получаем текущий offset из URL
    const currentPath = window.location.pathname;
    const offsetMatch = currentPath.match(/schedule\/(-?\d+)\//);
    let offset = offsetMatch ? parseInt(offsetMatch[1], 10) : 0;

    // Событие для кнопки "Предыдущая неделя"
    prevWeekButton.addEventListener('click', () => {
        window.location.href = `/schedule/${offset - 1}/`; // Сдвиг назад
    });

    // Событие для кнопки "Следующая неделя"
    nextWeekButton.addEventListener('click', () => {
        window.location.href = `/schedule/${offset + 1}/`; // Сдвиг вперед
    });

    // Удаление пары
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            const lessonId = e.target.dataset.id;
            const confirmed = confirm('Вы уверены, что хотите удалить эту пару?');

            if (confirmed) {
                try {
                    const response = await fetch(`/schedule/delete/${lessonId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        }
                    });

                    if (response.ok) {
                        window.location.reload(); // Перезагружаем страницу после удаления
                    } else {
                        alert('Ошибка при удалении пары.');
                    }
                } catch (error) {
                    console.error('Ошибка сети:', error);
                    alert('Произошла ошибка при удалении.');
                }
            }
        });
    });

    // Открытие модального окна
    const addLessonButton = document.getElementById('add-lesson-btn');
    const modal = document.getElementById('add-lesson-modal');
    const closeModalButton = document.getElementById('close-modal');
    
    // Проверим, существует ли кнопка
    if (addLessonButton) {
        addLessonButton.addEventListener('click', () => {
            console.log('Кнопка нажата');
            modal.classList.add('show');
        });
    }
    
    if (closeModalButton) {
        closeModalButton.addEventListener('click', () => {
            console.log('Закрыть модальное окно');
            modal.classList.remove('show');
        });
    }
    
    // Закрытие модального окна при клике вне его
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });
    
    // Обработка формы добавления пары
    const addLessonForm = document.getElementById('add-lesson-form');
    addLessonForm.addEventListener('submit', async (e) => {
        e.preventDefault();  // Не даем странице перезагрузиться
    
        const formData = new FormData(addLessonForm);
    
        try {
            const response = await fetch('/schedule/add/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
    
            if (response.ok) {
                console.log('Пара добавлена');
                window.location.reload();  // Перезагрузка страницы после успешного добавления
            } else {
                alert('Ошибка при добавлении пары.');
            }
        } catch (error) {
            console.error('Ошибка сети:', error);
            alert('Произошла ошибка при добавлении.');
        }
    });

    // Парсинг расписания с сайта
    const parseScheduleButton = document.getElementById('parse-schedule-btn');
    if (parseScheduleButton) {
        parseScheduleButton.addEventListener('click', async () => {
            try {
                const response = await fetch('/schedule/parse/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                const data = await response.json();
                if (response.ok) {
                    alert('Расписание успешно загружено!');
                    console.log(data.lessons);  // Выводим информацию о загруженных парах в консоль
                } else {
                    alert('Ошибка при загрузке расписания.');
                    console.error(data.error);
                }
            } catch (error) {
                console.error('Ошибка сети:', error);
                alert('Произошла ошибка при парсинге расписания.');
            }
        });
    }
});
