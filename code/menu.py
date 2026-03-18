#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from const import COLOR_BLUE


#Classe que cria a tela inicial do jogo com o tutorial, logo e botão de "novo jogo"
class Menu:
    def __init__(self, window):
        self.window = window
        #Define retângulo do botão "novo jogo"
        self.start_button_rect = Rect(0,0,220,60)
        self.start_button_rect.center = (480,420)
        self.start_clicked = False  #flag para verificar o clique no botão
        #carrega imagens
            #Botão novo jogo
        self.start_button_sprite = pygame.image.load("asset/UI_playButton.png").convert_alpha() #Escala exatamente para o tamanho do rect
        self.start_button_sprite = pygame.transform.scale(self.start_button_sprite,(self.start_button_rect.width, self.start_button_rect.height))
            #Logo
        self.logo = pygame.image.load("asset/UI_gamelogo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (200, 100))
            #Tutorial
        self.icon_wasd = pygame.image.load("asset/UI_Tutorial_WASD.png").convert_alpha()
        self.icon_wasd = pygame.transform.scale(self.icon_wasd, (74, 50))
    #loop principal da tela de menu
    def run(self):
        while True:
            #Processa continuamente o eventos do pygame
            for event in pygame.event.get():
                self.checkStartClick(event) #Verifica o clique no botão
            self.draw() #desenha o menu na tela
    #Função que desenha todos os elementos do menu
    def draw(self, ):
        #Define a posição da logo e icone "WASD"
        logo_x = (self.window.get_width() - self.logo.get_width()) // 2
        logo_y = 55
        icon_x = 340
        icon_y = 210
        #Desenha icone "WASD" e logo
        self.window.blit(self.icon_wasd, (icon_x, icon_y))
        self.window.blit(self.logo, (logo_x, logo_y))
        #Utiliza a função menu_text para renderizar textos na tela
        self.menu_text(
            text_size=28,
            text="MOVIMENTAÇÃO",
            text_color=(COLOR_BLUE),
            text_center_pos=(500, 230)
        )
        self.menu_text(
            text_size=28,
            text="Sobreviva às hordas de animais o maxímo que conseguir",
            text_color=(COLOR_BLUE),
            text_center_pos=(480, 280)
        )
        #Renderiza o botão "novo jogo" (rentângulo e texto)
        self.window.blit(self.start_button_sprite, self.start_button_rect.topleft)
        self.menu_text(
            text_size=32,
            text="NOVA PARTIDA",
            text_color=(COLOR_BLUE),
            text_center_pos=self.start_button_rect.center
        )
        #Atualiza a tela
        pygame.display.flip()
    #Verifica se o botão "novo jogo" foi clicado
    def checkStartClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   #clique esquerdo do mouse
                if self.start_button_rect.collidepoint(event.pos):
                    return True #Botão clicado
        return False    #Clique fora do botão
    #Função para criar textos disponibilizada durante a aula
    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)