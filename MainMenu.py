import random
import pygame
import pygame_gui
from MainForCreative import terminate, MainForCreative, h
from Main_Window import MainWindow
from select_circle import CreativeGame


def draw_text(window, text_info, position, colour, size):
    font = pygame.font.Font(None, size)
    text = font.render(text_info, True, colour)
    window.blit(text, text.get_rect(center=position))


def MainMenu(window: pygame.surface.Surface):  # Игра:
    k = window.get_width() // window.get_height()
    a = 2 * window.get_height() // 27
    manager = pygame_gui.UIManager(window.get_size(), "data/ui_theme.json")
    random_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window.get_width() // 6 + 2 * a * k,
                                                                            window.get_height() // 2 + 0.5 * a),
                                                                           (4 * window.get_width() // 12 - 2.5 * a * k,
                                                                            2 * a)),
                                                 text='Рандом',
                                                 manager=manager,
                                                 object_id="#buttons_in_menu")
    creative_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5 * window.get_width() // 6 - 2 * a * k
                                                                              - (4 * window.get_width() // 12 -
                                                                                 2.5 * a * k),
                                                                              window.get_height() // 2 + 0.5 * a),
                                                                             (4 * window.get_width() // 12 -
                                                                              2.5 * a * k, 2 * a)),
                                                   text='Вручную',
                                                   manager=manager,
                                                   object_id="#buttons_in_menu")
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((11 * window.get_width() // 12 -
                                                                          (4 * window.get_width() // 12 - 2.5 * a * k)
                                                                          // 3, window.get_height() // 12 - a // 3),
                                                                         ((4 * window.get_width() // 12 -
                                                                          2.5 * a * k) // 1.5, a // 1.5)),
                                               text='Выйти',
                                               manager=manager,
                                               object_id="#exit_in_menu")

    clock = pygame.time.Clock()
    running_in_MainGame = True
    while running_in_MainGame:  # Игра:
        time_delta = clock.tick(60) / 1000.0

        for event_in_MainGame in pygame.event.get():  # Отслеживаем события:
            if event_in_MainGame.type == pygame.QUIT:
                terminate()
            if event_in_MainGame.type == pygame_gui.UI_BUTTON_PRESSED:
                if event_in_MainGame.ui_element == random_button:
                    MainForCreative(window, random.choice(h))
                elif event_in_MainGame.ui_element == creative_button:
                    CreativeGame(window)
                elif event_in_MainGame.ui_element == exit_button:
                    MainWindow(window)
            manager.process_events(event_in_MainGame)

        bg = pygame.image.load('data/second_window.png')
        window.blit(bg, (0, 0))
        pygame.draw.rect(window, (204, 229, 255),
                         pygame.Rect((window.get_width() // 6, window.get_height() // 6),
                                     (4 * window.get_width() // 6, 4 * window.get_height() // 6)),
                         border_radius=15)
        pygame.draw.rect(window, (4, 29, 55),
                         pygame.Rect((window.get_width() // 6, window.get_height() // 6),
                                     (4 * window.get_width() // 6, 4 * window.get_height() // 6)),
                         2, 15)
        manager.update(time_delta)
        manager.draw_ui(window)
        draw_text(window, 'Дорогой пользователь!', (window.get_width() // 2, window.get_height() // 6 + 2 * a),
                  (0, 0, 255), 40)
        draw_text(window, 'Пожалуйста, выберите режим игры', (window.get_width() // 2,
                                                              window.get_height() // 6 + 3 * a),
                  (0, 0, 255), 40)
        draw_text(window, '(способ выбора пустой ячейки):', (window.get_width() // 2,
                                                             window.get_height() // 6 + 4 * a),
                  (0, 0, 255), 40)
        pygame.display.flip()  # Обновление дисплея


if __name__ == '__main__':  # Работа программы:
    pygame.init()
    MainMenu(pygame.display.set_mode((800, 693)))
