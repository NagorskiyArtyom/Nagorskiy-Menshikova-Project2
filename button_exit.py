import pygame
import json
import subprocess


def exit_prompt(window):
    # Загружаем настройки из JSON
    with open("data/ct_exit.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    # Настройки окна
    WIDTH, HEIGHT = config["window"]["width"], config["window"]["height"]
    screen = window  # Используем переданное окно
    pygame.display.set_caption(config["window"]["title"])

    # Текст сообщения
    text_config = config["text"]
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text_config["message"], True, tuple(text_config["color"]))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, text_config["y"]))

    # Настройки кнопок
    buttons = config["buttons"]
    exit_button = pygame.Rect(buttons["exit"]["x"], buttons["exit"]["y"], buttons["exit"]["width"],
                              buttons["exit"]["height"])
    cancel_button = pygame.Rect(buttons["cancel"]["x"], buttons["cancel"]["y"], buttons["cancel"]["width"],
                                buttons["cancel"]["height"])

    exit_color = tuple(buttons["exit"]["color"])
    exit_text_color = tuple(buttons["exit"]["text_color"])
    cancel_color = tuple(buttons["cancel"]["color"])
    cancel_text_color = tuple(buttons["cancel"]["text_color"])

    exit_text = font.render(buttons["exit"]["text"], True, exit_text_color)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)

    cancel_text = font.render(buttons["cancel"]["text"], True, cancel_text_color)
    cancel_text_rect = cancel_text.get_rect(center=cancel_button.center)

    json_window_open = True
    while json_window_open:
        screen.fill((255, 255, 255))  # Фон белый
        screen.blit(text_surface, text_rect)

        # Рисуем кнопки
        pygame.draw.rect(screen, exit_color, exit_button, border_radius=5)
        pygame.draw.rect(screen, cancel_color, cancel_button, border_radius=5)
        screen.blit(exit_text, exit_text_rect)
        screen.blit(cancel_text, cancel_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                json_window_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    json_window_open = False
                    # Запуск игры или выход, если нужно
                    if buttons["exit"]["action"] == "exit_game":
                        pygame.quit()
                        subprocess.run(["python", "button_start.py"])  # Запуск другого скрипта или выход
                if cancel_button.collidepoint(event.pos):
                    # Закрываем окно
                    json_window_open = False
