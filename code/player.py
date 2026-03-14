#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.entity import Entity
from const import SPRITE_POS_W, SPRITE_POS_H, SPRITE_SCALE


def get_sprite(sheet, col, row):
    rect = pygame.Rect(col * SPRITE_POS_W, row * SPRITE_POS_H, SPRITE_POS_W, SPRITE_POS_H)
    playersprite = pygame.Surface((SPRITE_POS_W, SPRITE_POS_H), pygame.SRCALPHA)
    playersprite.blit(sheet, (0, 0), rect)
    playersprite = pygame.transform.scale(playersprite,(SPRITE_POS_W * SPRITE_SCALE, SPRITE_POS_H * SPRITE_SCALE))
    return playersprite


class Player(Entity):
    def __init__(self, sprite, pos):
        super().__init__('Player', sprite, pos)
        self.health = 100
        self.speed = 4
        self.damage = 10
        character = pygame.image.load("asset/character.png").convert_alpha()
        self.direction = "down"
        self.frame = 0
        self.animation_timer = 0
        self.moving = False
        self.animations = {
            "idle": [
                get_sprite(character, 0, 0)
            ],
            "down": [
                get_sprite(character, 2, 1),
                get_sprite(character, 3, 1),
                get_sprite(character, 4, 1),
                get_sprite(character, 5, 1),
                get_sprite(character, 0, 1),
                get_sprite(character, 1, 1)
            ],
            "right": [
                get_sprite(character, 0, 2),
                get_sprite(character, 1, 2),
                get_sprite(character, 2, 2),
                get_sprite(character, 3, 2),
                get_sprite(character, 4, 2),
                get_sprite(character, 5, 2)
            ],
            "up": [
                get_sprite(character, 2, 3),
                get_sprite(character, 3, 3),
                get_sprite(character, 4, 3),
                get_sprite(character, 5, 3),
                get_sprite(character, 0, 3),
                get_sprite(character, 1, 3)
            ]
        }
        self.animations["left"] = [
            pygame.transform.flip(frame, True, False)
            for frame in self.animations["right"]
        ]
        self.rect.width = SPRITE_POS_W * SPRITE_SCALE
        self.rect.height = SPRITE_POS_H * SPRITE_SCALE

    def update(self, ):
        self.move()
        self.animate()

    def animate(self):
        if self.moving:
            self.animation_timer += 1
            if self.animation_timer > 10:
                self.animation_timer = 0
                self.frame += 1
                if self.frame >= len(self.animations[self.direction]):
                    self.frame = 0
        else:
            self.frame = 0

    def move(self):

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
            self.direction = "up"

        if keys[pygame.K_s]:
            dy += 1
            self.direction = "down"

        if keys[pygame.K_a]:
            dx -= 1
            self.direction = "left"

        if keys[pygame.K_d]:
            dx += 1
            self.direction = "right"

        self.moving = dx != 0 or dy != 0

        # normalizar diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        # aplicar movimento
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # limites da arena
        arena_left = 0
        arena_right = 960
        arena_top = 540
        arena_bottom = 960

        if self.rect.left < arena_left:
            self.rect.left = arena_left

        if self.rect.right > arena_right:
            self.rect.right = arena_right

        if self.rect.top < arena_top:
            self.rect.top = arena_top

        if self.rect.bottom > arena_bottom:
            self.rect.bottom = arena_bottom
    def attack(self, ):
        pass

    def takeDamage(self, ):
        pass

    def draw(self, window, camera_y):
        sprite = self.animations[self.direction][self.frame]
        window.blit(sprite, (self.rect.x, self.rect.y - camera_y))