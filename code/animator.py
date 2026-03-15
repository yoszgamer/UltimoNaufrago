#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame


class Animator:

    def __init__(self, sheet_path, frame_w, frame_h, frames, scale):

        self.sheet = pygame.image.load(sheet_path).convert_alpha()

        self.frames = []
        self.frame = 0
        self.timer = 0

        for i in range(frames):

            rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)

            sprite = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
            sprite.blit(self.sheet, (0,0), rect)

            sprite = pygame.transform.scale(
                sprite,
                (frame_w * scale, frame_h * scale)
            )

            self.frames.append(sprite)

    def update(self, speed=20):
        self.timer += 1
        if self.timer >= speed:
            self.timer = 0
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0

    def get_frame(self):
        return self.frames[self.frame]