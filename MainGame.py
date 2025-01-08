import os
import sys
import pygame
import math

pygame.init()  # Инициализация pygame
screen = pygame.display.set_mode((800, 693))  # Создали screen - дисплей игры
size = width, height = screen.get_size()


def triangle_position(x, y):  # Получение координат основного треугольника (в зависимости от размеров дисплея)
    return [(50, y - 50),
            (x * 0.5, y - (x - 100) * math.sqrt(3) // 2),
            (x - 50, y - 50)]


hole_radius = (triangle_position(width, height)[-1][0]
               - triangle_position(width, height)[0][0]) // 20  # Создали hole_radius - радиус нашего спрайта-отверстия


def holes_positions(triangle_coords: list):  # Возвращает список координат спрайтов-отверстий
    triangle_side = triangle_coords[-1][0] - triangle_coords[0][0]
    triangle_height = triangle_coords[0][1] - triangle_coords[1][1]
    part_x = triangle_side * 9 // 14 // 8  # Часть по x - расстояние от проекции центра одного спрайта на нижнюю
    # сторону треугольника до другой проекции
    part_y = (triangle_height * 114 // 139 + hole_radius) // 5  # Часть по y - расстояние от проекции центра одного
    # спрайта на высоту треугольника до другой проекции
    holes_coords = []  # Список для хранения координат каждого спрайта
    for row in range(0, 5):
        for col in range(4 - row, 4 + row + 1, 2):
            x = triangle_coords[0][0] + triangle_side * 5 // 28 + col * part_x - hole_radius
            y = triangle_coords[1][1] + triangle_height * 25 // 139 + part_y * row - hole_radius
            holes_coords.append((x, y))
    return holes_coords


def load_image(name, colorkey=None):  # Возвращает Surface, на котором расположено изображение «в натуральную величину»
    fullname = os.path.join('data', name)  # Получаем полный путь к файлу, содержащему изображение нашего спрайта
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()  # Завершаем работу программы и сообщаем про ошибку
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:  # Функция сама возьмет прозрачным цветом левый верхний угол изображения (обычно это будет
            # цвет фона, который хочется сделать прозрачным).
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)  # Переданный цвет станет прозрачным
    else:
        image = image.convert_alpha()  # Загруженное изображение сохранит прозрачность
    return image


class Hole(pygame.sprite.Sprite):  # Объект - отверстие
    image = load_image("yandex-logo.png")
    image1 = pygame.transform.scale(image, (2 * hole_radius, 2 * hole_radius))  # Изменили размер изображения

    def __init__(self, *group):  # Создаём спрайт
        super().__init__(*group)
        self.image = Hole.image1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = holes_positions(triangle_position(width, height))[len(holes) - 1]


running = True
while running:  # Игра:
    screen.fill((204, 229, 255))  # Установил нежно-голубой цвет фона дисплея
    size = width, height = screen.get_size()
    pygame.draw.polygon(screen, 'blue', triangle_position(width, height))  # Нарисовал основной треугольник на дисплей
    holes = pygame.sprite.Group()  # Создал группу спрайтов
    for _ in range(len(holes_positions(triangle_position(width, height)))):  # Добавляю в группу спрайты:
        Hole(holes)
    holes.draw(screen)  # Нарисовал эту группу спрайтов-отверстий
    pygame.display.flip()  # Обновление дисплея
    while pygame.event.wait().type != pygame.QUIT:
        running = False  # Остановим работу программы, если был нажат "крестик"
pygame.quit()
