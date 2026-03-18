#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code import player, enemySpawner
from code.HUD import HUD
from code.enemySpawner import EnemySpawner
from code.fishingGame import FishingGame
from code.menu import Menu
from code.player import Player
from const import WIN_WIDTH, WIN_HEIGHT, STATE_MENU, STATE_GAME, STATE_FISHING
from code.enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.background = pygame.image.load("asset/background.png").convert()
        self.state = STATE_MENU
        self.camera_y = 0
        self.target_camera_y = 0
        self.menu = Menu(self.window)
        self.fishingGame = FishingGame()
        self.player = Player(None, (480, 720))
        self.hud = HUD()
        #self.level = None
        #self.fishing = None
        self.fps = pygame.time.Clock()
        self.spawner = EnemySpawner()
        self.enemies = [
            Enemy("crab", (200, 700)),
            Enemy("snake", (600, 700))
        ]
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
                if self.state == STATE_FISHING:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.fishingGame.checkInput(event.pos)

            self.fps.tick(60)
            self.update()
            self.draw()

    def update(self):
        self.moveCamera()
        if self.state == STATE_GAME:
            self.player.update(self.enemies)
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            for enemy in self.enemies:
                enemy.update(self.player)
            self.spawner.update(self.enemies, self.player)
            if self.spawner.isWaveFinished(self.enemies):
                self.changeState(STATE_FISHING)
                self.fishingGame.start(self.player)

        elif self.state == STATE_FISHING:
            self.fishingGame.update()

            if self.fishingGame.is_finished():
                self.fishingGame.giveReward(self.player)

                self.spawner.startWave()
                self.enemies.clear()
                self.changeState(STATE_GAME)

    def draw(self):
        self.window.blit(self.background, (0, -self.camera_y))
        if self.state == STATE_MENU:
            self.menu.draw()
        if self.state == STATE_GAME:
            for enemy in self.enemies:
                enemy.draw(self.window, self.camera_y)
            self.player.draw(self.window, self.camera_y)
            self.hud.draw(self.window, self.player, self.spawner)
        if self.state == STATE_FISHING:
            self.player.draw(self.window, self.camera_y)
            self.fishingGame.draw(self.window)
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
            if self.camera_y > self.target_camera_y:
                self.camera_y = self.target_camera_y
        elif self.camera_y > self.target_camera_y:
            self.camera_y -= speed
            if self.camera_y < self.target_camera_y:
                self.camera_y = self.target_camera_y