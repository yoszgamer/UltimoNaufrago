#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from code import player, enemySpawner
from code.HUD import HUD
from code.enemySpawner import EnemySpawner
from code.fishingGame import FishingGame
from code.menu import Menu
from code.player import Player
from code.sfxManager import SFXManager
from const import WIN_WIDTH, WIN_HEIGHT, STATE_MENU, STATE_GAME, STATE_FISHING, STATE_GAME_OVER, UI_SCALE
from code.enemy import Enemy

#Classe principal que controla oa lógica do jogo
class Game:
    def __init__(self):
        pygame.init()
        #Gerenciador de sons
        self.sound = SFXManager()
        #Cria a janela do jogo
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        #Carrega a imagem de fundo
        self.background = pygame.image.load("asset/background.png").convert()
        #Estado inicial do jogo (menu)
        self.state = STATE_MENU
        #Variáveis da câmera (para movimentação da tela verticalmente)
        self.camera_y = 0
        self.target_camera_y = 0
        #instâncições de classes
        self.menu = Menu(self.window)
        self.fishingGame = FishingGame()
        self.player = Player(None, (480, 720))
        self.hud = HUD()
        self.fps = pygame.time.Clock()  #Controla o fps
        #Gerenciador de inimigos
        self.spawner = EnemySpawner()
        #Lista inicial de inimigos
        self.enemies = [
            Enemy("crab", (400, 1060)),
            Enemy("snake", (600, 400))
        ]
        #Game over
        self.gameOverTimer = 0
        self.gameOverDuration = 120
        self.gameOverImg = pygame.image.load("asset/UI_fishingFail.png").convert_alpha()    #Imagem usada no gameover
    #Loop principal do jogo
    def run(self):
        while True:
            #Processa eventos do pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #Verifica o clique no botão "novo jogo" no menu
                if self.state == STATE_MENU:
                    if self.menu.checkStartClick(event):
                        self.changeState(STATE_GAME)
                #Verifica o clique para skillcheck no minigame de pesca
                if self.state == STATE_FISHING:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.fishingGame.checkInput(event.pos)

            self.fps.tick(60)   #Limita o jogo a 60 FPS
            self.update()   #Atualiza lógica do jogo
            self.draw() #Desenha os elementos na tela
    #Atualiza o estado do jogo a cada frame
    def update(self):
        self.moveCamera()
        #GAME- Estado principal do jogo
        if self.state == STATE_GAME:
            #se jogador morrer = gameover
            if self.player.health <= 0:
                self.state = STATE_GAME_OVER
                self.sound.play("gameover")
                self.gameOverTimer = self.gameOverDuration
                return
            #Atualiza jogador
            self.player.update(self.enemies)
            #Remove inimigos mortos
            self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead]
            #Atualiza inimigos restantes
            for enemy in self.enemies:
                enemy.update(self.player)
            #Atualiza gerador de inimigos
            self.spawner.update(self.enemies, self.player)
            #se Wave atual acabar inicia minigame de pesca
            if self.spawner.isWaveFinished(self.enemies):
                self.changeState(STATE_FISHING)
                self.fishingGame.start(self.player)
        #Game Over
        elif self.state == STATE_GAME_OVER:
            self.gameOverTimer -= 1
            if self.gameOverTimer <= 0:
                self.reset_game()
                self.state = STATE_MENU
        #Mini game
        elif self.state == STATE_FISHING:
            self.fishingGame.update()
            #Quando minigame terminar, inicia nova wave
            if self.fishingGame.is_finished():
                self.spawner.startWave()
                self.enemies.clear()
                self.changeState(STATE_GAME)
    #Desenha a tela do gameover
    def draw_game_over(self, window):
        img = pygame.transform.scale(
            self.gameOverImg,
            (
                int(self.gameOverImg.get_width() * UI_SCALE),
                int(self.gameOverImg.get_height() * UI_SCALE)
            )
        )
        x = (window.get_width() - img.get_width()) // 2
        y = (window.get_height() - img.get_height()) // 2
        window.blit(img, (x, y))
    #Desenha todos os elementos do jogo dependendo do estado
    def draw(self):
        #Fundo
        self.window.blit(self.background, (0, -self.camera_y))
        if self.state == STATE_MENU:
            self.menu.draw()
        if self.state == STATE_GAME:
            #Desenha inimigos
            for enemy in self.enemies:
                enemy.draw(self.window, self.camera_y)
            #Desenha jogador
            self.player.draw(self.window, self.camera_y)
            #Desenha HUD
            self.hud.draw(self.window, self.player, self.spawner)
        if self.state == STATE_FISHING:
            #Desenha minigame
            self.fishingGame.draw(self.window)
        elif self.state == STATE_GAME_OVER:
            self.draw_game_over(self.window)
        pygame.display.flip()
    #Altera o estado de jogo e ajusta a posição da câmera
    def changeState(self, new_state):
        self.state = new_state
        if new_state == STATE_MENU:
            self.target_camera_y = 0
        elif new_state == STATE_GAME:
            self.target_camera_y = 540
        elif new_state == STATE_FISHING:
            self.target_camera_y = 960

    #move a câmera suavemente até o alvo
    def moveCamera(self):
        speed = 12
        if self.camera_y < self.target_camera_y:
            self.camera_y += speed
            if self.camera_y > self.target_camera_y:
                self.camera_y = self.target_camera_y
        elif self.camera_y > self.target_camera_y:
            self.camera_y -= speed
            if self.camera_y < self.target_camera_y:
                self.camera_y = self.target_camera_y
    #Reseta o jogo para reiniciar após o gameover
    def reset_game(self):
        self.player = Player(None, (480, 720))
        self.spawner.reset()
        self.enemies = []
        self.camera_y = 0
        self.target_camera_y = 0