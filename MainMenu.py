import pygame
import pygame_gui

import Main_Window
from MainGame import terminate, Things, Triangle


def MainMenu(window: pygame.surface.Surface):  # Игра:
    manager = pygame_gui.UIManager(window.get_size())
    btn1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, window.get_height() // 2 - 80),
                                                                         (160, 160)),
                                               text='Выйти',
                                               manager=manager)
    btn2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50 + 160 + 20,
                                                                            window.get_height() // 2 - 80),
                                                                           (160, 160)),
                                                 text='Заново',
                                                 manager=manager)
    btn3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50 + 160 * 2 + 20 * 2,
                                                                            window.get_height() // 2 - 80),
                                                                           (160, 160)),
                                                 text='Заново',
                                                 manager=manager)
    btn4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50 + 160 * 3 + 20 * 3
                                                                            , window.get_height() // 2 - 80),
                                                                           (160, 160)),
                                                 text='Заново',
                                                 manager=manager)
    clock = pygame.time.Clock()
    running_in_MainGame = True
    while running_in_MainGame:  # Игра:
        time_delta = clock.tick(60) / 1000.0

        for event_in_MainGame in pygame.event.get():  # Отслеживаем события:
            if event_in_MainGame.type == pygame.QUIT:
                terminate()
            if event_in_MainGame.type == pygame_gui.UI_BUTTON_PRESSED:
                if event_in_MainGame.ui_element == btn1:
                    pass
                elif event_in_MainGame.ui_element == btn2:
                    pass
            manager.process_events(event_in_MainGame)

        window.fill((204, 229, 255))  # Установил нежно-голубой цвет фона дисплея
        manager.update(time_delta)
        manager.draw_ui(window)
        font = pygame.font.Font(None, 50)
        text = font.render("Hello, Pygame!", True, (100, 255, 100))
        text_x = window.get_width() // 2 - text.get_width() // 2
        text_y = window.get_height() // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        window.blit(text, (text_x, text_y))
        pygame.display.flip()  # Обновление дисплея


if __name__ == '__main__':  # Работа программы:
    pygame.init()
    MainMenu(pygame.display.set_mode((800, 693)))