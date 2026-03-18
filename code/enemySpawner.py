#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from code.enemy import Enemy


class EnemySpawner:
    def __init__(self):
        self.wave = 1
        self.spawn_timer = 0
        self.spawn_delay = 120
        self.spawnRate = 3
        self.spawned = 0
        self.enemy_pool = ["crab", "snake"]

    def update(self, enemies, player):
        if self.spawned >= self.spawnRate:
            return
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            enemy = self.spawn(player)
            enemies.append(enemy)
            self.spawned += 1

    def spawn(self, player):
        spawn_distance = 400
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
        enemy_type = random.choice(self.enemy_pool)
        enemy = Enemy(enemy_type, (x, y))
        self.enemy_scaling(enemy)
        return enemy

    def enemy_scaling(self, enemy):
        enemy.health += self.wave * 5
        enemy.damage += self.wave * 2
        enemy.speed += self.wave * 0.1

    def startWave(self):
        self.wave += 1
        self.spawned = 0
        self.spawn_timer = 0
        self.spawnRate = 3 + self.wave * 2
        self.spawn_delay = max(30, 120 - self.wave * 5)


    def isWaveFinished(self, enemies):
        return self.spawned >= self.spawnRate and len(enemies) == 0
