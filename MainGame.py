import math
import os
import sys
import pygame
import pygame_gui
import Main_Window
import button_exit
import MainMenu

holes = []
colors = [(200, 200, 200)] * 15

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


class Triangle:
    def __init__(self, window: pygame.surface.Surface):
        self.window = window
        self.width = window.get_width() - 50 * 2  # Значение стороны равностороннего треугольника c отступами по 50
        # пикслей от краёв окна
        self.height = int((self.width // 2) * math.sqrt(3))  # Значение высоты этого треугольника

    def get_coords(self):  # Функция, которая выдаёт координаты вершин треугольника, для его отрисовки
        return [(50, self.window.get_height() - 50),
                (self.window.get_width() * 0.5, self.window.get_height() - 50 - self.height),
                (self.window.get_width() - 50, self.window.get_height() - 50)]

    def render(self):  # Функция, отрисовывающая треугольник
        pygame.draw.polygon(self.window, (0, 0, 255), self.get_coords())


class Things:  # Класс, посвящённый всем фишкам, как группе
    def __init__(self, the_complexity, figure, image):
        self.active_thing_index, self.dx, self.dy = None, None, None
        self.hole_radius = int(0.05 * figure.width)  # Радиус фишки
        # НИЖЕ ДАННЫЕ ДЛЯ ФИГУРЫ - ТРЕУГОЛЬНИК
        self.part_x = (figure.width - 250) // 8  # Часть по x - расстояние от проекции центра одной фишки на нижнюю
        # сторону треугольника до другой
        self.part_y = (figure.height - 115 + self.hole_radius) // 5  # Часть по y - расстояние от проекции центра одного
        # спрайта на высоту треугольника до другой проекции
        # ВЫШЕ ДАННЫЕ ДЛЯ ФИГУРЫ - ТРЕУГОЛЬНИК
        self.things_group = pygame.sprite.Group()  # Группа спрайтов-фишек
        self.image = pygame.transform.scale(load_image(image), (2 * self.hole_radius, 2 * self.hole_radius))  # Сразу
        # загрузим изображение каждой фишки и подгоним его под её размер
        self.add_things(figure, the_complexity)  # Установим начальное расположение фишек в фигуре

    def add_things(self, figure, the_complexity, k=0):
        if the_complexity == 1:  # Если мы проходим превый уровень - фигура - треугольник
            for row in range(0, 5):  # Проходим по ряду
                for col in range(4 - row, 4 + row + 1, 2):  # Проходим по столбцу
                    thing = pygame.sprite.Sprite(self.things_group)  # Создаём фишку, которая автоматически запишется в
                    # группу спрайтов-фишек
                    thing.image = self.image  # Присваеваем ей изображение
                    thing.rect = thing.image.get_rect()  # Присваеваем ей размер
                    x = figure.get_coords()[0][0] + 126 + col * self.part_x - self.hole_radius
                    y = figure.get_coords()[1][1] + 115 + self.part_y * row - self.hole_radius
                    thing.rect.x, thing.rect.y = (x, y)  # Присваиваем ей координаты
                    holes.append((k, x, y))
                    k += 1

    def render(self, window):  # Функция, отрисовывающая каждую фишку группы
        self.things_group.draw(window)

    def get_click(self, mouse_pos):  # Функция, описывающая действие, при нажатии клавиши мыши
        for thing in self.things_group.sprites():
            if mouse_pos[0] in range(thing.rect[0], thing.rect[0] + thing.rect[2] + 1) \
                    and mouse_pos[1] in range(thing.rect[1],
                                              thing.rect[1] + thing.rect[3] + 1):  # Проверка: находится ли
                # курсор в области какой-либо фишки
                self.active_thing_index = self.things_group.sprites().index(thing)  # Такая фишка будет "активной"
                self.new_things_group(self.active_thing_index)  # Меняем группу так, чтобы эта "активная" фишка была
                # поверх других, т.е последняя в отрисовке
                self.dx, self.dy = mouse_pos[0] - thing.rect[0], mouse_pos[1] - thing.rect[1]  # Точное расположение
                # курсора мыши в фишке
                break

    def new_things_group(self, active_thing_index):  # Функция, переделывающая группу фишек так, чтобы фишка, которой
        # мы коснулись, была поверх других, т.е. отрисовывалась последней - была 15-й фишкой
        new_thing_group = pygame.sprite.Group()
        for thing_index in range(active_thing_index):  # Порядок фишек до "активной" фишки остаётся неизменным
            new_thing_group.add(self.things_group.sprites()[thing_index])
        for thing_index in range(active_thing_index, len(self.things_group) - 1):  # Начиная с "бывшего" места фишки
            # и до предпоследнего места, смещаем все фишки влево (в списке)
            new_thing_group.add(self.things_group.sprites()[thing_index + 1])
        new_thing_group.add(self.things_group.sprites()[active_thing_index])  # Последняя, 15-я фишка - "активный"
        # спрайт
        self.things_group = new_thing_group

    def mouse_position_with_thing(self, window, mouse_pos):  # Функция, проверяющая область допустимых значение
        # координат курсора, в зависимости от "активной" фишки
        x, y = mouse_pos
        if x - self.dx < 0:
            x = self.dx
        elif x - self.dx + 2 * self.hole_radius > window.get_width():
            x = window.get_width() - 2 * self.hole_radius + self.dx
        if y - self.dy < 0:
            y = self.dy
        elif y - self.dy + 2 * self.hole_radius > window.get_height():
            y = window.get_height() - 2 * self.hole_radius + self.dy
        return x, y

    def get_move(self, window, mouse_pos):  # Функция, описывающая действие, при перемещении курсора мыши
        if self.active_thing_index is not None:  # Если есть "активная" фишка, то поменяем её координаты
            mouse_pos = self.mouse_position_with_thing(window, mouse_pos)
            self.things_group.sprites()[-1].rect[:2] = mouse_pos[0] - self.dx, mouse_pos[1] - self.dy

    def get_end_click(self):  # Функция, описывающая действие, при отпуске клавиши мыши
        self.active_thing_index, self.dx, self.dy = None, None, None  # "Активная" фишка исчезает, а следовательно и
        # точное расположение куросра в ней - тоже

    def draw_circles(self, scr):
        for (i, x, y) in holes:
            pygame.draw.circle(scr, colors[i], (x + 35, y + 35), self.hole_radius)


def terminate():  # Функция, прерывающая всю работу
    pygame.quit()
    sys.exit()


def MainGame(window: pygame.surface.Surface, complexity, choosen_sprite=None):  # Игра:
    global colors
    shapes = {1: Triangle(window), 2: None, 3: None, 4: None}  # Словарь фигур, соответствующих уровням, пока что
    # доступен только треугольник
    shape = shapes[complexity]  # Фигура соответствует уровню
    things = Things(1, shape, "yandex-logo.png")  # Фишки
    manager = pygame_gui.UIManager(window.get_size(), "data/ui_theme.json")
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window.get_width() - 50 - 176,
                                                                          window.get_height() - 50 - shape.height),
                                                                         (176, 63)),
                                               text='Выйти',
                                               manager=manager)
    return_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window.get_width() - 50 - 176,
                                                                            window.get_height() - 50 + 63 + 15
                                                                            - shape.height), (176, 63)),
                                                 text='Заново',
                                                 manager=manager)
    clock = pygame.time.Clock()
    running_in_MainGame = True
    exit_prompt_open = False  # Флаг для окна подтверждения
    while running_in_MainGame:  # Игра:
        time_delta = clock.tick(60) / 1000.0
        x1, y1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        for event_in_MainGame in pygame.event.get():  # Отслеживаем события:
            if event_in_MainGame.type == pygame.QUIT:
                terminate()

            if event_in_MainGame.type == pygame.MOUSEBUTTONDOWN:
                things.get_click(pygame.mouse.get_pos())
            if event_in_MainGame.type == pygame.MOUSEMOTION:
                things.get_move(window, pygame.mouse.get_pos())
            if event_in_MainGame.type == pygame.MOUSEBUTTONUP:
                things.get_end_click()

            if event_in_MainGame.type == pygame_gui.UI_BUTTON_PRESSED:
                if event_in_MainGame.ui_element == return_button:
                    MainGame(window, complexity)
                elif event_in_MainGame.ui_element == exit_button:
                    exit_prompt_open = True  # Открываем окно подтверждения
                    button_exit.exit_prompt(window)  # Отображаем окно подтверждения
            manager.process_events(event_in_MainGame)

        if not exit_prompt_open:  # Если окно подтверждения не открыто, продолжаем игру
            window.fill((204, 229, 255))  # Установил нежно-голубой цвет фона дисплея
            shape.render()  # Отрисовка фигуры
            things.draw_circles(window)
            things.render(window)
            manager.update(time_delta)
            manager.draw_ui(window)
            pygame.display.flip()  # Обновление дисплея