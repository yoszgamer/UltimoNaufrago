#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code import player
from code.menu import Menu
from code.player import Player
from const import WIN_WIDTH, WIN_HEIGHT, STATE_MENU, STATE_GAME, STATE_FISHING


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.background = pygame.image.load("asset/background.png").convert()
        self.state = STATE_MENU
        self.camera_y = 0
        self.target_camera_y = 0
        self.menu = Menu(self.window)
        self.player = Player(None, (480, 720))
        #self.level = None
        #self.fishing = None
        self.fps = pygame.time.Clock()

    def run(self):
        while True:
            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close window
                    quit()  # End pygame
                if self.state == STATE_MENU:
                    if self.menu.checkStartClick(event):
                        self.changeState(STATE_GAME)
            self.fps.tick(60)
            self.update()
            self.draw()

    def update(self):
        self.moveCamera()

        if self.state == STATE_GAME:
            self.player.update()

    def draw(self):
        self.window.blit(self.background, (0, -self.camera_y))
        if self.state == STATE_MENU:
            self.menu.draw()
        if self.state == STATE_GAME:
            self.player.draw(self.window, self.camera_y)
        pygame.display.flip()

    def changeState(self, new_state):
        self.state = new_state
        if new_state == STATE_MENU:
            self.target_camera_y = 0
        elif new_state == STATE_GAME:
            self.target_camera_y = 540
        elif new_state == STATE_FISHING:
            self.target_camera_y = 960

    def moveCamera(self):
        speed = 12
        if self.camera_y < self.target_camera_y:
            self.camera_y += speed