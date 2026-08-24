from pygame import *
import settings
from math import *


class HpBar(sprite.Sprite):
    def __init__(self, group, player, screen):
        super().__init__()
        self.add(group)
        self.w = 300
        
        self.player, self.screen = player, screen
        
        self.rect1 = Rect(120, 10, 300, 75)
        self.rect2 = Rect(120, 10, 300, 75)
    
    def update(self, *args):
        if self.w > (self.player.hp / settings.HP) * self.rect1.width:
            self.w -= self.Lerp(self.w, (self.player.hp / settings.HP), 0.05)
        elif self.w < (self.player.hp / settings.HP) * self.rect1.width:
            self.w += self.Lerp(self.w, (self.player.hp / settings.HP), 0.05)
        #self.w = (self.player.hp / settings.HP) * self.rect1.width
        self.rect2.width = self.w
        
        draw.rect(self.screen, (255, 255, 255), self.rect2)
        draw.rect(self.screen, (255, 255, 255), self.rect1, 2)
    
    def Lerp(self, cur, goal, lerp):
        return abs(cur - goal * self.rect1.width) * lerp

class WaveTime(sprite.Sprite):
    def __init__(self, group, player, screen, time):
        super().__init__()
        self.add(group)
        self.player, self.screen, self.time = player, screen, time
        self.fnt = font.SysFont('AC_line', 72)
        self.txt = self.fnt.render(f'{self.time}s left', True, (255, 255, 255))
        self.rect = self.txt.get_rect(bottomleft=(10, self.screen.get_height() - 10))
    
    def update(self, *args):
        self.time = args[1]
        self.txt = self.fnt.render(f'{self.time}s left', True, (255, 255, 255))
        self.rect = self.txt.get_rect(bottomleft=(10, self.screen.get_height() - 10))
        self.screen.blit(self.txt, self.rect)

class WaveCount(sprite.Sprite):
    def __init__(self, group, player, screen, count):
        super().__init__()
        self.add(group)
        self.player, self.screen, self.count= player, screen, count
        self.fnt = font.SysFont('AC_line', 72)
        self.txt = self.fnt.render(f'wave {self.count}', True, (255, 255, 255))
        self.rect = self.txt.get_rect(topright=(self.screen.get_width() - 10, 10))
    
    def update(self, *args):
        self.count = args[2]
        self.txt = self.fnt.render(f'wave {self.count}', True, (255, 255, 255))
        self.rect = self.txt.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(self.txt, self.rect)

class Hp_text(sprite.Sprite):
    def __init__(self, group, screen):
        super().__init__()
        self.add(group)
        self.screen = screen
        self.fnt = font.SysFont('AC_line', 64)
        self.txt = self.fnt.render('hp:', True, (255, 255, 255))
        self.rect = self.txt.get_rect(topleft=(10, 20))
    
    def update(self, *args):
        self.screen.blit(self.txt, self.rect)

class Loss_text(sprite.Sprite):
    def __init__(self, group, screen, wave):
        super().__init__()
        self.add(group)
        self.screen = screen
        self.wave = wave
        self.fnt = font.SysFont('AC_line', 64)
        self.lines = f'Game Over-Score: {wave}-Well done'.split('-')
    def update(self, *args):
        self.lines = f'Game Over-Score: {self.wave}-Well done'.split('-')
        for x in self.lines:
            self.txt = self.fnt.render(x, True, (255, 255, 255))
            self.rect = self.txt.get_rect(center=(640, 240 + 72 * self.lines.index(x)))
            self.screen.blit(self.txt, self.rect)


class KdUlt(sprite.Sprite):
    def __init__(self, group, player, screen, count):
        super().__init__()
        self.add(group)
        self.player, self.screen, self.count = player, screen, count
        self.fnt = font.SysFont('AC_line', 72)
        self.txt = self.fnt.render(f'{self.count}%', True, (255, 255, 255))
        self.rect = self.txt.get_rect(topright=(self.screen.get_width() - 10, 10))
    
    def update(self, *args):
        self.count = round(self.player.kills / args[3] * 100) if self.player.kills < args[3] else 100
        self.txt = self.fnt.render(f'Ult [R] {self.count}%', True, (255, 255, 255))
        self.rect = self.txt.get_rect(bottomright=(self.screen.get_width() - 15, self.screen.get_height() - 10))
        self.screen.blit(self.txt, self.rect)