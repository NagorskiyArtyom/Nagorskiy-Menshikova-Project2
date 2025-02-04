import pygame
import math
import os
import sys
import pygame_widgets
from pygame import sprite
from pygame_widgets.button import Button

# Инициализация Pygame
pygame.init()

# Размеры окна
width, height = 800, 693
screen = pygame.display.set_mode((width, height))

# Кнопки выхода и старта
exitt = Button(screen, 520, 25, 200, 70, text='Выход', fontSize=30, margin=20, inactiveColour=(120, 160, 160),
               hoverColour=(150, 0, 0), pressedColour=(20, 130, 120), radius=10)

start = Button(screen, 520, 125, 200, 70, text='Начать игру', fontSize=30, margin=20, inactiveColour=(120, 160, 160),
               hoverColour=(150, 0, 0), pressedColour=(20, 130, 120), radius=10)


# Функция для получения координат вершин треугольника
def triangle_position(pos_x, pos_y):
    return [
        (50, pos_y - 50),
        (pos_x * 0.5, pos_y - (pos_x - 100) * math.sqrt(3) // 2),
        (pos_x - 50, pos_y - 50)
    ]


# Радиус кругов
hole_radius = (triangle_position(width, height)[-1][0] - triangle_position(width, height)[0][0]) // 20


# Функция для получения позиций кругов
def holes_positions(triangle_coords):
    triangle_side = triangle_coords[-1][0] - triangle_coords[0][0]
    triangle_height = triangle_coords[0][1] - triangle_coords[1][1]
    part_x = triangle_side * 9 // 14 // 8
    part_y = (triangle_height * 114 // 139 + hole_radius) // 5

    holes_coords = []
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


# Цвета кругов
colors = [(170, 200, 230)] * len(holes_positions(triangle_position(width, height)))

# Главный цикл программы
start_visible = True
running = True
while running:
    screen.fill((204, 229, 255))  # Фоновый цвет

    pygame.draw.polygon(screen, 'blue', triangle_position(width, height))  # Основной треугольник

    func = holes_positions(triangle_position(width, height))

    # Рисуем круги
    for i, (x, y) in enumerate(func):
        pygame.draw.circle(screen, colors[i], (x + 35, y + 35), 30)
    # Обработка событий
    for event in pygame.event.get():
        x1, y1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

            colors = [(170, 200, 230)] * len(holes_positions(triangle_position(width, height)))

            for i, (x, y) in enumerate(func):
                if math.hypot(x1 - (x + 35), y1 - (y + 35)) <= 30:
                    # Меняем цвет круга при клике
                    colors[i] = (130, 130, 130) if colors[i] != (130, 130, 130) else (170, 200, 230)

            if 520 <= x1 <= 720 and 125 <= y1 <= 195:
                for sprite in holes.sprites():
                    if x in range(sprite.rect[0], sprite.rect[0] + sprite.rect[2] + 1) \
                            and y in range(sprite.rect[1],
                                           sprite.rect[1] + sprite.rect[3] + 1):  # Проверяем, находится ли
                        # курсор в области определения какого-либо спрайта
                        active_sprite_index = holes.sprites().index(
                            sprite)  # Определяем индекс такого "активного" спрайта
                        # в списке спрайтов группы
                        holes = move(holes,
                                     active_sprite_index)  # Переделаем группу спрайтов так, чтобы спрайт, которого
                        # мы коснулись, был поверх других, т.е. отрисовывался последним -  был 15-й фишкой
                        dx, dy = event.pos[0] - sprite.rect[0], event.pos[1] - sprite.rect[1]  # Расположение курсора в
                        # спрайте
                        break

        pygame_widgets.update(event)
        pygame.display.flip()  # Обновляем экран

pygame.quit()


