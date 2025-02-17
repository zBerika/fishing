import cv2
import numpy as np
import mss
import time
import threading
import keyboard

# Изначальные координаты для двух зон захвата
top_1 = 655
left_1 = 950
width_1 = 160
height_1 = 80

top_2 = 478
left_2 = 897


monitor1 = {"top": top_1, "left": left_1, "width": width_1, "height": height_1}
monitor2 = {"top": top_2, "left": left_2, "width": 250, "height": 160}  # Смещение top -150, left +100
print(f"Область для захвата 1: {monitor1}")
print(f"Область для захвата 2: {monitor2}")

# Установка начальных значений для нижней и верхней границы бинаризации
lower_threshold_1 = 84
lower_threshold_2 = 44

upper_threshold_1 = 195
upper_threshold_2 = 255

# Минимальная и максимальная площадь контура для фильтрации
min_contour_area_1 = 4500
min_contour_area_2 = 4400
max_contour_area_1 = 12000
max_contour_area_2 = 30000

# Переменные для хранения координат центра объектов
object_center_x1 = None
object_center_x2 = None

# Флаг для управления потоком
running = True

# Флаги для режима перемещения и поиска объектов
moving_zone = True
search_mode = False

# Функция для перемещения областей захвата
def change_capture_area(direction, monitor):
    move_step = 5  # Шаг перемещения
    if direction == 'left':
        monitor["left"] -= move_step
    elif direction == 'right':
        monitor["left"] += move_step
    elif direction == 'up':
        monitor["top"] -= move_step
    elif direction == 'down':
        monitor["top"] += move_step

# Поток для управления движением
def control_thread():
    global object_center_x1, object_center_x2
    while running:
        if search_mode:  # Управление поиском объекта
            if object_center_x1 is not None or object_center_x2 is not None:
                keyboard.press('space')  # Нажимаем пробел
                time.sleep(0.1)
                keyboard.release('space')
                time.sleep(0.5)
                object_center_x1 = None
                object_center_x2 = None
        time.sleep(0.02)

# Запускаем поток
thread = threading.Thread(target=control_thread)
thread.start()

def print_monitor_values():
    print(f"Область для захвата 1: {monitor1}")
    print(f"Область для захвата 2: {monitor2}")

# Обновление параметров через ползунки для первой зоны
def update_width_1(val):
    monitor1["width"] = val
    print_monitor_values()

def update_height_1(val):
    monitor1["height"] = val
    print_monitor_values()

def update_lower_threshold_1(val):
    global lower_threshold_1
    lower_threshold_1 = val

def update_upper_threshold_1(val):
    global upper_threshold_1
    upper_threshold_1 = val

def update_min_contour_area_1(val):
    global min_contour_area_1
    min_contour_area_1 = val

def update_max_contour_area_1(val):
    global max_contour_area_1
    max_contour_area_1 = val

# Обновление параметров через ползунки для второй зоны
def update_width_2(val):
    monitor2["width"] = val
    print_monitor_values()

def update_height_2(val):
    monitor2["height"] = val
    print_monitor_values()

def update_lower_threshold_2(val):
    global lower_threshold_2
    lower_threshold_2 = val

def update_upper_threshold_2(val):
    global upper_threshold_2
    upper_threshold_2 = val

def update_min_contour_area_2(val):
    global min_contour_area_2
    min_contour_area_2 = val

def update_max_contour_area_2(val):
    global max_contour_area_2
    max_contour_area_2 = val

# Создаем окна с ползунками для настройки параметров
cv2.namedWindow("Settings Zone 1")
cv2.createTrackbar("Width", "Settings Zone 1", monitor1["width"], 1920, update_width_1)
cv2.createTrackbar("Height", "Settings Zone 1", monitor1["height"], 1080, update_height_1)
cv2.createTrackbar("Lower Threshold", "Settings Zone 1", lower_threshold_1, 255, update_lower_threshold_1)
cv2.createTrackbar("Upper Threshold", "Settings Zone 1", upper_threshold_1, 255, update_upper_threshold_1)
cv2.createTrackbar("Min Contour Area", "Settings Zone 1", min_contour_area_1, 10000, update_min_contour_area_1)
cv2.createTrackbar("Max Contour Area", "Settings Zone 1", max_contour_area_1, 20000, update_max_contour_area_1)

