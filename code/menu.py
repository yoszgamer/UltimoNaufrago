#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.game import Game

game = Game()

class Menu:
    def __init__(self):
        self.tutorial_text = None
        self.start_button_rect = None

    def run(self, ):
        while True:


    def update(self, ):
        pass

    def draw(self, ):
        pass

    def checkStartClick(self, ):
        pass

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        game.get_window().blit(source=text_surf, dest=text_rect)