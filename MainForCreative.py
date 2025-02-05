import math
import os
import sys
import time

import pygame
import pygame_gui
import button_exit
import lose_window
import win_window

holes = []
h = [(365, 117), (309, 222), (421, 222), (253, 327), (365, 327), (477, 327),
     (197, 432), (309, 432), (421, 432), (533, 432), (141, 537), (253, 537),
     (365, 537), (477, 537), (589, 537)]


def load_image(name, colorkey=None):  # Возвращает Surface, на котором расположено изображение «в натуральную величину»
    fullname = os.path.join('data', name)  # Получаем полный путь к файлу, содержащему изображение нашего спрайта
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()  # Завершаем работу программы и сообщаем про ошибку
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:  # Функция сама возьмет прозрачным цветом левый верхний угол изображения, обычно это будет
            # цвет фона, который хочется сделать прозрачным.
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)  # Переданный цвет станет прозрачным
    else:
        image = image.convert_alpha()  # Загруженное изображение сохранит прозрачность
    return image


class Triangle:
    def __init__(self, window: pygame.surface.Surface):
        self.window = window
        self.width = window.get_width() - 50 * 2  # Значение стороны равностороннего треугольника с отступами по 50
        # пикслей от краёв окна
        self.height = int((self.width // 2) * math.sqrt(3))  # Значение высоты этого треугольника

    def get_coords(self):  # Функция, которая выдаёт координаты вершин треугольника, для его отрисовки
        return [(50, self.window.get_height() - 50),
                (self.window.get_width() * 0.5, self.window.get_height() - 50 - self.height),
                (self.window.get_width() - 50, self.window.get_height() - 50)]

    def render(self):  # Функция, отрисовывающая треугольник
        pygame.draw.polygon(self.window, (0, 0, 255), self.get_coords())


class Things:  # Класс, посвящённый всем фишкам, как группе
    def __init__(self, the_complexity, figure, image, selected_sprite=None):
        self.no_moves = False
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
        self.selected_sprite = selected_sprite
        self.empty_cells.append(self.selected_sprite)

        self.check_dis1 = math.sqrt((365 - 253) ** 2 + (
                    117 - 327) ** 2)  # рассчитывала расстояние между ячейками стоящими через один друг от друга
        # в данном примере 1 и 4 ячейка
        self.check_dis2 = math.sqrt(
            (197 - 421) ** 2 + (432 - 432) ** 2)  # а здесь 7 и 9 (координаты из переменной h) 238.0 224.0

        self.add_things(figure, the_complexity)  # Установим начальное расположение фишек в фигуре

    def add_things(self, figure, the_complexity, k=0):
        if the_complexity == 1:  # Если мы проходим превый уровень - фигура - треугольник
            for row in range(0, 5):  # Проходим по ряду
                for col in range(4 - row, 4 + row + 1, 2):  # Проходим по столбцу
                    x = figure.get_coords()[0][0] + 126 + col * self.part_x - self.hole_radius
                    y = figure.get_coords()[1][1] + 115 + self.part_y * row - self.hole_radius
                    holes.append((k, x, y))
                    k += 1
                    if (x, y) != self.selected_sprite:
                        thing = pygame.sprite.Sprite(self.things_group)  # Создаём фишку, которая автоматически
                        # запишется в группу спрайтов-фишек
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

    def check_possible_moves(self):
        """Проверяет, можно ли сделать хотя бы один ход. Если нет - включает флаг `self.no_moves`."""
        self.no_moves = False  # По умолчанию считаем, что ходы возможны
        k = 0
        for sprite in self.things_group.sprites():
            sprite_x, sprite_y = sprite.rect.centerx - 35, sprite.rect.centery - 35  # Центр фишки
            for (i, x, y) in holes:
                # Вычисляем расстояние между центром спрайта и центром кружочка
                start_active = math.sqrt((sprite_x - x) ** 2 + (sprite_y - y) ** 2)
                dell_cell = ((x + sprite_x) // 2, (y + sprite_y) // 2)
                if (start_active == self.check_dis1 or start_active == self.check_dis2) and (x, y) in self.empty_cells \
                        and dell_cell not in self.empty_cells:  # Если расстояние меньше радиуса кружочка
                    k += 1
                    break
        if k == 0:
            self.no_moves = True
        if len(self.things_group.sprites()) == 1:
            self.no_moves = None

    def draw_no_moves_message(self, window, selected_sprite):
        """Выводит текст 'Нет возможных ходов!' на экран, если `self.no_moves == True`."""
        if self.no_moves:
            time.sleep(0.5)
            lose_window.Lose(window, selected_sprite)
        elif self.no_moves is None:
            time.sleep(0.5)
            win_window.Win(window, selected_sprite)

    def get_end_click(self):
        """Вызывается при отпускании фишки."""
        self.snap_to_hole()
        self.check_possible_moves()  # Проверяем возможные ходы после движения
        self.active_thing_index, self.dx, self.dy = None, None, None

    def snap_to_hole(self):  # функция для проверки возможности поставить спрайт в ячейку
        if self.active_thing_index is not None:
            active_sprite = self.things_group.sprites()[-1]
            sprite_center = (active_sprite.rect.centerx, active_sprite.rect.centery)
            snapped = False
            for (i, x, y) in holes:
                # Вычисляем расстояние между центром спрайта и центром кружочка
                distance = math.sqrt((sprite_center[0] - (x + self.hole_radius)) ** 2 +
                                     (sprite_center[1] - (y + self.hole_radius)) ** 2)
                start_active = math.sqrt((self.start_x - x) ** 2 + (self.start_y - y) ** 2)
                if (distance <= self.hole_radius and (start_active == self.check_dis1 or
                                                      start_active == self.check_dis2) and (x, y) in self.empty_cells):
                    # Если расстояние меньше радиуса кружочка
                    dell_cell = ((x + self.start_x) // 2, (y + self.start_y) // 2)  # кружок который впоследствии будем
                    # удалять
                    if dell_cell not in self.empty_cells:  # проверяем удаляли мы эту фишку ранее

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
        #  Мы коснулись, была поверх других, т.е. Отрисовывалась последней - была 15-й фишкой
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

    def draw_circles(self, scr):
        for (i, x, y) in holes:
            pygame.draw.circle(scr, (204, 229, 255), (x + 35, y + 35), self.hole_radius)

    def boarder_for_empty_cels(self, window):
        for circle in self.empty_cells:
            pygame.draw.circle(window, (0, 235, 0), (circle[0] + self.hole_radius, circle[1] + self.hole_radius),
                               self.hole_radius, width=5)
        pygame.draw.circle(window, (117, 117, 117), (self.start_x + self.hole_radius, self.start_y + self.hole_radius),
                           self.hole_radius, width=5)


def terminate():  # Функция, прерывающая всю работу
    pygame.quit()
    sys.exit()


def MainForCreative(window: pygame.surface.Surface, selected_sprite):  # Игра:
    shape = Triangle(window)  # Фигура соответствует уровню
    things = Things(1, shape, "yandex-logo.png", selected_sprite)  # Фишки
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
    flag = False
    while running_in_MainGame:  # Игра:
        time_delta = clock.tick(60) / 1000.0
        things.draw_no_moves_message(window, selected_sprite)
        for event_in_MainGame in pygame.event.get():  # Отслеживаем события:
            if event_in_MainGame.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event_in_MainGame.type == pygame.MOUSEBUTTONDOWN:
                things.get_click(pygame.mouse.get_pos())
                if things.active_thing_index is not None:
                    return_button.disable()
                    exit_button.disable()
                    flag = True
            if event_in_MainGame.type == pygame.MOUSEMOTION:
                things.get_move(window, pygame.mouse.get_pos())
            if event_in_MainGame.type == pygame.MOUSEBUTTONUP:
                return_button.enable()
                exit_button.enable()
                flag = False
                things.get_end_click()

            if event_in_MainGame.type == pygame_gui.UI_BUTTON_PRESSED:
                if event_in_MainGame.ui_element == return_button:
                    MainForCreative(window, selected_sprite)
                elif event_in_MainGame.ui_element == exit_button:
                    button_exit.exit_prompt(window)
                    #  Main_Window.MainWindow(window)
            manager.process_events(event_in_MainGame)
        window.fill((149, 192, 230))  # Установил нежно-голубой цвет фона дисплея
        manager.update(time_delta)
        manager.draw_ui(window)
        shape.render()  # Отрисовка фигуры
        things.draw_circles(window)
        if flag:
            things.boarder_for_empty_cels(window)
        things.render(window)
        manager.update(time_delta)
        manager.draw_ui(window)
        pygame.display.flip()  # Обновление дисплея
