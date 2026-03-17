#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.entity import Entity
from code.weapon import Weapon
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
        self.damage = 50
        self.attack_cooldown = 25
        self.attack_timer = 0
        self.attack_duration = 8
        self.attack_active = 0
        self.hit_enemies = set()
        character = pygame.image.load("asset/character.png").convert_alpha()
        self.direction = "down"
        self.frame = 0
        self.animation_timer = 0
        self.moving = False
        self.weapon = Weapon(
            "asset/animation_attack_stick.png",
            32,
            64,
            3,
            30
        )
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

    def update(self, enemies):
        self.move()
        self.animate()
        self.weapon.update()

        # controle de ataque
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attack_active = self.attack_duration
            self.attack_timer = self.attack_cooldown
            self.hit_enemies.clear()

        # ataque ativo: verifica se o ataque está ativo, se estiver ataca os inimigos 1x e o desativa. Evita varios hits no mesmo inimigo em um uníco ataque.
        if self.attack_active > 0:
            self.attack(enemies)
            self.attack_active -= 1

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

        # normaliza a velocidade diagonal
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
        arena_bottom = 1080

        if self.rect.left < arena_left:
            self.rect.left = arena_left
        if self.rect.right > arena_right:
            self.rect.right = arena_right
        if self.rect.top < arena_top:
            self.rect.top = arena_top
        if self.rect.bottom > arena_bottom:
            self.rect.bottom = arena_bottom

    def attack(self, enemies):
        sprite = self.weapon.rotate_sprite(self.direction)
        rect = sprite.get_rect()

        cx, cy = self.rect.center

        if self.direction == "right":
            rect.midleft = (cx, cy)

        elif self.direction == "left":
            rect.midright = (cx, cy)

        elif self.direction == "up":
            rect.midbottom = (cx, cy)

        elif self.direction == "down":
            rect.midtop = (cx, cy)

        self.last_attack_rect = rect  # debug

        for enemy in enemies:

            if enemy in self.hit_enemies:
                continue  # já tomou dano nesse ataque

            if rect.colliderect(enemy.rect):
                enemy.takeDamage(self.damage)
                self.hit_enemies.add(enemy)
    def takeDamage(self, damage):
        self.health -= damage
        #print("Player HP:", self.health)
        if self.health <= 0:
            print("Player morreu")

    def draw(self, window, camera_y):
        sprite = self.animations[self.direction][self.frame]
        window.blit(sprite, (self.rect.x, self.rect.y - camera_y))
        self.weapon.draw(window, self, camera_y)