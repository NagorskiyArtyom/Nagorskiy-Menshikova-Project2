import pygame
import pygame_gui

import MainGame

pygame.init()
win = pygame.display.set_mode((800, 693))


def MainWindow(window):
    manager = pygame_gui.UIManager(window.get_size(), "custom_theme.json")
    pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((300, 300),
                                  (176, 63)), text='Начать', manager=manager)

    font = pygame.font.Font(None, 100)
    text = font.render("The Peg Game", True, (50, 100, 140))

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                MainGame.terminate()

        window.fill((149, 192, 230))
        window.blit(text, (170, 200))
        pygame.display.update()