#!/usr/bin/python
# -*- coding: utf-8 -*-

class Entity:
    def __init__(self, name, sprite, pos):
        self.name = name
        self.sprite = sprite
        self.rect = self.sprite.get_rect(center=pos)

    def update(self, ):
        pass

    def draw(self, window, camera_y):
        window.blit(self.sprite, (self.rect.x, self.rect.y - camera_y))
