import pygame

from const import SPRITE_SCALE


class Weapon:
    def __init__(self, sprite_path, frame_w, frame_h, frames, attack_range):
        #sprite_path (caminho do spritesheet da arma)
        #frame_w, frame_h (largura e altura de cada frame)
        #frames (quantidade de frames na animação)
        #attack_range (alcance do ataque da arma)
        sheet = pygame.image.load(sprite_path).convert_alpha()  #Carrega o spritesheet
        self.frames = []        #Lista com frames individuais
        self.frame = 0          #Frame atual
        self.timer = 0          #Timer interno para controlar animação
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.attack_range = attack_range
        #Ponto pivô para rotações e transformações
        self.pivot = ((frame_w * SPRITE_SCALE) // 2,(frame_h * SPRITE_SCALE) // 2)
        #Extrai cada frame do spritesheet e aplica escala
        for i in range(frames):
            rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), rect)
            frame = pygame.transform.scale(frame,(frame_w * SPRITE_SCALE, frame_h * SPRITE_SCALE))
            self.frames.append(frame)
    #Atualiza a animação da arama
    def update(self):
        self.timer += 1
        if self.timer > 5:
            self.timer = 0
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0
    #Rotaciona ou espelha o sprite dependendo da direção do jogador
    def rotate_sprite(self, direction):
        sprite = self.frames[self.frame]
        if direction == "right":
            return sprite
        if direction == "down":
            return pygame.transform.rotate(sprite, -90)
        if direction == "left":
            return pygame.transform.flip(sprite, True, False)
        if direction == "up":
            return pygame.transform.rotate(sprite, 90)
    #Desenha a arma na tela em relação ao jogador e à câmera
    def draw(self, window, player, camera_y):
        sprite = self.rotate_sprite(player.direction)
        rect = sprite.get_rect()
        cx, cy = player.rect.center
        #Posiciona a arma com base na direção do jogador
        if player.direction == "right":
            rect.midleft = (cx, cy)
        elif player.direction == "left":
            rect.midright = (cx, cy)
        elif player.direction == "up":
            rect.midbottom = (cx, cy)
        elif player.direction == "down":
            rect.midtop = (cx, cy)
        window.blit(sprite, (rect.x, rect.y - camera_y))