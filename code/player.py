#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code.entity import Entity
from code.sfxManager import SFXManager
from code.weapon import Weapon
from const import SPRITE_POS_W, SPRITE_POS_H, SPRITE_SCALE

#Função para extrair sprites de uma sprite sheet
def get_sprite(sheet, col, row):
    rect = pygame.Rect(col * SPRITE_POS_W, row * SPRITE_POS_H, SPRITE_POS_W, SPRITE_POS_H)
    playersprite = pygame.Surface((SPRITE_POS_W, SPRITE_POS_H), pygame.SRCALPHA)
    playersprite.blit(sheet, (0, 0), rect)
    playersprite = pygame.transform.scale(playersprite,(SPRITE_POS_W * SPRITE_SCALE, SPRITE_POS_H * SPRITE_SCALE))
    return playersprite

#Classe do jogador, herda Entity
class Player(Entity):
    def __init__(self, sprite, pos):
        super().__init__('Player', sprite, pos)
        #Gerenciador de sons
        self.sound = SFXManager()
        #Stats básicos
        self.base_damage = 50
        self.damage_multiplier = 1
        self.stats = {"damage": 0}
        self.health = 100
        self.speed = 4
        #controle de ataque
        self.attack_cooldown = 25   #Frames entre ataques
        self.attack_timer = 0       #Contador para cooldown
        self.attack_duration = 8    #Duração de cada ataque
        self.attack_active = 0      #Se ataque está ativo
        self.hit_enemies = set()    #Evita atacar inimigos múltiplas vezes por ataque
        #Carrega o sprite sheet do jogador
        character = pygame.image.load("asset/character.png").convert_alpha()
        self.direction = "down"
        self.frame = 0
        self.animation_timer = 0
        self.moving = False
        #Cria arma do jogador
        self.weapon = Weapon(
            "asset/animation_attack_stick.png",
            32,
            64,
            3,
            30
        )
        #Configura as animações de movimento
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
        #animação da esquerda é a versão espelhada da direita
        self.animations["left"] = [
            pygame.transform.flip(frame, True, False)
            for frame in self.animations["right"]
        ]
        #Ajusta o tamanho do retângulo de colisão do jogador
        self.rect.width = SPRITE_POS_W * SPRITE_SCALE
        self.rect.height = SPRITE_POS_H * SPRITE_SCALE
    #Atualiza o jogador a cada frame
    def update(self, enemies):
        self.move()         #Movimentação
        self.animate()      #Animação
        self.weapon.update()#Arma

        # controle do cooldown do ataque
        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attack_active = self.attack_duration
            self.attack_timer = self.attack_cooldown
            self.hit_enemies.clear()
        #Ataque ativo (verifica colisão com inimigos)
        if self.attack_active > 0:
            self.attack(enemies)
            self.attack_active -= 1
    #Atualiza animação do jogador
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
    #Movimentação com as teclas "WASD"
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
        #Normaliza a velocidade diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        #Aplicar movimento
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        #Limites da arena
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
    #Ataque (cria retângulo da arma e verifica colisão com inimigos)
    def attack(self, enemies):
        self.sound.play("attack")
        sprite = self.weapon.rotate_sprite(self.direction)
        rect = sprite.get_rect()
        cx, cy = self.rect.center
        #Posiciona este retângulo de acordo com a direção do jogador
        if self.direction == "right":
            rect.midleft = (cx, cy)

        elif self.direction == "left":
            rect.midright = (cx, cy)

        elif self.direction == "up":
            rect.midbottom = (cx, cy)

        elif self.direction == "down":
            rect.midtop = (cx, cy)
        #Verifica colisão com inimigos
        for enemy in enemies:
            if enemy in self.hit_enemies:
                continue  # já foi atingido nesse ataque
            if rect.colliderect(enemy.rect):
                enemy.takeDamage(self.get_damage())
                self.hit_enemies.add(enemy)
    #Recebe dano do inimigo
    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            pass
    #Calcula o dano total
    def get_damage(self):
        return int(self.base_damage * self.damage_multiplier)
    #Desenha o jogador na tela
    def draw(self, window, camera_y):
        sprite = self.animations[self.direction][self.frame]
        window.blit(sprite, (self.rect.x, self.rect.y - camera_y))
        self.weapon.draw(window, self, camera_y)