cv2.namedWindow("Settings Zone 2")
cv2.createTrackbar("Width", "Settings Zone 2", monitor2["width"], 1920, update_width_2)
cv2.createTrackbar("Height", "Settings Zone 2", monitor2["height"], 1080, update_height_2)
cv2.createTrackbar("Lower Threshold", "Settings Zone 2", lower_threshold_2, 255, update_lower_threshold_2)
cv2.createTrackbar("Upper Threshold", "Settings Zone 2", upper_threshold_2, 255, update_upper_threshold_2)
cv2.createTrackbar("Min Contour Area", "Settings Zone 2", min_contour_area_2, 30000, update_min_contour_area_2)
cv2.createTrackbar("Max Contour Area", "Settings Zone 2", max_contour_area_2, 30000, update_max_contour_area_2)


with mss.mss() as sct:
    last_key = False
    while True:
        # Перемещение зон захвата
        if moving_zone and not search_mode:
            if keyboard.is_pressed('left'):
                change_capture_area('left', monitor1)
                change_capture_area('left', monitor2)
            elif keyboard.is_pressed('right'):
                change_capture_area('right', monitor1)
                change_capture_area('right', monitor2)
            elif keyboard.is_pressed('up'):
                change_capture_area('up', monitor1)
                change_capture_area('up', monitor2)
            elif keyboard.is_pressed('down'):
                change_capture_area('down', monitor1)
                change_capture_area('down', monitor2)

        # Захват и обработка первой зоны
        screenshot1 = sct.grab(monitor1)
        frame1 = np.array(screenshot1)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGRA2BGR)
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blurred1 = cv2.GaussianBlur(gray1, (5, 5), 0)
        _, binary1 = cv2.threshold(blurred1, lower_threshold_1, upper_threshold_1, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned_binary1 = cv2.morphologyEx(binary1, cv2.MORPH_OPEN, kernel)
        contours1, _ = cv2.findContours(cleaned_binary1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours1 = [cnt for cnt in contours1 if min_contour_area_1 < cv2.contourArea(cnt) < max_contour_area_1]
        if filtered_contours1:
            largest_contour1 = max(filtered_contours1, key=cv2.contourArea)
            x1, y1, w1, h1 = cv2.boundingRect(largest_contour1)
            object_center_x1 = x1 + w1 // 2
            cv2.drawContours(frame1, [largest_contour1], -1, (255, 0, 0), 2)
            cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
            cv2.circle(frame1, (object_center_x1, y1 + h1 // 2), 5, (0, 0, 255), -1)
        else:
            object_center_x1 = None

        # Захват и обработка второй зоны
        screenshot2 = sct.grab(monitor2)
        frame2 = np.array(screenshot2)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGRA2BGR)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)
        _, binary2 = cv2.threshold(blurred2, lower_threshold_2, upper_threshold_2, cv2.THRESH_BINARY)
        cleaned_binary2 = cv2.morphologyEx(binary2, cv2.MORPH_OPEN, kernel)
        contours2, _ = cv2.findContours(cleaned_binary2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours2 = [cnt for cnt in contours2 if min_contour_area_2 < cv2.contourArea(cnt) < max_contour_area_2]
        if filtered_contours2:
            largest_contour2 = max(filtered_contours2, key=cv2.contourArea)
            x2, y2, w2, h2 = cv2.boundingRect(largest_contour2)
            object_center_x2 = x2 + w2 // 2
            cv2.drawContours(frame2, [largest_contour2], -1, (255, 0, 0), 2)
            cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
            cv2.circle(frame2, (object_center_x2, y2 + h2 // 2), 5, (0, 0, 255), -1)
        else:
            object_center_x2 = None

        # Объединение и отображение результатов
        cv2.imshow("Frame 1", frame1)
        cv2.imshow("Frame 2", frame2)
        cv2.imshow("Binary 1", binary1)  # Отображение бинарного изображения 1
        cv2.imshow("Binary 2", binary2)  # Отображение бинарного изображения 2

        # Проверка переключения режима поиска
        if keyboard.is_pressed('+') and not last_key:
            search_mode = not search_mode
            moving_zone = not moving_zone
            last_key = True

        if not keyboard.is_pressed('+'):
            last_key = False

        # Выход из программы
        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

# Завершение потока
thread.join()
cv2.destroyAllWindows()
