#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame


class Entity:
    def __init__(self, name, sprite, pos):
        self.name = name
        self.sprite = sprite
        if sprite:
            self.rect = sprite.get_rect(center=pos)
        else:
            self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

    def update(self, ):
        pass

    def draw(self, window, camera_y):
        window.blit(self.sprite, (self.rect.x, self.rect.y - camera_y))
