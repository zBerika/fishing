import cv2
import numpy as np
import mss
import time
import threading
import keyboard

# Изначальные координаты для захвата
monitor1 = {"top": 460, "left": 700, "width": 645, "height": 170}
monitor2 = {"top": 520, "left": 665, "width": 645, "height": 170}
print(f"Область для захвата: {monitor1}")

# Установка нижнего и верхнего порога бинаризации для обоих объектов
lower_threshold1 = 84
upper_threshold1 = 150
lower_threshold2 = 45
upper_threshold2 = 105

# Минимальная и максимальная площадь контура для фильтрации
min_contour_area1 = 0
max_contour_area1 = 1100
min_contour_area2 = 1400
max_contour_area2 = 7000

# Переменные для хранения координат центра объектов
object_center_x1 = None
object_center_x2 = None
difference = 0

# Флаг для управления потоком
running = True

# Флаг для включения/выключения режима перемещения зоны захвата
moving_zone = True
search_mode = False  # Флаг для управления поиском объектов и движением

# Функция для перемещения области захвата
def change_capture_area(direction):
    global monitor1, monitor2
    move_step = 5  # Шаг перемещения
    if direction == 'left':
        monitor1["left"] -= move_step
        monitor2["left"] -= move_step
    elif direction == 'right':
        monitor1["left"] += move_step
        monitor2["left"] += move_step
    elif direction == 'up':
        monitor1["top"] -= move_step
        monitor2["top"] -= move_step
    elif direction == 'down':
        monitor1["top"] += move_step
        monitor2["top"] += move_step

last_center_x1 = None
# Функция для управления движением666666442+
def control_thread():
    global  object_center_x1, object_center_x2, last_center_x1
    while running:
        if search_mode:  # Управление движением только если включен режим поиска
            if object_center_x1 is not None and object_center_x2 is not None:
                # Отслеживание направления движения первого объекта
                if last_center_x1 is not None:
                    # Если первый объект двигается вправо6+2++46++4+
                    if object_center_x1 > last_center_x1:
                        if object_center_x1 - 20 < object_center_x2 < object_center_x1:
                            # Если второй объект левее первого на 2066666666+28+6+ пикселей, перемещаем его влево
                            keyboard.release('right')  # Отпускаем вправо
                            keyboard.press('left')  # Зажимаем влево
                        elif object_center_x2 < object_center_x1 -20 :
                            # Если второй объект правее первого, двигаем его вправо
                            keyboard.release('left')  # Отпускаем влево
                            keyboard.press('right')  # Зажимаем вправо
                        elif object_center_x2 > object_center_x1  :
                            keyboard.release('right')  # Отпускаем влево
                            keyboard.press('left')  # Зажимаем вправо
                        else:
                            # Если центры выровнялись
                            keyboard.release('left')
                            keyboard.release('right')

                    # Если первый объект двигается влево
                    elif object_center_x1 < last_center_x1:
                        if object_center_x2 <= object_center_x1:
                            # Если второй объект левее или на том же уровне с первым
                            keyboard.release('left')  # Отпускаем влево
                            keyboard.press('right')  # Зажимаем вправо,
                        elif object_center_x2 > object_center_x1 + 20:
                            # Если второй объект правее первого на более чем 20+ пикселей
                            keyboard.release('right')  # Отпускаем вправо
                            keyboard.press('left')  # Зажимаем влево
                        elif object_center_x1 > object_center_x2 > object_center_x1 + 20:
                            # Если второй объект правее первого на более чем 20 пикселей
                            keyboard.release('left')  # Отпускаем влево
                            keyboard.press('right')  # Зажимаем вправо
                        else:
                            # Если центры выровнялись с учетом сдвига
                            keyboard.release('left')
                            keyboard.release('right')

                # Если первый объект остановился
                if object_center_x1 == last_center_x1:
                    if object_center_x1 is not None and object_center_x2 is not None:
                        if object_center_x1 > object_center_x2:
                        # Если центр первого объекта правее второго, зажимаем вправо, пока центры не выровняются
                            keyboard.release('left')
                            keyboard.press('right')
                        elif object_center_x1 < object_center_x2:
                        # Если центр первого объекта левее второго, зажимаем влево, пока центры не выровняются
                            keyboard.release('right')
                            keyboard.press('left')
                    else:
                        time.sleep(0)
                        print(f"{object_center_x1}, {object_center_x2}")

                # Обновляем предыдущие координаты первого объекта
                last_center_x1 = object_center_x1

            else:
                # Если один из объектов не найден, отпускаем все клавиши
                keyboard.release('right')
                keyboard.release('left')

        time.sleep(0.04)  # Задержка для сниж+ения 4444666666666666666644+нагрузки на процессор


# Запускаем поток
thread = threading.Thread(target=control_thread)
thread.start()

# Функции для изменения параметров через ползунки
def update_lower_threshold1(val):
    global lower_threshold1
    lower_threshold1 = val

def update_upper_threshold1(val):
    global upper_threshold1
    upper_threshold1 = val

def update_lower_threshold2(val):
    global lower_threshold2
    lower_threshold2 = val

def update_upper_threshold2(val):
    global upper_threshold2
    upper_threshold2 = val

def update_min_contour_area1(val):
    global min_contour_area1
    min_contour_area1 = val

def update_max_contour_area1(val):
    global max_contour_area1
    max_contour_area1 = val

def update_min_contour_area2(val):
    global min_contour_area2
    min_contour_area2 = val

def update_max_contour_area2(val):
    global max_contour_area2
    max_contour_area2 = val

