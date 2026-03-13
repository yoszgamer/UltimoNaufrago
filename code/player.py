#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.entity import Entity


class Player(Entity):
    def __init__(self, sprite, pos):
        super().__init__('Player', sprite, pos)
        self.health = 100
        self.speed = 4
        self.damage = 10

    def update(self, ):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def attack(self, ):
        pass

    def takeDamage(self, ):
        pass
