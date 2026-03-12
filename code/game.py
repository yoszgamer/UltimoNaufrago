#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from const import WIN_WIDTH, WIN_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        #self.state = None
        #self.camera_y = None
        #self.target_camera_y = None
        #self.menu = None
        #self.level = None
        #self.fishing = None

    def run(self):
        while True:
            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close window
                    quit()  # End pygame
            background = pygame.image.load("asset/background.png").convert()
            self.window.blit(background, (0, 0))
            pygame.display.flip()

    def update(self):
        pass

    def draw(self):
        pass

    def changestate(self):
        pass

    def movecamera(self):
        pass

    def get_window(self):
        return self.window