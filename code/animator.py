#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

#Classe responsável por gerencia animações de sprites
class Animator:
    #Construtor de classe
    def __init__(self, sheet_path, frame_w, frame_h, frames, scale):
        #sheet_path (caminho do spritesheet)
        #frame_w (largura de cada frame)
        #frame_h (altura de cada frame)
        #frames (número total de frames na animação)
        #scale (fator de escala para aumentar/diminuir tamanho do sprite)
        self.sheet = pygame.image.load(sheet_path).convert_alpha()  #Carrega o spritesheet
        self.frames = []    #Lista que vai armazenar cada frame separado
        self.frame = 0      #Frame atual
        self.timer = 0      #Contador interno para controlar a velocidade da animação
        #Extrai cada frame do spritesheet
        for i in range(frames):
            rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)    #Retângulo de recorte do frame
            sprite = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)    #Cria surface transparente
            sprite.blit(self.sheet, (0,0), rect)    #Copia o frame do sheet
            sprite = pygame.transform.scale(sprite,(frame_w * scale, frame_h * scale))  #Aplica escala
            self.frames.append(sprite)  #Adiciona à lista de frames
#Atualiza o frame de animação
    def update(self, speed=20):
        #Speed (número de frams do jogo entre a troca de frames da animação
        self.timer += 1
        if self.timer >= speed:
            self.timer = 0
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0  #Loop da animação
    #Retorna o frame atual para ser desenhado
    def get_frame(self):
        return self.frames[self.frame]