# Создаем окно с ползунками
cv2.namedWindow("Capture Settings")
cv2.createTrackbar("Lower Threshold 1", "Capture Settings", lower_threshold1, 255, update_lower_threshold1)
cv2.createTrackbar("Upper Threshold 1", "Capture Settings", upper_threshold1, 255, update_upper_threshold1)
cv2.createTrackbar("Lower Threshold 2", "Capture Settings", lower_threshold2, 255, update_lower_threshold2)
cv2.createTrackbar("Upper Threshold 2", "Capture Settings", upper_threshold2, 255, update_upper_threshold2)
cv2.createTrackbar("Min Contour Area 1", "Capture Settings", min_contour_area1, 10000, update_min_contour_area1)
cv2.createTrackbar("Max Contour Area 1", "Capture Settings", max_contour_area1, 10000, update_max_contour_area1)
cv2.createTrackbar("Min Contour Area 2", "Capture Settings", min_contour_area2, 10000, update_min_contour_area2)
cv2.createTrackbar("Max Contour Area 2", "Capture Settings", max_contour_area2, 10000, update_max_contour_area2)


with mss.mss() as sct:
    last_key = False  # Флаг, чтобы отслеживать нажатие клавиши
    while True:
        # Перемещение зоны захвата, если не активирован режим поиска
        if moving_zone and not search_mode:
            if keyboard.is_pressed('left'):
                print_monitor_values()
                change_capture_area('left')
            elif keyboard.is_pressed('right'):
                change_capture_area('right')
            elif keyboard.is_pressed('up'):
                change_capture_area('up')
            elif keyboard.is_pressed('down'):
                change_capture_area('down')

        def print_monitor_values():
            print(f"Область для захвата 1: {monitor1}")

        # Захват области экрана для первого объекта
        screenshot1 = sct.grab(monitor1)
        frame1 = np.array(screenshot1)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGRA2BGR)

        # Удаляем синий цвет (обнуляем синий канал)
        #frame1[:, :, 0] = 0  # Канал B (синий)

        # Захват области экрана для второго объекта
        screenshot2 = sct.grab(monitor2)
        frame2 = np.array(screenshot2)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGRA2BGR)

        # Удаляем синий цвет (обнуляем синий канал)
        frame2[:, :, 0] = 0  # Канал B (синий)


        # Преобразование в оттенки серого и размытие для первого объекта
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blurred1 = cv2.GaussianBlur(gray1, (5, 5), 0)

        # Бинаризация для первого объекта
        _, binary1 = cv2.threshold(blurred1, lower_threshold1, upper_threshold1, cv2.THRESH_BINARY)

        # Морфологические операции для очистки маски для первого объекта
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        cleaned_binary1 = cv2.morphologyEx(binary1, cv2.MORPH_OPEN, kernel1)

        # Находим контуры для первого объекта
        contours1, _ = cv2.findContours(cleaned_binary1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours1 = [cnt for cnt in contours1 if min_contour_area1 < cv2.contourArea(cnt) < max_contour_area1]

        if filtered_contours1:
            largest_contour1 = max(filtered_contours1, key=cv2.contourArea)
            x1, y1, w1, h1 = cv2.boundingRect(largest_contour1)
            object_center_x1 = x1 + w1 // 2
            cv2.drawContours(frame1, [largest_contour1], -1, (255, 0, 0), 2)  # Обводим контур первого объекта
            cv2.rectangle(frame1, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
            cv2.circle(frame1, (object_center_x1, y1 + h1 // 2), 5, (0, 0, 255), -1)
        else:
            object_center_x1 = None  # Если объект пропал, устанавливаем в None

        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)

        # Бинаризация для первого объекта
        _, binary2 = cv2.threshold(blurred2, lower_threshold2, upper_threshold2, cv2.THRESH_BINARY)

        # Морфологические операции для очистки маски для первого объекта
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        cleaned_binary2 = cv2.morphologyEx(binary2, cv2.MORPH_OPEN, kernel2)


        # Находим контуры для второго объекта
        contours2, _ = cv2.findContours(cleaned_binary2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours2 = [cnt for cnt in contours2 if min_contour_area2 < cv2.contourArea(cnt) < max_contour_area2]

        if filtered_contours2:
            largest_contour2 = max(filtered_contours2, key=cv2.contourArea)
            x2, y2, w2, h2 = cv2.boundingRect(largest_contour2)
            object_center_x2 = x2 + w2 // 2
            #cv2.drawContours(frame2, [largest_contour2], -1, (0, 255, 0), 2)  # Обводим контур второго объекта
            cv2.rectangle(frame2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
            cv2.circle(frame2, (object_center_x2, y2 + h2 // 2), 5, (0, 0, 255), -1)

            # Вычисляем разницу между координатами объектов

        else:
            object_center_x2 = None  # Если объе+кт пропал, устанавливаем в None



        # Объединение дву+х+ кадров
        combined_frame = np.hstack((frame1, frame2))

        # Отображение+ объединенного изображения
        cv2.imshow("Combined Frame", combined_frame)
        cv2.imshow("Binary Frame 1", cleaned_binary1)  # Отображение бинарного изображения первого объекта
        cv2.imshow("Binary Frame 2", cleaned_binary2)  # Отображение бинарного изображения второго объекта

        # Проверка нажатия '+' для переключения между режимами
        if keyboard.is_pressed('+') and not last_key:  # Проверка нажатия и что клавиша не была нажата раньше
            search_mode = not search_mode
            moving_zone = not moving_zone
            last_key = True  # Устанавливаем флаг на True, чтобы не зацикливать переключение

        if not keyboard.is_pressed('+'):
            last_key = False  # Сбрасываем флаг, когда клавиша+ отпущена

        # Выход по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

# Заверш+ение потока
thread.join()
cv2.destroyAllWindows()