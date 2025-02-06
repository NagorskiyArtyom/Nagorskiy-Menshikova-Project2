import pygame
import json
import sys
import pygame_gui

import MainForCreative
from button_start import buttonStart


def Win(window, selected_sprite):
    sound = pygame.mixer.Sound("data/mixkit-game-level-completed-2059.wav")
    sound.play()
    # Загружаем настройки из JSON
    with open("data/ct_exit.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    # Настройки окна
    WIDTH, HEIGHT = config["window"]["width"], config["window"]["height"]
    pygame.display.set_caption(config["window"]["title"])

    k = window.get_width() // window.get_height()
    a = 2 * window.get_height() // 27

    # Текст сообщения
    font = pygame.font.Font(None, 50)
    text1_surface = font.render('ПОБЕДА!', True, (0, 225, 0))
    text1_rect = text1_surface.get_rect(center=(WIDTH // 2, window.get_height() // 6 + 2.5 * a))
    text2_surface = font.render("Вы выиграли! Поздравляем!", True, (0, 225, 0))
    text2_rect = text2_surface.get_rect(center=(WIDTH // 2, window.get_height() // 6 + 3.5 * a))

    manager = pygame_gui.UIManager(window.get_size(), "data/ui_theme.json")
    retry_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window.get_width() // 6 + 2 * a * k,
                                                                           window.get_height() // 2 + 0.5 * a),
                                                                          (4 * window.get_width() // 12 - 2.5 * a * k,
                                                                           2 * a)),
                                                text='Заново',
                                                manager=manager,
                                                object_id="#buttons_in_menu")
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5 * window.get_width() // 6 - 2 * a * k
                                                                          - (4 * window.get_width() // 12 -
                                                                             2.5 * a * k), window.get_height() // 2 +
                                                                          0.5 * a), (4 * window.get_width() // 12 -
                                                                                     2.5 * a * k, 2 * a)),
                                               text='Выйти',
                                               manager=manager,
                                               object_id="#buttons_in_menu")

    clock = pygame.time.Clock()
    json_window_open = True
    while json_window_open:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == retry_button:
                    MainForCreative.MainForCreative(window, selected_sprite)
                elif event.ui_element == exit_button:
                    sound = pygame.mixer.Sound("data/mixkit-arrow-whoosh-1491 (mp3cut.net).wav")
                    sound.play()
                    buttonStart(window)
            manager.process_events(event)

        pygame.draw.rect(window, (178, 255, 229),
                         pygame.Rect((window.get_width() // 6, window.get_height() // 6),
                                     (4 * window.get_width() // 6, 4 * window.get_height() // 6)),
                         border_radius=15)
        pygame.draw.rect(window, (4, 29, 55),
                         pygame.Rect((window.get_width() // 6, window.get_height() // 6),
                                     (4 * window.get_width() // 6, 4 * window.get_height() // 6)),
                         1, 15)
        window.blit(text1_surface, text1_rect)
        window.blit(text2_surface, text2_rect)
        # Рисуем кнопки
        manager.update(time_delta)
        manager.draw_ui(window)
        pygame.display.flip()
