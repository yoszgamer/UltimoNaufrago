#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.entity import Entity
from const import SPRITE_POS_W, SPRITE_POS_H, SPRITE_SCALE


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
                self.get_sprite(character, 0, 0)
            ],
            "down": [
                self.get_sprite(character, 2, 1),
                self.get_sprite(character, 3, 1),
                self.get_sprite(character, 4, 1),
                self.get_sprite(character, 5, 1),
                self.get_sprite(character, 0, 1),
                self.get_sprite(character, 1, 1)
            ],
            "right": [
                self.get_sprite(character, 0, 2),
                self.get_sprite(character, 1, 2),
                self.get_sprite(character, 2, 2),
                self.get_sprite(character, 3, 2),
                self.get_sprite(character, 4, 2),
                self.get_sprite(character, 5, 2)
            ],
            "up": [
                self.get_sprite(character, 2, 3),
                self.get_sprite(character, 3, 3),
                self.get_sprite(character, 4, 3),
                self.get_sprite(character, 5, 3),
                self.get_sprite(character, 0, 3),
                self.get_sprite(character, 1, 3)
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
        self.moving = False
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.direction = "up"
            self.moving = True
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.direction = "down"
            self.moving = True
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = "left"
            self.moving = True
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = "right"
            self.moving = True

    def attack(self, ):
        pass

    def takeDamage(self, ):
        pass

    def get_sprite(self, sheet, col, row):
        rect = pygame.Rect(col * SPRITE_POS_W, row * SPRITE_POS_H, SPRITE_POS_W, SPRITE_POS_H)
        playersprite = pygame.Surface((SPRITE_POS_W, SPRITE_POS_H), pygame.SRCALPHA)
        playersprite.blit(sheet, (0, 0), rect)
        playersprite = pygame.transform.scale(playersprite,(SPRITE_POS_W * SPRITE_SCALE, SPRITE_POS_H * SPRITE_SCALE))
        return playersprite

    def draw(self, window, camera_y):
        sprite = self.animations[self.direction][self.frame]
        window.blit(sprite, (self.rect.x, self.rect.y - camera_y))