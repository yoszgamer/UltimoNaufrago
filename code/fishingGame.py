#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import copy
import pygame

from const import FISHING_SCALE


def get_item_description(item):
    if item["type"] == "hp":
        return f"+{item['value']} HP"
    elif item["type"] == "damage":
        return f"+{item['value']} DANO"
    elif item["type"] == "speed":
        return f"+{item['value']} VEL."
    elif item["type"] == "mult":
        return f"x{item['value']} DANO"


class FishingGame:
    def __init__(self):
        self.reward_upgrade = None
        self.reward_given = False
        self.sprite = pygame.image.load("asset/UI_fishingScreen.png").convert_alpha()
        self.frame_width = 256
        self.frame_height = 128
        self.set_state(0)
        self.current_frame = 0  # 0 = upgrade, 1 = skill check
        self.markerPos = None
        self.succesZone = None
        self.speed = None
        self.active = False
        self.panel_surface = self.get_frame(0)
        self.mode = None
        self.icon_positions = [
            (119, 72),
            (157, 72),
            (195, 72)
        ]
        self.font = pygame.font.SysFont(None, int(9 * FISHING_SCALE))
        self.items = [
            {
                "name": "HP+",
                "type": "hp",
                "value": 20,
                "icon": pygame.image.load("asset/icon_hpPlus.png").convert_alpha(),
                "rarity": "common",
                "difficulty": 1.0
            },
            {
                "name": "DANO+",
                "type": "damage",
                "value": 5,
                "icon": pygame.image.load("asset/icon_strenghtPlus.png").convert_alpha(),
                "rarity": "common",
                "difficulty": 1.2
            },
            {
                "name": "VELOCIDADE+",
                "type": "speed",
                "value": 1,
                "icon": pygame.image.load("asset/icon_speedPlus.png").convert_alpha(),
                "rarity": "common",
                "difficulty": 1.1
            },
            {
                "name": "LANÇA DE PEDRA",
                "type": "mult",
                "value": 3,
                "icon": pygame.image.load("asset/icon_weapon_stonelance.png").convert_alpha(),
                "rarity": "legendary",
                "difficulty": 2.0
            }
        ]
        self.legendary_taken = False
        self.current_choices = []

        self.cursor_y = 0
        self.cursor_speed = 4
        self.cursor_dir = 1

        self.target_y = 0
        self.target_height = 40

        self.skill_active = False
        self.success = False
        self.finished = False

        self.success_img = pygame.image.load("asset/UI_fishingSucess.png").convert_alpha()
        self.fail_img = pygame.image.load("asset/UI_fishingFail.png").convert_alpha()

        self.result_timer = 0
        self.show_result = False

    def generate_choices(self):
        commons = [i for i in self.items if i["rarity"] == "common"]
        if self.legendary_taken:
            self.current_choices = random.sample(commons, 3)
            return
        self.current_choices = random.sample(commons, 3)
        if random.random() < 0.35:
            legendary = next(i for i in self.items if i["rarity"] == "legendary")
            index = random.randint(0, 2)
            self.current_choices[index] = legendary

    def handle_upgrade_click(self, mouse_pos):
        panel_w = self.panel_surface.get_width()
        x = (960 - panel_w) // 2
        y = 50
        icon_size = int(32 * FISHING_SCALE)
        for i, item in enumerate(self.current_choices):
            base_x, base_y = self.icon_positions[i]
            icon_x = x + int(base_x * FISHING_SCALE)
            icon_y = y + int(base_y * FISHING_SCALE)
            rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
            if rect.collidepoint(mouse_pos):
                self.reward_upgrade = {
                    "type": item["type"],
                    "value": item["value"],
                    "rarity": item["rarity"],
                    "difficulty": item["difficulty"]
                }
                if item["rarity"] == "legendary":
                    self.legendary_taken = True
                print("ESCOLHIDO:", item["type"])
                self.start_skillcheck()
                break

    def handle_skill_click(self):
        if not self.skill_active or self.finished:
            return
        if self.target_y <= self.cursor_y <= self.target_y + self.target_height:
            self.success = True
        else:
            self.success = False
        self.skill_active = False
        self.show_result = True
        self.result_timer = 120

    def start(self, player):
        self.player = player
        self.active = True
        self.mode = "upgrade"
        self.set_state(0)
        self.finished = False
        self.show_result = False
        self.generate_choices()
        self.reward_upgrade = None

    def update(self):
        if not self.active:
            return
        if self.mode == "skill" and self.skill_active:
            self.cursor_y += self.cursor_speed * self.cursor_dir
            if self.cursor_y >= self.bar_height:
                self.cursor_y = self.bar_height
                self.cursor_dir = -1
            elif self.cursor_y <= 0:
                self.cursor_y = 0
                self.cursor_dir = 1
        if self.show_result:
            self.result_timer -= 1
            if self.result_timer <= 0 and not self.reward_given:
                if self.success:
                    self.giveReward(self.player)
                self.reward_given = True
                self.finished = True

    def is_finished(self):
        return self.finished

    def checkInput(self, mouse_pos):
        if self.show_result:
            return
        if self.mode == "upgrade":
            self.handle_upgrade_click(mouse_pos)
        elif self.mode == "skill":
            self.handle_skill_click()

    def start_skillcheck(self):
        self.mode = "skill"
        self.set_state(1)

        difficulty = self.reward_upgrade["difficulty"]

        self.skill_active = True
        self.finished = False
        self.success = False

        self.bar_height = int(103 * FISHING_SCALE)

        self.cursor_y = 0
        self.cursor_speed = 3 * difficulty
        self.cursor_dir = 1

        self.target_height = int(30 / difficulty)
        self.target_y = random.randint(10, self.bar_height - self.target_height - 10)
        self.reward_given = False

    def giveReward(self, player):
        upgrade = self.reward_upgrade
        print("REWARD:", upgrade["type"])

        if upgrade["type"] == "hp":
            player.health += upgrade["value"]

        elif upgrade["type"] == "damage":
            player.stats["damage"] += 1
            player.base_damage += upgrade["value"] * player.stats["damage"]

        elif upgrade["type"] == "speed":
            player.speed += upgrade["value"]


        elif upgrade["type"] == "mult":
            if player.damage_multiplier == 1:
                player.damage_multiplier = upgrade["value"]

    def get_frame(self, index):
        rect = pygame.Rect(
            index * self.frame_width,
            0,
            self.frame_width,
            self.frame_height
        )
        surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        surface.blit(self.sprite, (0, 0), rect)
        scaled_surface = pygame.transform.scale(
            surface,
            (
                int(self.frame_width * FISHING_SCALE),
                int(self.frame_height * FISHING_SCALE)
            )
        )
        return scaled_surface

    def set_state(self, state):
        self.current_frame = state
        self.panel_surface = self.get_frame(state)

    def draw_icons(self, window, panel_x, panel_y, panel_w):
        for i, item in enumerate(self.current_choices):
            icon = item["icon"]
            icon_size = int(32 * FISHING_SCALE)
            icon = pygame.transform.scale(icon, (icon_size, icon_size))
            base_x, base_y = self.icon_positions[i]
            icon_x = panel_x + int(base_x * FISHING_SCALE)
            icon_y = panel_y + int(base_y * FISHING_SCALE)
            window.blit(icon, (icon_x, icon_y))
            text = get_item_description(item)
            text_surface = self.font.render(text, True, (255, 255, 255))
            text_x = icon_x + (icon_size - text_surface.get_width()) // 2
            text_y = icon_y + icon_size + 5
            window.blit(text_surface, (text_x, text_y))

    def draw_skillcheck(self, window, panel_x, panel_y):

        bar_x = panel_x + int(102 * FISHING_SCALE)
        bar_y = panel_y + int(13 * FISHING_SCALE)
        bar_width = int(4 * FISHING_SCALE)

        # barra fundo
        pygame.draw.rect(window, (80, 80, 80),
                         (bar_x, bar_y, bar_width, self.bar_height))

        # zona verde (alvo)
        pygame.draw.rect(window, (0, 255, 0),
                         (bar_x, bar_y + self.target_y,
                          bar_width, self.target_height))

        # cursor (linha)
        pygame.draw.rect(window, (255, 255, 255),
                         (bar_x - 2,
                          bar_y + int(self.cursor_y),
                          bar_width + 4,
                          3))

    def draw(self, window):
        screen_width = window.get_width()
        panel_w = self.panel_surface.get_width()
        x = (screen_width - panel_w) // 2
        y = 50
        window.blit(self.panel_surface, (x, y))
        if self.mode == "upgrade":
            self.draw_icons(window, x, y, panel_w)
        if self.mode == "skill":
            self.draw_skillcheck(window, x, y)
        if self.show_result:
            self.draw_result(window)

    def draw_result(self, window):
        img = self.success_img if self.success else self.fail_img
        img = pygame.transform.scale(
            img,
            (
                int(img.get_width() * FISHING_SCALE),
                int(img.get_height() * FISHING_SCALE)
            )
        )
        x = (window.get_width() - img.get_width()) // 2
        y = 150
        window.blit(img, (x, y))
