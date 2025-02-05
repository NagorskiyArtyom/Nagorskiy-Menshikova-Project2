import math
import pygame
import pygame_gui
import button_exit
from MainForCreative import MainForCreative, Triangle, terminate

colors = [(170, 200, 230)] * 15  # Цвета для всех ячеек

pygame.init()
pygame.display.set_caption('CreativeGame')
window_surface = pygame.display.set_mode((800, 693))
background = pygame.Surface((800, 693))

manager = pygame_gui.UIManager((800, 693), "data/ui_theme.json")
exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_surface.get_width() - 50 - 176,
                                                                      window_surface.get_height() - 655),
                                                                     (176, 63)), text='Выйти', manager=manager)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_surface.get_width() - 50 - 176,
                                                                       window_surface.get_height() - 578),
                                                                      (176, 63)), text='Начать', manager=manager)


def draw_text(window, text_info, position, colour, size):
    font = pygame.font.Font(None, size)
    text = font.render(text_info, True, colour)
    window.blit(text, text.get_rect(center=position))


def CreativeGame(window):  # Функци для ползовательского режима
    global colors
    shape = Triangle(window)  # Фигура соответствует уровню
    false_mess = ""  # Локальное сообщение внутри функции
    please = ''
    holes = [(0, 365, 117), (1, 309, 222), (2, 421, 222), (3, 253, 327), (4, 365, 327), (5, 477, 327),
             (6, 197, 432), (7, 309, 432), (8, 421, 432), (9, 533, 432), (10, 141, 537), (11, 253, 537),
             (12, 365, 537), (13, 477, 537), (14, 589, 537)]
    clicks_pos = []
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        x1, y1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_sprite = None  # координаты выбранной ячейки равны None
                colors = [(170, 200, 230)] * 15
                for (i, x, y) in holes:
                    if math.hypot(x1 - (x + 35), y1 - (y + 35)) <= 30:
                        colors[i] = (130, 130, 130)
                        selected_sprite = (x, y)  # координаты выбранной ячейки
                        # если сообщение о просьбе выбрать ячейку уже есть на моменте нажатия ячейки -
                        # сообщение исчезает
                        if false_mess != '':
                            false_mess = ''
                            please = ''
                clicks_pos.append(selected_sprite)  # в список добавляется либо координаты ячейки, либо None
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    # если предпоследнее (тк последнее это нажатие на кнопку 'начать') нажатие - None, меняем сообщение
                    if ((len(clicks_pos) > 1 and clicks_pos[-2] is None)
                            or (len(clicks_pos) == 1 and clicks_pos[0] is None)):
                        please = "Пожалуйста, "
                        false_mess = "выберите пустую ячейку"
                    else:
                        selected_sprite = clicks_pos[-2]
                        MainForCreative(window, selected_sprite)
                elif event.ui_element == exit_button:
                    button_exit.exit_prompt(window)
                    # Main_Window.MainWindow(window)

            manager.process_events(event)

        window_surface.fill((204, 229, 255))  # Фон
        # Рисуем сообщение, если оно есть
        draw_text(window_surface, please, (190, 30), (0, 0, 255), 40)  # Выводим сообщения
        draw_text(window_surface, false_mess, (190, 60), (0, 0, 255), 40)
        shape.render()
        for (i, x, y), color in zip(holes, colors):
            pygame.draw.circle(window_surface, color, (x + 35, y + 35), 35)
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        pygame.display.update()
