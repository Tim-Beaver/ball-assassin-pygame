from pygame import *
import settings
from player import Player, Reload, Pointer
from enemies import EnemyCube
from uxgui import HpBar, WaveTime, WaveCount, Hp_text, Loss_text, KdUlt
import random
import schedule
import os
from math import *


WAVE = 1
WAVE_TIME = 10
t = WAVE_TIME

counter = WAVE

kills_needed = 90


def SpawnEnemyCoordinates():
    a = random.randint(1, 4)
    if a == 1:
        x = random.randint(-100, -60)
        y = random.randint(-80, screen.get_height() + 80)
    elif a == 2:
        x = random.randint(screen.get_width() + 60, screen.get_width() + 100)
        y = random.randint(-80, screen.get_height() + 80)
    elif a == 3:
        x = random.randint(-80, screen.get_width() + 80)
        y = random.randint(-100, -60)
    elif a == 4:
        x = random.randint(-80, screen.get_width() + 80)
        y = random.randint(screen.get_height() + 60, screen.get_height() + 100)
    else:
        x = random.randint(-80, screen.get_width() + 80)
        y = random.randint(screen.get_height() + 60, screen.get_height() + 100)
    return x, y


def Timing():
    global t
    t -= 1


def SpawnWave():
    global WAVE, WAVE_TIME, spawning, counter, t, timing

    schedule.cancel_job(spawning)
    schedule.cancel_job(timing)
    WAVE += 1
    if WAVE == 40:
        WAVE_TIME = 4

    if WAVE == 80:
        WAVE_TIME = 3

    if WAVE == 120:
        WAVE_TIME = 2
    if WAVE == 228:
        WAVE_TIME = 1
    if WAVE == 999:
        raise RuntimeError()

    counter = WAVE
    if WAVE <= 40:
        spawn_range = WAVE * 2
    else:
        spawn_range = 80
    
    
    if len(enemies) > 20 and WAVE <= 120:
        for x in range(len(enemies) // 2):
            enemies.sprites()[x].kill()
    
    
    elif len(enemies) > 50:
        for x in range(len(enemies) // 2):
            enemies.sprites()[x].kill()

    settings.DAMAGE += 0.5 if WAVE <= 120 else 0.3
    player.damage = settings.DAMAGE

    settings.ATTACK_SPEED += 1 if WAVE <= 70 else 0

    settings.HP += 3
    if player.hp + settings.HP // 10 < settings.HP:
        player.hp += settings.HP // 10
    else:
        player.hp = settings.HP

    settings.SPEED += 5 if settings.SPEED < 125 else 0
    player.speed = settings.SPEED

    if WAVE % 4 == 0:
        settings.MULTISHOT += 1 if settings.MULTISHOT <= 16 else 0
        settings.STEALTH += 0.1
        settings.ENEMY_SPEED += 1 if settings.ENEMY_SPEED <= 35 else 0
        settings.ENEMY_DMG += 1
        if WAVE_TIME > 5:
            WAVE_TIME -= 1
        if settings.ARMOR <= 0.6:
            settings.ARMOR += 0.04 if settings.ARMOR <= 0.4 else 0.02
    
    
    for i in range(spawn_range):
        EnemyCube(
            enemies,
            screen,
            settings.ENEMY_SPEED,
            player,
            SpawnEnemyCoordinates(),
            9 * WAVE,
            settings.ENEMY_DMG,
            hit_sounds,
            cubeimage,
            cubeglow,
        )

    spawning = schedule.every(WAVE_TIME).seconds.do(SpawnWave)
    timing = schedule.every().seconds.do(Timing)

    t = WAVE_TIME


def Shake(i):
    global shaking
    if i <= 5:
        if player.ulti <= 0:
            for x in [players, particles]:
                for y in x:
                    y.rect.centerx += random.random() * random.choice([-1, 1]) * 10
        else:
            for x in [players, particles, enemies, projectiles]:
                for y in x:
                    y.rect.centerx += random.random() * random.choice([-1, 1]) * 10
    else:
        shaking = False
i = 0

def IngniteShake(x):
    global shaking, i, reload
    if x:
        shaking = True
        reload.canshake = False
        i = 0




mixer.pre_init()
init()


mixer.init()
snd_1, snd_2, snd_3 = (
    mixer.Sound("sounds\hit1.wav"),
    mixer.Sound("sounds\hit2.wav"),
    mixer.Sound("sounds\hit3.wav"),
)
hit_sounds = [snd_1, snd_2, snd_3]
hit_channel = mixer.Channel(6)
shot = mixer.Sound("sounds\shot1.wav")
boom = mixer.Sound("sounds\shot.wav")
shot_sound = shot
shot_channel = mixer.Channel(7)

ost1 = mixer.music.load("sounds/ost.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)


font.init()
deltaTime = 0

screen = display.set_mode([1280, 720], vsync=1)
display.set_icon(image.load("images\ico1.png").convert_alpha())
display.set_caption("Ball Assassin")
shaking = False

clock = time.Clock()

Running = True

players = sprite.Group()
projectiles = sprite.Group()
particles = sprite.Group()
enemies = sprite.Group()
ui = sprite.Group()
loss_ui = sprite.Group()

cubeimage = transform.scale_by(
    image.load("images/cube_enemy.png").convert_alpha(), 0.15
)
cubeglow = transform.scale_by(
    image.load("images/cube_enemy_glow.png").convert_alpha(), 0.3
)
bullet = transform.scale_by(image.load("images/bullet.png").convert_alpha(), 0.4)
bulletimage = bullet
ultis = transform.scale_by(image.load("images/ultimate.png").convert_alpha(), 0.4)


player = Player(players, settings.SPEED, screen, 50, (200, 11, 110))
reload = Reload(players, screen, player, shot_channel, enemies)
pointer = Pointer(players, screen, 20, player)
EnemyCube(
    enemies,
    screen,
    settings.ENEMY_SPEED,
    player,
    SpawnEnemyCoordinates(),
    6 * WAVE,
    settings.ENEMY_DMG,
    hit_sounds,
    cubeimage,
    cubeglow,
)

hpbar = HpBar(ui, player, screen)
hptext = Hp_text(ui, screen)
wavetime = WaveTime(ui, player, screen, WAVE_TIME)
wavecount = WaveCount(ui, player, screen, WAVE)
kdult = KdUlt(ui, player, screen, 0)
loss_text = None

player_spraying = False
spawning = schedule.every(WAVE_TIME).seconds.do(SpawnWave)
timing = schedule.every().seconds.do(Timing)


mouse.set_visible(False)
cursor = transform.scale_by(image.load("images/aim.png").convert_alpha(), 0.4)
cursor_pos = cursor.get_rect(center=mouse.get_pos())

game_over_screen = image.load("images/game_over.png").convert_alpha()
fire = [transform.scale(image.load("images/particle.png"), (5, 5))]
for scale in [10, 12]:
    fire.append(transform.scale(fire[0], (scale, scale)))

while Running:
    for void in event.get():
        if void.type == QUIT:
            Running = False
            quit()
        if void.type == MOUSEBUTTONDOWN:
            if void.button == 1:
                player_spraying = True
                reload.Shoot(
                    projectiles,
                    particles,
                    random.choice(fire), 
                    settings.MULTISHOT,
                    bulletimage,
                    shot_sound,
                )
                IngniteShake(reload.canshake)
                
        elif void.type == MOUSEBUTTONUP:
            if void.button == 1:
                player_spraying = False
        if void.type == MOUSEMOTION:
            pointer.Rotate()
        if void.type == KEYDOWN:
            if void.key == K_F12:
                for x in enemies.sprites():
                    x.kill()
                SpawnWave()
            if void.key == K_r:
                if player.kills >= kills_needed:
                    player.kills = 0
                    player.ulti = 720
                    bulletimage = ultis
                    shot_sound = boom
                    k = round(WAVE * 1.5)
                    if k < 90:
                        kills_needed = 90
                    else:
                        kills_needed = k

    screen.fill((0, 0, 0))
    if settings.MODE == "game":
        projectiles.update(deltaTime, enemies.sprites(), hit_channel)
        enemies.update(deltaTime)
        players.update(deltaTime)
        particles.update(deltaTime)
        particles.draw(screen)
        ui.update(deltaTime, t, counter, kills_needed)
    elif settings.MODE == "wasted":
        if not loss_text:
            loss_text = Loss_text(loss_ui, screen, WAVE)
        players.update(deltaTime)
        particles.update(deltaTime)
        particles.draw(screen)
        loss_ui.update(deltaTime, t, counter)
        screen.blit(
            game_over_screen,
            game_over_screen.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2 - 250)
            ),
        )
    
    if player.ulti > 0:
        player.ulti -= 1
    else:
        shot_sound = shot
        bulletimage = bullet
        player.ulti = 0

    cursor_pos.center = mouse.get_pos()
    screen.blit(cursor, cursor_pos)

    clock.tick_busy_loop(settings.FPS)
    deltaTime = clock.get_time() / 1000
    
    if shaking:
        Shake(i)
        i += 1
    
    if key.get_pressed()[K_F12]:
        for x in enemies.sprites():
            x.kill()
        SpawnWave()
    
    display.update()
    schedule.run_pending()
    

    if player_spraying:
        reload.Shoot(
            projectiles,
            particles,
            random.choice(fire),
            settings.MULTISHOT,
            bulletimage,
            shot_sound,
        )
        IngniteShake(reload.canshake)
