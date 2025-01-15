import pygame

import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
win = pygame.display.set_mode((800, 693))
button = Button(win, 250, 350, 300, 150,  text='Start', fontSize=75,
                inactiveColour=(50, 100, 140), hoverColour=(70, 130, 170), radius=20, pressedColour=(30, 70, 100))

font = pygame.font.Font(None, 100)
text = font.render("The Peg Game", True, (50, 100, 140))

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((149, 192, 230))
    win.blit(text, (170, 200))
    pygame_widgets.update(events)
    pygame.display.update()