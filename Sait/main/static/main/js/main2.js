
  // ----------------------------days of week------------
  // Функция для обновления дней недели
  function updateWeekDates(weekStartDate) {
    const daysOfWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
    const dayElements = document.querySelectorAll('.day_of_week');
    const dayElementsDay = document.querySelectorAll('.day_data');
  
    // Заполняем дни недели
    for (let i = 0; i < 7; i++) {
        const currentDay = new Date(weekStartDate);
        currentDay.setDate(weekStartDate.getDate() + i);
        dayElements[i].innerText = `${daysOfWeek[i]}`;
        dayElementsDay[i].innerText = currentDay.toLocaleDateString('ru-RU');
    }
  }
  
  // Функция для получения даты начала недели (понедельник)
  function getStartOfWeek(date) {
    const startOfWeek = new Date(date);
    const day = startOfWeek.getDay();
    const diff = startOfWeek.getDate() - day + (day == 0 ? -6 : 1); // если воскресенье, то отнимаем 6
    startOfWeek.setDate(diff);
    return startOfWeek;
  }
  
  // Начальная дата - текущая неделя
  let currentWeekStartDate = getStartOfWeek(new Date());
  
  // Инициализируем отображение текущей недели
  updateWeekDates(currentWeekStartDate);
  
  // Обработчик для кнопки "Предыдущая неделя"
  document.getElementById('prevWeekBtn').addEventListener('click', () => {
    currentWeekStartDate.setDate(currentWeekStartDate.getDate() - 7); // Переходим на предыдущую неделю
    updateWeekDates(currentWeekStartDate);
  });
  
  // Обработчик для кнопки "Следующая неделя"
  document.getElementById('nextWeekBtn').addEventListener('click', () => {
    currentWeekStartDate.setDate(currentWeekStartDate.getDate() + 7); // Переходим на следующую неделю
    updateWeekDates(currentWeekStartDate);
  });

  // ---------------------------модальное окноооооо-----------
const modalController = ({modal, btnOpen, btnClose, time = 300}) => {
    const buttonElems = document.querySelectorAll(btnOpen);
    const modalElem = document.querySelector(modal);
  
    modalElem.style.cssText = `
      display: flex;
      visibility: hidden;
      opacity: 0;
      transition: opacity ${time}ms ease-in-out;
    `;
  
    const closeModal = event => {
      const target = event.target;
  
      if (
        target === modalElem ||
        (btnClose && target.closest(btnClose)) ||
        event.code === 'Escape'
        ) {
        
        modalElem.style.opacity = 0;
  
        setTimeout(() => {
          modalElem.style.visibility = 'hidden';
        }, time);
  
        window.removeEventListener('keydown', closeModal);
      }
    }
  
    const openModal = () => {
      modalElem.style.visibility = 'visible';
      modalElem.style.opacity = 1;
      window.addEventListener('keydown', closeModal)
    };
  
    buttonElems.forEach(btn => {
      btn.addEventListener('click', openModal);
    });
  
    modalElem.addEventListener('click', closeModal);
  };
  
  modalController({
    modal: '.modal1',
    btnOpen: '.section__button1',
    btnClose: '.modal__close',
  });
  
  modalController({
    modal: '.modal2',
    btnOpen: '.section__button2',
    btnClose: '.modal__close'
  });
  
  