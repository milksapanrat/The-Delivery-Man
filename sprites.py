import pygame
from config import *
from data import *
import math

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height]) #สร้าง surface เปล่าสำหรับ sprite
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "left"
        self.animation_loop = 1
        self.image = self.game.character_spritesheet.get_sprite(
            0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    #movement
    def movement(self):
        if not self.game.show_dialog and not self.game.cutscene_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.x_change -= PLAYER_SPEED
                self.facing = 'left'
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.x_change += PLAYER_SPEED
                self.facing = 'right'
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.y_change += PLAYER_SPEED
                self.facing = 'down'
    
    #update
    def update(self):
        self.x_change = 0
        self.y_change = 0

        self.movement()

        # ขยับแกน X
        self.rect.x += self.x_change
        self.collide_blocks('x')

        # ขยับแกน Y
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.animate()

    def collide_blocks(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            if direction == 'x':
                if self.x_change > 0: self.rect.right = hits[0].rect.left
                if self.x_change < 0: self.rect.left = hits[0].rect.right
            if direction == 'y':
                if self.y_change > 0: self.rect.bottom = hits[0].rect.top
                if self.y_change < 0: self.rect.top = hits[0].rect.bottom

    def animate(self):
        left_animations = [self.game.character_spritesheet.get_sprite(35, 107, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 38, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(38, 38, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(2, 107, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(74, 2, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(110, 2, self.width, self.height)]
        
        down_animations = [self.game.character_spritesheet.get_sprite(38, 74, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(2, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(74, 38, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(2, 74, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(111, 38, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(38, 2, self.width, self.height)]
        
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(38, 74, self.width, self.height)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 72, self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(33, 105, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(0, 105, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, groups, layer):
        self.game = game
        self._layer = layer
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 0))  # โปร่งใสเต็มที่
        self.rect = self.image.get_rect(topleft=(x * TILESIZE, y * TILESIZE))

class Blocked_Block(Block):
    def __init__(self, game, x, y):
        groups = (game.all_sprites, game.blocks)
        super().__init__(game, x, y, groups, BLOCKEDBLOCK_LAYER)
        # self.image.fill((0, 0, 255, 100))

class interact_blocks(Block):
    def __init__(self, game, x, y, cutscene_key=None):
        self.cutscene_key = cutscene_key
        groups = (game.all_sprites, game.interact_block)
        super().__init__(game, x, y, groups, INTERACTABLE_LAYER)
        # self.image.fill((255, 0, 0, 100))

class Dialog_Block(Block):
    def __init__(self, game, x, y, dialog_id):
        groups = (game.all_sprites, game.dialog_block)
        super().__init__(game, x, y, groups, DIABLOCK_LAYER)
        # self.image.fill((0, 255, 0, 100))
        self.dialog_id = dialog_id

class ChangeMap_Block(Block):
    def __init__(self, game, x, y, exit_type):
        groups = (game.all_sprites, game.changemap_block)
        super().__init__(game, x, y, groups, CHANGEMAP_LAYER)
        self.exit_type = exit_type
        # self.image.fill((0, 255, 0, 100))

    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            if not self.game.scene_changing and self.game.map_cooldown == 0:
                self.game.change_requested = True
                self.game.target_exit = self.exit_type
                self.game.map_cooldown = 30
                print("HIT CHANGE MAP", self.exit_type)



class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('TA 8 bit.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if self.bg is not None:
            self.image.fill(self.bg)

        if self.content != "" and self.fg is not None:
            text = self.font.render(self.content, True, self.fg)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.image.blit(text, text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
    

    
