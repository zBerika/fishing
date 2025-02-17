import cv2
import numpy as np
import mss
import time
from screeninfo import get_monitors

# Загрузка шаблона с альфа-каналом
template = cv2.imread("ramka.png", cv2.IMREAD_UNCHANGED)

# Разделяем каналы (BGR и альфа-канал)
if template.shape[2] == 4:
    template_bgr = template[:, :, :3]  # BGR-каналы
    template_alpha = template[:, :, 3]  # Альфа-канал
else:
    template_bgr = template
    template_alpha = np.ones_like(template[:, :, 0]) * 255  # Если альфа-канала нет, используем белый (непрозрачный)

# Преобразуем BGR в оттенки серого
template_gray = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)

# Бинаризация шаблона с учетом альфа-канала
_, template_binary = cv2.threshold(template_gray, 30, 255, cv2.THRESH_BINARY)

# Используем альфа-канал для определения прозрачных/непрозрачных областей
alpha_mask = cv2.threshold(template_alpha, 128, 255, cv2.THRESH_BINARY)[1]

# Применяем маску альфа-канала к бинарному изображению
template_binary = cv2.bitwise_and(template_binary, alpha_mask)

# Находим контуры шаблона
template_contours, _ = cv2.findContours(template_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Минимальная и максимальная площадь объекта (по умолчанию)
min_area = 3000
max_area = 15000

# Функция для обновления значений минимальной и максимальной площади
def update_area(val, area_type):
    global min_area, max_area
    if area_type == 'min':
        min_area = val
    elif area_type == 'max':
        max_area = val


# Функция для обновления бинаризации на основе значения ползунка
def update_binary(val):
    # Бинаризация шаблона с учетом альфа-канала
    _, template_binary = cv2.threshold(template_gray, val, 255, cv2.THRESH_BINARY)

    # Используем альфа-канал для определения прозрачных/непрозрачных областей
    alpha_mask = cv2.threshold(template_alpha, 128, 255, cv2.THRESH_BINARY)[1]

    # Применяем маску альфа-канала к бинарному изображению
    template_binary = cv2.bitwise_and(template_binary, alpha_mask)

    # Находим контуры
    template_contours, _ = cv2.findContours(template_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создаем пустое изображение для отображения контуров
    contour_image = np.zeros_like(template)

    # Отображаем контуры на черном фоне
    cv2.drawContours(contour_image, template_contours, -1, (255, 255, 255), 1)

    # Отображаем изображение с контурами
    cv2.imshow('Contours', contour_image)


# Создаем окно для отображения контуров
cv2.namedWindow('Contours')

# Создаем ползунок для настройки порога бинаризации
cv2.createTrackbar('Threshold', 'Contours', 30, 255, update_binary)

# Создаем ползунки для минимальной и максимальной площади
cv2.createTrackbar('Min Area', 'Contours', min_area, 3000, lambda x: update_area(x, 'min'))
cv2.createTrackbar('Max Area', 'Contours', max_area, 20000, lambda x: update_area(x, 'max'))


# Инициализируем бинаризацию с начальным значением порога
update_binary(30)

# Определение разрешения монитора
monitor_info = get_monitors()[0]  # Получаем информацию о первом мониторе
screen_width = monitor_info.width
screen_height = monitor_info.height

# Рассчитываем координаты области, занимающей 30% от разрешения экрана и размещенной в центре
width = int(screen_width * 0.5)
height = int(screen_height * 0.5)

left = (screen_width - width) // 2
top = (screen_height - height) // 2

monitor = {"top": top, "left": left, "width": width, "height": height}

# Функция для поиска и выделения объекта в указанной области
def find_object_in_zone(screenshot, template_binary):
    # Преобразуем скриншот в оттенки серого
    frame_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)

    # Бинаризуем изображение
    _, frame_binary = cv2.threshold(frame_gray, 30, 255, cv2.THRESH_BINARY)

    # Находим контуры в скриншоте
    frame_contours, _ = cv2.findContours(frame_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_match = None
    best_val = float('inf')

    # Проходим по всем контурным объектам в шаблоне и скриншоте
    for cnt in frame_contours:
        area = cv2.contourArea(cnt)

        # Проверяем, подходит ли площадь под заданные ограничения
        if area < min_area or area > max_area:
            continue  # Пропускаем контуры, которые не соответствуют площади

        for template_cnt in template_contours:
            match_val = cv2.matchShapes(template_cnt, cnt, cv2.CONTOURS_MATCH_I1, 0)
            if match_val < best_val:
                best_val = match_val
                best_match = cnt

    # Если найден лучший совпадающий контур
    if best_match is not None:
        return best_match  # Возвращаем сам контур
    else:
        return None


# Открытие экрана и захват изображения в реальном времени
with mss.mss() as sct:
    while True:
        try:
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)

            # Преобразуем изображение в черно-белое
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
            _, frame_binary = cv2.threshold(frame_gray, 127, 255, cv2.THRESH_BINARY)

            # Поиск объекта в зоне
            matched_contour = find_object_in_zone(frame, template_binary)

            # Если объект найден, рисуем его контур и выводим координаты и площадь
            if matched_contour is not None:
                # Рисуем сам контур
                cv2.drawContours(frame, [matched_contour], -1, (0, 255, 0), 2)  # Зеленый контур

                # Получаем координаты для отображения
                x, y, w, h = cv2.boundingRect(matched_contour)

                # Корректируем координаты, добавляя смещение области захвата
                global_x = x + left
                global_y = y + top

                # Выводим глобальные координаты
                cv2.putText(frame, f"Coords: ({global_x}, {global_y})", (global_x, global_y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 1)

                # Получаем площадь объекта
                area = cv2.contourArea(matched_contour)

                # Выводим площадь
                cv2.putText(frame, f"Area: {int(area)}", (global_x, global_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 1)

            # Отображаем изображение с выделением объекта
            cv2.imshow("Captured Zone", frame)

            # Пауза для уменьшения нагрузки
            time.sleep(0.05)

            # Обновляем контуры при каждом кадре
            update_binary(30)

            # Выход из программы при нажатии клавиши 'q'
            if cv2.waitKey(1) & 0xFF == 27:
                break
        except KeyboardInterrupt:
            break

cv2.destroyAllWindows()
