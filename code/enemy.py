#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

import pygame

from code.animator import Animator
from code.entity import Entity
from const import ENEMY_SPRITE_POS_W, ENEMY_SPRITE_POS_H, SPRITE_SCALE, ENEMY_FRAME_COUNT

#Classe Enemy que herda de Entity
class Enemy(Entity):
    #Tipos de inimigos disponíveis e seus stats
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
    #Construtor do inimigos
    def __init__(self, enemy_type, pos):
        stat = self.type[enemy_type]    #Obtém stats do tipo
        super().__init__(enemy_type, None, pos)
        self.health = stat["health"]    #Vida
        self.speed = stat["speed"]      #Velocidade
        self.damage = stat["damage"]    #Dano
        self.is_dead = False            #Flag para saber se está morto
        #Controle de ataque
        self.attack_cooldown = 60       #Frames entre ataques
        self.attack_timer = 0           #Contador de cooldown
        #Animador dos inimigos
        self.animator = Animator(
            stat["sprite"],
            ENEMY_SPRITE_POS_W,
            ENEMY_SPRITE_POS_H,
            ENEMY_FRAME_COUNT,
            SPRITE_SCALE
        )
    #Atualiza o inimigo a cada frame
    def update(self, player):
        self.chase(player)      #Segue o jogador
        self.animator.update()  #Atualiza animação
        self.attack(player)     #Verifica ataque
    #Função de animação (controla os frames manualmente)
    def animate(self):
        self.animator.update(20)
        self.sprite = self.animator.get_frame(0)
    #Segue o jogador
    def chase(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            dx /= distance
            dy /= distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
    #Recebe dano
    def takeDamage(self, damage):
        self.health -= damage
        print("enemy:", self.health)
        if self.health <= 0:
            self.is_dead = True #Marca como morto
    #Ataca o jogador ao colidir
    def attack(self, player):
        if self.rect.colliderect(player.rect):
            if self.attack_timer <= 0:
                player.takeDamage(self.damage)
                self.attack_timer = self.attack_cooldown    #Reinicia o cooldown
        if self.attack_timer > 0:
            self.attack_timer -= 1  #Reduz timer a cada frame
    #Desenha o inimigo na tela
    def draw(self, window, camera_y):
        sprite = self.animator.get_frame()
        window.blit(sprite, (self.rect.x, self.rect.y - camera_y))

