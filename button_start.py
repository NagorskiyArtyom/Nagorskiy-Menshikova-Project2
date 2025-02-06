import sys
import pygame
import json
import MainMenu
from test2 import MovingText


def buttonStart(screen):
    # Загружаем настройки из JSON
    with open("data/custom_theme.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    # Настройки кнопки
    button_config = config["button"]["#center_button"]
    normal_bg = pygame.Color(button_config["normal_bg"])
    hovered_bg = pygame.Color(button_config["hovered_bg"])
    active_bg = pygame.Color(button_config["active_bg"])
    border_width = button_config["border_width"]
    border_colour = pygame.Color(button_config["border_colour"])
    corner_radius = button_config["corner_radius"]

    # Текст кнопки
    font_size = button_config["text"]["font_size"]
    text_colour = pygame.Color(button_config["text"]["text_colour"])

    # Создаем прямоугольник для кнопки
    button_width = 300  # Вы можете изменить эти значения или добавить в JSON
    button_height = 80
    button_rect = pygame.Rect((screen.get_width() - button_width) // 2, 4 * screen.get_height() // 5 -
                              button_height // 2, button_width, button_height)

    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Начать", True, text_colour)
    text_rect = text_surface.get_rect(center=button_rect.center)
    clock = pygame.time.Clock()
    mouse_click = False

    font = pygame.font.Font(None, 36)
    text_obj = MovingText(["Nagorskiy A. & Menshikova E.", "Яндекс лицей 2024-2025"],
                          font)  # Создаем один объект текста

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Обработка состояния кнопки (обычное, наведенное, активное)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Если кнопка мыши нажата
                mouse_click = True
                button_color = active_bg
            else:
                button_color = hovered_bg
        else:
            button_color = normal_bg

        screen.fill((149, 192, 230))  # Заполняем фон
        text_obj.update()
        text_obj.draw(screen)

        MainMenu.draw_text(screen, 'THE', (screen.get_width() // 2, screen.get_height() // 5),
                           (0, 0, 255), 125)
        MainMenu.draw_text(screen, 'PEG GAME', (screen.get_width() // 2, 2 * screen.get_height() // 5),
                           (0, 0, 255), 125)
        MainMenu.draw_text(screen, 'N.A & M.E', (screen.get_width() // 2, 3 * screen.get_height() // 5),
                           (0, 0, 255), 50)

        # Рисуем кнопку с учетом состояния
        pygame.draw.rect(screen, button_color, button_rect, border_radius=corner_radius)
        pygame.draw.rect(screen, border_colour, button_rect, border_width,
                         border_radius=corner_radius)  # Рисуем границу
        screen.blit(text_surface, text_rect)

        # Проверяем, был ли клик по кнопке
        if mouse_click and button_rect.collidepoint(pygame.mouse.get_pos()):
            running = False  # Закрываем текущее окно
            MainMenu.MainMenu(screen)  # Запускаем главное меню
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':  # Запуск программы
    pygame.init()
    pygame.display.set_caption("THE PEG GAME. A.K.")
    buttonStart(pygame.display.set_mode((800, 693)))
