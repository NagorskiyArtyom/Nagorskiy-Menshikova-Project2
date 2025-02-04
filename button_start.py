import pygame
import json
import MainMenu


def buttonStart():
    # Загружаем настройки из JSON
    with open("custom_theme.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    # Инициализация pygame
    pygame.init()

    # Задаем размеры окна вручную, так как в JSON их нет
    WIDTH, HEIGHT = 800, 600  # Фиксированные значения для окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Window")

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
    button_rect = pygame.Rect((WIDTH - button_width) // 2, (HEIGHT - button_height) // 2, button_width, button_height)

    font = pygame.font.Font(None, font_size)
    text_surface = font.render("Начать", True, text_colour)
    text_rect = text_surface.get_rect(center=button_rect.center)

    button_color = normal_bg
    mouse_over = False
    mouse_click = False

    running = True
    while running:
        screen.fill((255, 255, 255))  # Фон белый

        # Обработка состояния кнопки (обычное, наведенное, активное)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            mouse_over = True
            if pygame.mouse.get_pressed()[0]:  # Если кнопка мыши нажата
                mouse_click = True
                button_color = active_bg
            else:
                button_color = hovered_bg
        else:
            mouse_over = False
            button_color = normal_bg

        # Рисуем кнопку с учетом состояния
        pygame.draw.rect(screen, button_color, button_rect, border_radius=corner_radius)
        pygame.draw.rect(screen, border_colour, button_rect, border_width,
                         border_radius=corner_radius)  # Рисуем границу
        screen.blit(text_surface, text_rect)

        # Проверяем, был ли клик по кнопке
        if mouse_click and button_rect.collidepoint(pygame.mouse.get_pos()):
            running = False  # Закрываем текущее окно
            MainMenu.MainMenu(pygame.display.set_mode((800, 693)))  # Запускаем главное меню

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':  # Запуск программы
    pygame.init()
    buttonStart()
