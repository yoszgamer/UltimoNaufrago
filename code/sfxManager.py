#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

#Classe que gerencia todos os efeitos sonoros (SFX) e música do jogo
class SFXManager:
    def __init__(self):
        #Incia o mixer do pygame
        pygame.mixer.init()
        #Música de fundo
        pygame.mixer.music.load("asset/SFX_bgm.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        #Carrega outros SFX do jogo em um dicionário
        self.sounds = {
            "attack": pygame.mixer.Sound("asset/SFX_attack.wav"),
            "success": pygame.mixer.Sound("asset/SFX_catch_success.wav"),
            "fail": pygame.mixer.Sound("asset/SFX_catch_fail.wav"),
            "gameover": pygame.mixer.Sound("asset/SFX_gameover.wav"),
        }
        #Define o volume individual de cada SFX
        self.volumes = {
            "attack": 0.2,
            "success": 0.6,
            "fail": 0.6,
            "gameover": 0.6,
        }
        #Aplica os respectivos volumes
        for name, sound in self.sounds.items():
            sound.set_volume(self.volumes.get(name, 1.0))
    #Função para reproduzir o SFX pelo nome
    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
