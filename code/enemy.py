#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.animator import Animator
from code.entity import Entity
from const import ENEMY_SPRITE_POS_W, ENEMY_SPRITE_POS_H, SPRITE_SCALE, ENEMY_FRAME_COUNT


class Enemy(Entity):
    type = {
        "crab": {
            "sprite": "asset/enemy_crab_spritesheet.png",
            "health": 40,
            "speed": 1.5,
            "damage": 5,
        },
        "snake": {
            "sprite": "asset/enemy_snake_spritesheet.png",
            "health": 30,
            "speed": 2.5,
            "damage": 6,
        }
    }
    def __init__(self, enemy_type, pos):
        stat = self.type[enemy_type]
        super().__init__(enemy_type, None, pos)
        self.health = stat["health"]
        self.speed = stat["speed"]
        self.damage = stat["damage"]
        self.animator = Animator(
            stat["sprite"],
            ENEMY_SPRITE_POS_W,
            ENEMY_SPRITE_POS_H,
            ENEMY_FRAME_COUNT,
            SPRITE_SCALE
        )

    def update(self):
        self.animator.update()

    def animate(self):
        self.animator.update(20)
        self.sprite = self.animator.get_frame(0)

    def chase(self, player):
        pass

    def attack(self, ):
        pass

    def draw(self, window, camera_y):
        sprite = self.animator.get_frame()
        window.blit(sprite, (self.rect.x, self.rect.y - camera_y))

