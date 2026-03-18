#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from const import FISHING_SCALE

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont(None, int(10 * FISHING_SCALE))

        self.icon_hp = pygame.image.load("asset/icon_hpPlus.png").convert_alpha()
        self.icon_damage = pygame.image.load("asset/icon_strenghtPlus.png").convert_alpha()
        self.icon_speed = pygame.image.load("asset/icon_speedPlus.png").convert_alpha()

        self.icon_size = int(10 * FISHING_SCALE)

    def draw(self, window, player, spawner):
        self.draw_stats(window, player)
        self.draw_wave(window, spawner.wave)

    def draw_stats(self, window, player):
        x = 20
        y = 20
        spacing = int(15 * FISHING_SCALE)

        stats = [
            ("HP", player.health, self.icon_hp),
            ("DANO", self.get_damage_text(player), self.icon_damage),
            ("VEL.", round(player.speed, 1), self.icon_speed),
        ]

        for i, (label, value, icon) in enumerate(stats):
            icon_scaled = pygame.transform.scale(icon, (self.icon_size, self.icon_size))

            icon_y = y + i * spacing

            # ícone
            window.blit(icon_scaled, (x, icon_y))

            # texto
            text = self.font.render(f"{label}: {value}", True, (255, 255, 255))
            window.blit(text, (x + self.icon_size + 10, icon_y))

    def get_damage_text(self, player):
        return int(player.base_damage * player.damage_multiplier)

    def draw_wave(self, window, wave):
        text = self.font.render(f"WAVE {wave}", True, (255, 255, 255))

        x = (window.get_width() - text.get_width()) // 2
        y = 10

        window.blit(text, (x, y))