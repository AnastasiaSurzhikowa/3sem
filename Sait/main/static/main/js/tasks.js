document.addEventListener('DOMContentLoaded', () => {
    const prevWeekButton = document.getElementById('prev-week');
    const nextWeekButton = document.getElementById('next-week');

    // Получаем текущий offset из URL
    const currentPath = window.location.pathname;
    const offsetMatch = currentPath.match(/tasks\/(-?\d+)\//);
    let offset = offsetMatch ? parseInt(offsetMatch[1], 10) : 0;

    // Событие для кнопки "Предыдущая неделя"
    prevWeekButton.addEventListener('click', () => {
        window.location.href = `/tasks/${offset - 1}/`; // Сдвиг назад
    });

    // Событие для кнопки "Следующая неделя"
    nextWeekButton.addEventListener('click', () => {
        window.location.href = `/tasks/${offset + 1}/`; // Сдвиг вперед
    });

    // Удаление пары
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            const taskId = e.target.dataset.id;
            const confirmed = confirm('Вы уверены, что хотите удалить эту задачу?');

            if (confirmed) {
                try {
                    const response = await fetch(`/tasks/delete/${taskId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        }
                    });

                    if (response.ok) {
                        window.location.reload(); // Перезагружаем страницу после удаления
                    } else {
                        alert('Ошибка при удалении задания.');
                    }
                } catch (error) {
                    console.error('Ошибка сети:', error);
                    alert('Произошла ошибка при удалении.');
                }
            }
        });

    });
    

    // Открытие модального окна
    const addtaskButton = document.getElementById('add-task-btn');
    const modal = document.getElementById('add-task-modal');
    const closeModalButton = document.getElementById('close-modal');
    
    // Проверим, существует ли кнопка
    if (addtaskButton) {
        addtaskButton.addEventListener('click', () => {
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
    const addtaskForm = document.getElementById('add-task-form');
    addtaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();  // Не даем странице перезагрузиться
    
        const formData = new FormData(addtaskForm);
    
        try {
            const response = await fetch('/tasks/add/', {
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

});
