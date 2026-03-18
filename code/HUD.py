#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from const import UI_SCALE, COLOR_BLUE


#Classe que exibe a HUD do jogador
class HUD:
    def __init__(self):
        #Fonte usada para os textos da HUD, escalada pela constante UI_SCALE
        self.font = pygame.font.SysFont(None, int(10 * UI_SCALE))
        #Carrega fundo para os textos dos stats
        self.stat_bg = pygame.image.load("asset/UI_iconBG.png").convert_alpha()
        self.stat_bg = pygame.transform.scale(self.stat_bg, (160, 50))  #Ajuste conforme tamanho do texto
        #Carrega fundo para o texto da wave
        self.wave_bg = pygame.image.load("asset/UI_waveBG.png").convert_alpha()
        self.wave_bg = pygame.transform.scale(self.wave_bg, (120, 40))  #Ajuste conforme tamanho do texto
        #Carrega ícones para stats
        self.icon_hp = pygame.image.load("asset/icon_hpPlus.png").convert_alpha()
        self.icon_damage = pygame.image.load("asset/icon_strenghtPlus.png").convert_alpha()
        self.icon_speed = pygame.image.load("asset/icon_speedPlus.png").convert_alpha()
        #Tamanho dos icones escalado
        self.icon_size = int(10 * UI_SCALE)
    #Função principal que desenha toda a HUD
    def draw(self, window, player, spawner):
        self.draw_stats(window, player) #Desenha os stats do jogador
        self.draw_wave(window, spawner.wave)    #Desenha o número da wave atual
    #Desenha os stats do jogador (HP, Dano, Velocidade
    def draw_stats(self, window, player):
        x = 20  #Posição horizontal base
        y = 25  #Posição Vertical base
        spacing = int(15 * UI_SCALE)    #Espaçamento entre eles
        #Lista de stats com label, valor e ícone
        stats = [
            ("HP", player.health, self.icon_hp),
            ("DANO", self.get_damage_text(player), self.icon_damage),
            ("VEL.", round(player.speed, 1), self.icon_speed),
        ]
        #Desenha cada stat
        for i, (label, value, icon) in enumerate(stats):
            icon_scaled = pygame.transform.scale(icon, (self.icon_size, self.icon_size))
            icon_y = y + i * spacing
            #Texto
            text = self.font.render(f"{label}: {value}", True, (COLOR_BLUE))
            #Retâgulo total (icone + espaçamento + texto)
            total_width = self.icon_size + 10 + text.get_width()
            total_height = max(self.icon_size, text.get_height())
            block_rect = pygame.Rect(x, icon_y, total_width, total_height)
            #Fundo centralizado no bloco
            bg_rect = self.stat_bg.get_rect(center=block_rect.center)
            window.blit(self.stat_bg, bg_rect.topleft)
            #Ícone e texto
            window.blit(icon_scaled, (x, icon_y))
            window.blit(text, (x + self.icon_size + 10, icon_y + 8))
    #Calcula o dano do jogador levando em conta o multiplicador de dano
    def get_damage_text(self, player):
        return int(player.base_damage * player.damage_multiplier)
    #Desenha o número da wave centralizado no topo da tela
    def draw_wave(self, window, wave):
        text = self.font.render(f"WAVE {wave}", True, (COLOR_BLUE))
        x = (window.get_width() - text.get_width()) // 2
        y = 10
        # fundo atrás do texto
        window.blit(self.wave_bg, (x - 23, y - 10))  # ajuste x e y para centralizar
        window.blit(text, (x, y))