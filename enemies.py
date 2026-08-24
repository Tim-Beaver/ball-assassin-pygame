from pygame import *
from math import *
import settings
import random



class EnemyCube(sprite.Sprite):
    def __init__(self, group, scr, speed, player, pos, hp, dmg, sounds, image, glow):
        super().__init__()
        self.add(group)
        self.image = image
        self.origimage = self.image
        self.rect = self.image.get_rect(center=pos)
        self.rect2 = self.image.get_rect(center=pos)
        self.screen, self.player, self.speed, self.hp, self.damage = scr, player, speed, hp, dmg
        self.k = 0
        self.koeff = random.choice([-1, 1])
        self.pos = math.Vector2(self.rect.center)
        self.can_play_sound = False
        self.lerp = 0
        
        self.glow = glow
        self.glow_rect = self.glow.get_rect(center=self.rect2.center)
        self.sounds = sounds

    def update(self, *args):
        self.screen.blit(self.glow, self.glow_rect)
        self.screen.blit(self.image, self.rect)
        self.image = transform.rotate(self.origimage, self.k * self.koeff)
        self.rect = self.image.get_rect(center=self.rect2.center)
        self.k += 1
        
        if self.hp <= 0:
            self.kill()
            self.player.kills += 1 if not self.player.ulti else 0
        
        if self.rect2.colliderect(self.player.rect):
            self.kill()
            self.player.TakeDamage(self.DealDamage())
        
        if self.rect2.x >= self.player.rect.x:
            self.rect2.centerx -= self.speed / 10
        
        if self.rect2.x <= self.player.rect.x:
            self.rect2.centerx += self.speed / 10
        
        if self.rect2.y >= self.player.rect.y:
            self.rect2.centery -= self.speed / 10
        
        if self.rect2.y <= self.player.rect.y:
            self.rect2.centery += self.speed / 10
        
        self.rect.center = self.rect2.center
        self.glow_rect.center = self.rect2.center
    
    def TakeDamage(self, dmg, channel):
        global cubes_can_sound
        a = random.randint(0, 2)
        if not channel.get_busy() and settings.cubes_can_sound:
            mixer.Sound(self.sounds[a]).play()
            settings.cubes_can_sound = False
        self.hp -= dmg
        self.direction = (
            math.Vector2(self.player.rect.center) - math.Vector2([self.rect.x, self.rect.y])
        ).normalize()
        
        self.pos = self.rect2.center
        self.pos -= self.direction * 20
        self.rect2.center = round(self.pos.x), round(self.pos.y)
    
    def DealDamage(self):
        return self.damage
        
        
