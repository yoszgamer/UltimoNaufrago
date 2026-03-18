#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from pygame import Surface, Rect
from pygame.font import Font

class Menu:
    def __init__(self, window):
        self.window = window
        self.start_button_rect = Rect(0,0,220,60)
        self.start_button_rect.center = (480,420)
        self.start_clicked = False
        self.logo = pygame.image.load("asset/UI_gamelogo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (200, 100))
        self.icon_wasd = pygame.image.load("asset/UI_Tutorial_WASD.png").convert_alpha()
        self.icon_wasd = pygame.transform.scale(self.icon_wasd, (37, 25))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.checkStartClick(event)
            self.update()
            self.draw()

    def update(self, ):
        pass

    def draw(self, ):
        logo_x = (self.window.get_width() - self.logo.get_width()) // 2
        logo_y = 50
        icon_x = 370
        icon_y = 220

        self.window.blit(self.icon_wasd, (icon_x, icon_y))

        self.window.blit(self.logo, (logo_x, logo_y))
        self.menu_text(
            text_size=28,
            text="MOVIMENTAÇÃO",
            text_color=(255, 255, 255),
            text_center_pos=(500, 230)
        )

        self.menu_text(
            text_size=28,
            text="Sobreviva às hordas de animais",
            text_color=(255, 255, 255),
            text_center_pos=(480, 280)
        )

        # botão
        pygame.draw.rect(self.window, (200, 200, 200), self.start_button_rect)

        self.menu_text(
            text_size=32,
            text="NOVA PARTIDA",
            text_color=(0, 0, 0),
            text_center_pos=self.start_button_rect.center
        )

        pygame.display.flip()

    def checkStartClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.start_button_rect.collidepoint(event.pos):
                    print('startgame')
                    return True
        return False

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)