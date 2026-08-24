from pygame import *
import os
from math import *
from particles import Particle, create_particles
import settings


class Player(sprite.Sprite):
    def __init__(self, group, speed, scr, radius, color):
        super().__init__()
        self.add(group)

        self.screen, self.radius, self.color = scr, radius, color

        self.rect = Rect(600, 300, 100, 100)
        self.rect2 = Rect(600, 300, 100, 100)
        self.speed = settings.SPEED
        self.hp = settings.HP
        self.damage = settings.DAMAGE
        self.dead = False
        self.glow = transform.scale_by(image.load('images/player_glow.png').convert_alpha(), 0.3)
        self.glow_rect = self.glow.get_rect(center=self.rect.center)
        
        self.ulti = 0
        
        self.kills = 0

    def update(self, *args):
        self.Move(args[0])
        self.Glow()
        
        self.rect.center = self.rect2.center
        draw.circle(
            self.screen,
            self.color,
            (self.rect.x + self.radius, self.rect.y + self.radius),
            self.radius,
            8,
        )
        
        if self.hp <= 0 and not self.dead:
            self.GameOver()

    def Move(self, dt):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect2.x -= self.speed * dt * 10
        if keys[K_d] and self.rect.x < (self.screen.get_width() - self.radius * 2):
            self.rect2.x += self.speed * dt * 10
        if keys[K_w] and self.rect.y > 0:
            self.rect2.y -= self.speed * dt * 10
        if keys[K_s] and self.rect.y < (self.screen.get_height() - self.radius * 2):
            self.rect2.y += self.speed * dt * 10
    
    def Glow(self):
        if self.glow_rect.centerx < self.rect.centerx:
            self.glow_rect.centerx += self.Lerp(self.glow_rect.centerx, self.rect.centerx, 0.2)
        elif self.glow_rect.centerx > self.rect.centerx:
            self.glow_rect.centerx -= self.Lerp(self.glow_rect.centerx, self.rect.centerx, 0.2)
        if self.glow_rect.centery < self.rect.centery:
            self.glow_rect.centery += self.Lerp(self.glow_rect.centery, self.rect.centery, 0.2)
        elif self.glow_rect.centery > self.rect.centery:
            self.glow_rect.centery -= self.Lerp(self.glow_rect.centery, self.rect.centery, 0.2)
        
        self.screen.blit(self.glow, self.glow_rect)
    
    def GameOver(self):
        settings.MODE = 'wasted'
        self.dead = True
        mixer.Sound('sounds/loss.wav').play()
        mixer.music.stop()
    
    def Lerp(self, start, end, lerp):
        return abs(start - end) * lerp

    def TakeDamage(self, dmg):
        self.hp -= dmg * (1 - settings.ARMOR)


class Reload(sprite.Sprite):
    def __init__(self, group, scr, player, sound, enemies):
        super().__init__()
        self.add(group)
        self.screen, self.player = scr, player
        self.radius = self.player.radius - 12
        self.enemies = enemies
        self.canshake = False

        self.reload = 360

        self.rect = Rect(612, 312, 100, 100)
        self.rect.width = player.rect.width - 20
        self.rect.height = player.rect.height - 20
        
        self.sound = sound

    def update(self, *args):
        self.rect.x, self.rect.y = self.player.rect.x, self.player.rect.y
        draw.circle(
            self.screen,
            (255, 255, 255),
            (self.rect.x + self.player.radius, self.rect.y + self.player.radius),
            self.player.radius - 12,
            3,
        )
        draw.circle(
            self.screen,
            (0, 0, 0),
            (self.rect.x + self.player.radius, self.rect.y + self.player.radius),
            self.player.radius - 8,
            4,
        )
        draw.circle(
            self.screen,
            (0, 0, 0),
            (self.rect.x + self.player.radius, self.rect.y + self.player.radius),
            self.player.radius - 15,
        )
        draw.arc(
            self.screen,
            (0, 0, 0),
            (self.rect.x + 10, self.rect.y + 10, 80, 80),
            radians(90),
            radians(90 + self.reload),
            10,
        )

        if self.reload > 0.01:
            self.reload -= settings.ATTACK_SPEED
        if self.reload < 0:
            self.reload = 0

    def Shoot(self, group, particle_group, particle_image, multishot, image, snd):
        if self.reload <= 0.01:
            self.canshake = True
            self.reload = 360

            for i in range(multishot):
                Bullet(group, self.screen, self.player, i * 1 if i % 2 != 0 else i * -1, image)
            
            settings.cubes_can_sound = True
            
            create_particles(self.player.rect.center, particle_group, self.player, particle_image)
            
            self.sound.play(snd)
            
            
        
            
            


class Pointer(sprite.Sprite):
    def __init__(self, group, scr, side, player):
        super().__init__()
        self.add(group)
        self.image = transform.scale_by(
            image.load("images/pointer.png").convert_alpha(), 0.3
        )
        self.origimage = self.image
        self.screen, self.player, self.side = scr, player, side
        self.rect = Rect(600, 300, 100, 100)
        self.rect = self.image.get_rect(center=self.rect.center)

        mouse_x, mouse_y = mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.angle = (180 / pi) * -atan2(rel_y, rel_x)

    def update(self, *args):
        self.screen.blit(self.image, self.rect)
        

        mouse_x, mouse_y = mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y


        self.direction = (
            math.Vector2(mouse.get_pos()) - math.Vector2([self.rect.centerx, self.rect.centery])
        )
        radius, self.angle = self.direction.as_polar()
        self.Rotate()

    def Rotate(self):
        self.image = transform.rotate(self.origimage, -self.angle - 90)
        self.rect = self.image.get_rect(center=self.player.rect.center)


class Bullet(sprite.Sprite):
    def __init__(self, group, scr, player, multishot, image):
        super().__init__()
        self.add(group)

        self.screen, self.player = scr, player
        self.origimage = image
        self.image = self.origimage
        self.rect = self.image.get_rect(center=self.player.rect.center)

        self.pos = math.Vector2(self.rect.center)

        self.direction = (
            Vector2(mouse.get_pos()) - Vector2([self.rect.x + 10 * multishot, self.rect.y + 10 * multishot])
        ).normalize()
        
        radius, self.angle = self.direction.as_polar()
        
        self.image = transform.rotate(self.origimage, -self.angle - 90)
        self.rect = self.image.get_rect(center=self.player.rect.center)
        

    def update(self, *args):
        self.screen.blit(self.image, self.rect)

        if self.rect.colliderect(self.screen.get_rect()):
            self.pos += self.direction * args[0] * 2000
            self.rect.center = round(self.pos.x), round(self.pos.y)
        else:
            self.kill()
        
        a = self.rect.collidelist(args[1])
        if a > -1:
            if self.player.ulti <= 0:
                self.kill()
            args[1][a].TakeDamage(self.player.damage, args[2])
            self.player.hp += settings.STEALTH if self.player.hp < settings.HP else 0

            
