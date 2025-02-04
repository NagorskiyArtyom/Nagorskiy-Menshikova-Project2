import math
import os
import sys
import pygame
import pygame_gui
import Main_Window
import button_exit
from MainGame import MainGame

holes = []
h = [(365, 117), (309, 222), (421, 222), (253, 327), (365, 327), (477, 327),
    (197, 432), (309, 432), (421, 432), (533, 432), (141, 537), (253, 537),
    (365, 537), (477, 537), (89, 537)]
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
    def __init__(self, the_complexity, figure, image, choosen_sprite):
        self.start_x, self.start_y = None, None
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
        self.empty_cells = []
        self.choosen_sprite = choosen_sprite
        self.empty_cells.append(self.choosen_sprite)

        self.add_things(figure, the_complexity)  # Установим начальное расположение фишек в фигуре

    def add_things(self, figure, the_complexity, k=0):
        if the_complexity == 1:  # Если мы проходим превый уровень - фигура - треугольник
            for row in range(0, 5):  # Проходим по ряду
                for col in range(4 - row, 4 + row + 1, 2):  # Проходим по столбцу
                    x = figure.get_coords()[0][0] + 126 + col * self.part_x - self.hole_radius
                    y = figure.get_coords()[1][1] + 115 + self.part_y * row - self.hole_radius
                    holes.append((k, x, y))
                    k += 1
                    if (x, y) != self.choosen_sprite:
                        thing = pygame.sprite.Sprite(self.things_group)  # Создаём фишку, которая автоматически запишется в
                        # группу спрайтов-фишек
                        thing.image = self.image  # Присваеваем ей изображение
                        thing.rect = thing.image.get_rect()  # Присваеваем ей размер
                        thing.rect.x, thing.rect.y = (x, y)  # Присваиваем ей координаты

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
                self.start_x, self.start_y = thing.rect.x, thing.rect.y
                break

    def check_possible_moves(self, window, things):
        font = pygame.font.Font(None, 36)
        no_moves_text = font.render("Нет возможных ходов!", True, (255, 0, 0))

        possible_move = False

        for sprite in things.things_group:
            sprite_center = (sprite.rect.centerx, sprite.rect.centery)

            for (i, x, y) in holes:
                distance = math.sqrt((sprite_center[0] - (x + things.hole_radius)) ** 2 +
                                     (sprite_center[1] - (y + things.hole_radius)) ** 2)

                if distance <= things.hole_radius and (x, y) in things.empty_cells:
                    possible_move = True
                    break
            if possible_move:
                break

        if not possible_move:
            window.blit(no_moves_text,
                        (window.get_width() // 2 - no_moves_text.get_width() // 2, 20))  # Выводим сообщение


    def snap_to_hole(self): # функция для проверки возможности поставить спрайт в ячейку
        if self.active_thing_index is not None:
            active_sprite = self.things_group.sprites()[-1]
            sprite_center = (active_sprite.rect.centerx, active_sprite.rect.centery)

            check_dis1 = math.sqrt((365 - 253) ** 2 + (117 - 327) ** 2) # рассчитывала расстояние между ячейками стоящими через один друг от друга
            # в данном примере 1 и 4 ячейка
            check_dis2 = math.sqrt((197 - 421) ** 2 + (432 - 432) ** 2) # а здесь 7 и 9 (координаты из переменной h) 238.0 224.0

            snapped = False
            for (i, x, y) in holes:

                # Вычисляем расстояние между центром спрайта и центром кружочка
                distance = math.sqrt((sprite_center[0] - (x + self.hole_radius)) ** 2 +
                                     (sprite_center[1] - (y + self.hole_radius)) ** 2)
                start_active = math.sqrt((self.start_x - x) ** 2 + (self.start_y - y) ** 2)
                if (distance <= self.hole_radius and (start_active == check_dis1 or start_active == check_dis2) and
                        (x, y) in self.empty_cells):  # Если расстояние меньше радиуса кружочка
                    dell_cell = ((x + self.start_x) // 2, (y + self.start_y) // 2) # кружок который впоследствии будем удалять
                    if dell_cell not in self.empty_cells: # проверяем удаляли мы эту фишку ранее

                        active_sprite.rect.center = (x + self.hole_radius, y + self.hole_radius)

                        self.empty_cells.remove((x, y))
                        self.empty_cells.append((self.start_x, self.start_y))

                        for sprite in self.things_group:
                            # Проверяем совпадение координат центра
                            if sprite.rect.centerx - 35 == dell_cell[0] and sprite.rect.centery - 35 == dell_cell[1]:
                                self.things_group.remove(sprite)  # Удаляем спрайт из группы

                                self.empty_cells.append(dell_cell)

                        snapped = True
                        break

            if not snapped:
                # Возвращаем спрайт на начальное место, если не попал в кружочек
                active_sprite.rect.x, active_sprite.rect.y = self.start_x, self.start_y

    def new_things_group(self, active_thing_index):  # Функция, переделывающая группу фишек так, чтобы фишка, которой
        # мы коснулись, была поверх других, т.е. Отрисовывалась последней - была 15-й фишкой
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
        self.snap_to_hole()
        self.active_thing_index, self.dx, self.dy = None, None, None  # "Активная" фишка исчезает, а следовательно и
        # точное расположение куросра в ней - тоже

    def draw_circles(self, scr):
        for (i, x, y) in holes:
            pygame.draw.circle(scr, colors[i], (x + 35, y + 35), self.hole_radius)


def terminate():  # Функция, прерывающая всю работу
    pygame.quit()
    sys.exit()


def MainForCreative(window: pygame.surface.Surface, complexity, choosen_sprite):  # Игра:
    global colors
    shapes = {1: Triangle(window), 2: None, 3: None, 4: None}  # Словарь фигур, соответствующих уровням, пока что
    # доступен только треугольник
    shape = shapes[complexity]  # Фигура соответствует уровню
    things = Things(1, shape, "yandex-logo.png", choosen_sprite)  # Фишки
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
                    MainForCreative(window, complexity, choosen_sprite)
                elif event_in_MainGame.ui_element == exit_button:
                    button_exit.exit_prompt(window)
                    #Main_Window.MainWindow(window)
            manager.process_events(event_in_MainGame)

        window.fill((204, 229, 255))  # Установил нежно-голубой цвет фона дисплея
        shape.render()  # Отрисовка фигуры
        things.draw_circles(window)
        things.render(window)
        manager.update(time_delta)
        manager.draw_ui(window)
        things.check_possible_moves(window, things)
        pygame.display.flip()  # Обновление дисплея