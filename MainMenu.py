import random

import pygame
import pygame_gui
from MainForCreative import terminate, MainForCreative, h
from select_circle import CreativeGame


def draw_text(window, text_info, position, colour, size):
    font = pygame.font.Font(None, size)
    text = font.render(text_info, True, colour)
    window.blit(text, text.get_rect(center=position))


def MainMenu(window: pygame.surface.Surface):  # Игра:
    manager = pygame_gui.UIManager(window.get_size(), "data/ui_theme.json")
    random_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 535),
                                                                           (window.get_width() // 2 - 50 - 10, 80)),
                                                 text='Рандом',
                                                 manager=manager,
                                                 object_id="#buttons_in_menu")
    creative_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window.get_width() // 2 + 10, 535),
                                                                             (window.get_width() // 2 - 50 - 10, 80)),
                                                   text='Пользовательский',
                                                   manager=manager,
                                                   object_id="#buttons_in_menu")

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
            manager.process_events(event_in_MainGame)

        window.fill((204, 229, 255))  # Установил нежно-голубой цвет фона дисплея
        manager.update(time_delta)
        manager.draw_ui(window)
        draw_text(window, 'Дорогой пользователь!', (window.get_width() // 2, 75), (0, 0, 255), 50)
        draw_text(window, 'Пожалуйста, выберите уровень', (window.get_width() // 2, 125), (0, 0, 255), 50)
        draw_text(window, 'сложности с 1-го по 4-й:', (window.get_width() // 2, 175), (0, 0, 255), 50)
        draw_text(window, 'Пожалуйста, выберите режим игры',
                  (window.get_width() // 2, 435), (0, 0, 255), 50)
        draw_text(window, '(способ выбора пустой ячейки):',
                  (window.get_width() // 2, 485), (0, 0, 255), 50)
        pygame.display.flip()  # Обновление дисплея


if __name__ == '__main__':  # Работа программы:
    pygame.init()
    MainMenu(pygame.display.set_mode((800, 693)))
