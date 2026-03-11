#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(640, 480))
        self.state = None
        self.camera_y = None
        self.target_camera_y = None
        self.menu = None
        self.level = None
        self.fishing = None

    def run(self, window):
        while True:
            menu = Menu(self.window)
            menu.run()
            pass
            # Check for all events
            #for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        pygame.quit()  # Close window
            #        quit()  # End pygame

    def update(self, ):
        pass

    def draw(self, ):
        pass

    def changeState(self, ):
        pass

    def moveCamera(self, ):
        pass

