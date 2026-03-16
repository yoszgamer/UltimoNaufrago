#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

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
        self.attack_cooldown = 60
        self.attack_timer = 0
        self.animator = Animator(
            stat["sprite"],
            ENEMY_SPRITE_POS_W,
            ENEMY_SPRITE_POS_H,
            ENEMY_FRAME_COUNT,
            SPRITE_SCALE
        )

    def update(self, player):
        self.chase(player)
        self.animator.update()
        self.attack(player)

    def animate(self):
        self.animator.update(20)
        self.sprite = self.animator.get_frame(0)

    def chase(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            dx /= distance
            dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def attack(self, player):

        if self.rect.colliderect(player.rect):

            if self.attack_timer <= 0:
                player.takeDamage(self.damage)
                self.attack_timer = self.attack_cooldown

        if self.attack_timer > 0:
            self.attack_timer -= 1

    def draw(self, window, camera_y):
        sprite = self.animator.get_frame()
        window.blit(sprite, (self.rect.x, self.rect.y - camera_y))

