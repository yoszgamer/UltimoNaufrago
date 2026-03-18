#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

#Classe base para qualquer entidade do jogo
class Entity:
    def __init__(self, name, sprite, pos):
        #name (nome)
        #sprite (imagem da entidade)
        #pos (posição inicial)
        self.name = name
        self.sprite = sprite
        if sprite:
            #Se houver sprite, cria um retângulo com base na imagem, centralizado na posição
            self.rect = sprite.get_rect(center=pos)
        else:
            #Se não houver sprite, cria um retângulo genérico de 32x32 pixels
            self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
    #Desenha a entidade na tela considerando o deslocamento da câmera
    def draw(self, window, camera_y):
        if self.sprite:
            window.blit(self.sprite, (self.rect.x, self.rect.y - camera_y))
