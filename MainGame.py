import os
import sys
import pygame
import math

pygame.init()  # Инициализация pygame
screen = pygame.display.set_mode((800, 693))  # Создали screen - дисплей игры
size = width, height = screen.get_size()


def triangle_position(pos_x, pos_y):  # Получение координат основного треугольника (в зависимости от размеров дисплея)
    return [(50, pos_y - 50),
            (pos_x * 0.5, pos_y - (pos_x - 100) * math.sqrt(3) // 2),
            (pos_x - 50, pos_y - 50)]


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
    image = load_image("minion.jpg")
    image1 = pygame.transform.scale(image, (2 * hole_radius, 2 * hole_radius))  # Изменили размер изображения

    def __init__(self, *group):  # Создаём спрайт
        super().__init__(*group)
        self.image = Hole.image1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = holes_positions(triangle_position(width, height))[len(holes) - 1]

    def update(self):  # Меняем координаты спрайта
        self.rect.x, self.rect.y = pygame.mouse.get_pos()[0] - dx, pygame.mouse.get_pos()[1] - dy


holes = pygame.sprite.Group()  # Создал группу спрайтов
for _ in range(len(holes_positions(triangle_position(width, height)))):  # Добавляю в группу спрайты:
    Hole(holes)


def move(sprite_group, main_sprite_index):  # Функция, переделывающая группу спрайтов так, чтобы спрайт, которого мы
    # коснулись, был поверх других, т.е. отрисовывался последним - был 15-й фишкой
    new_sprite_group = pygame.sprite.Group()
    for sprite_index in range(main_sprite_index):  # Порядок спрайтов до "активного" спрайта остаётся неизменным
        new_sprite_group.add(sprite_group.sprites()[sprite_index])
    for sprite_index in range(main_sprite_index, len(sprite_group) - 1):  # Начиная с "бывшего" места спрайта и до
        # предпоследнего места, смещаем все спрайты влево (в списке)
        new_sprite_group.add(sprite_group.sprites()[sprite_index + 1])
    new_sprite_group.add(sprite_group.sprites()[main_sprite_index])  # Последняя, 15-я фишка - "активный" спрайт
    return new_sprite_group


active_sprite_index = None
running = True
while running:  # Игра:
    size = width, height = screen.get_size()
    for event in pygame.event.get():  # Отслеживаем события:
        if event.type == pygame.QUIT:
            running = False  # Остановим работу программы, если был нажат "крестик"
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos  # Получаем координаты курсора, если клавиша мыши была нажата.
            for sprite in holes.sprites():
                if x in range(sprite.rect[0], sprite.rect[0] + sprite.rect[2] + 1) \
                   and y in range(sprite.rect[1], sprite.rect[1] + sprite.rect[3] + 1):  # Проверяем, находится ли
                    # курсор в области определения какого-либо спрайта
                    active_sprite_index = holes.sprites().index(sprite)  # Определяем индекс такого "активного" спрайта
                    # в списке спрайтов группы
                    holes = move(holes, active_sprite_index)  # Переделаем группу спрайтов так, чтобы спрайт, которого
                    # мы коснулись, был поверх других, т.е. отрисовывался последним -  был 15-й фишкой
                    dx, dy = event.pos[0] - sprite.rect[0], event.pos[1] - sprite.rect[1]  # Расположение курсора в
                    # спрайте
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            active_sprite_index = None  # Если отпустить клавишу - "активный" спрайт перестаёт быть "активным"
        if event.type == pygame.MOUSEMOTION:
            if active_sprite_index is not None:
                holes.sprites()[-1].update()  # Если курсор движется, и "активный" спрайт есть - спрайт смещается
    screen.fill((204, 229, 255))  # Установил нежно-голубой цвет фона дисплея
    pygame.draw.polygon(screen, 'blue', triangle_position(width, height))  # Нарисовал основной треугольник на дисплей
    holes.draw(screen)  # Нарисовал эту группу спрайтов-отверстий
    pygame.display.flip()  # Обновление дисплея
pygame.quit()
