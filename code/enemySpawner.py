#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from code.enemy import Enemy

#Classe responsável por gerenciar o spawn de inimigos e as waves
class EnemySpawner:
    def __init__(self):
        self.wave = 1           #Número da wave atual
        self.spawn_timer = 0    #Timer interno para o delay de spawn
        self.spawn_delay = 120  #Frames entre spawn de inimigos
        self.spawnRate = 3      #Quantidade de inimigos que serão spawnados na wave
        self.spawned = 0        #Contador de inimigos já spawnados
        self.enemy_pool = ["crab", "snake"] #Tipos de inimigos disponíveis
    #Atualiza o spawner a cada frame
    def update(self, enemies, player):
        #Se já spawnou todos os inimigos da wave, não faz nada
        if self.spawned >= self.spawnRate:
            return
        self.spawn_timer += 1
        #Quando o timer chega ao delay, spawna um novo inimigo
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            enemy = self.spawn(player)
            enemies.append(enemy)
            self.spawned += 1
    #Função que cria um inimigo próximo ao jogador (fora da tela)
    def spawn(self, player):
        spawn_distance = 400    #Distância mínima do jogador
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.randint(0, 960)
            y = player.rect.y - spawn_distance
        elif side == "bottom":
            x = random.randint(0, 960)
            y = player.rect.y + spawn_distance
        elif side == "left":
            x = player.rect.x - spawn_distance
            y = random.randint(540, 960)
        else:
            x = player.rect.x + spawn_distance
            y = random.randint(540, 960)
        #Escolhe o tipo de inimigo aleatório
        enemy_type = random.choice(self.enemy_pool)
        enemy = Enemy(enemy_type, (x, y))
        self.enemy_scaling(enemy)   #Escala stats de acordo com a wave
        return enemy
    #Ajusta stats do inimigo com base na wave atual
    def enemy_scaling(self, enemy):
        enemy.health += self.wave * 4
        enemy.damage += self.wave * 2
        enemy.speed += self.wave * 0.1
    #Começa uma nova wave
    def startWave(self):
        self.wave += 1
        self.spawned = 0
        self.spawn_timer = 0
        self.spawnRate = 3 + self.wave * 2  #Aumenta o número de inimigos por wave
        self.spawn_delay = max(30, 120 - self.wave * 5) #Reduz delay entre spawns até um mínimo
    #Retorna True se todos os inimigos da wave morreram e não há mais nenhum para spawnar
    def isWaveFinished(self, enemies):
        return self.spawned >= self.spawnRate and len(enemies) == 0
    #Reseta spawner para o início do jogo
    def reset(self):
        self.wave = 1
        self.spawned = 0
        self.spawnRate = 3
        self.spawn_timer = 0
