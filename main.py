import pygame as pyg
from colors import *
from const import *
from assets import *
from functions import *
from entities import Player, Enemy
from timer import TimedEvent
from random import randint as rdi
from random import choice as rdc

pyg.display.set_caption("Infinitum")
pyg.display.set_icon(LOGO)
pyg.init()
timer = pyg.time.Clock()

advance_wave = TimedEvent(2000, False)

class Control():
    def __init__(self, width: int, height: int):
        self.game_over = False
        self.surface = pyg.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.color = 'green'
        self.size = (width, height)
        self.pos = (WIDTH-height, HEIGHT-height)
        self.player = Player(self.surface, 20.5, CENTER, (*self.pos, width, height), circle_width=3)
        self.enemies = []
        self.pause = False
        
        self.score = 0
        self.wave = 0
        self.enemies_per_wave = 1

    def spawn_wave(self):
        self.wave += 1
        self.enemies_per_wave += .7
        self.enemies += [Enemy(self.surface, 12, self.rand_pos(20), self.size + self.pos) for _ in range(round(self.enemies_per_wave))]
    
    def event(self):
        for event in pyg.event.get():
            if event.type == pyg.KEYDOWN and event.key == pyg.K_p and not self.game_over:
                self.pause = False if self.pause else True
            
            if event.type == pyg.QUIT:
                self.running = False
                
            if not self.pause:

                if event.type == pyg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.shoot(5)

        advance_wave.update(not self.enemies)
        if not advance_wave.active:
            self.spawn_wave()

    def start(self):
        while self.running:
            timer.tick(FPS)
            
            self.event()

            if self.player.health == 0:
                self.game_over = True

            if self.game_over:
                h1, h2 = 200, 180
                pyg.draw.rect(self.surface, 'grey', (0, HEIGHT/2-h1/2, WIDTH, h1))
                pyg.draw.rect(self.surface, 'black', (0, HEIGHT/2-h2/2, WIDTH, h2))
                render_text_on_screen(self.surface, "GAME OVER", WIDTH/2, HEIGHT/2, 85, RED, adjust=True)
                pyg.display.update()
                continue

            if self.pause:
                h1, h2 = 200, 180
                pyg.draw.rect(self.surface, 'grey', (0, HEIGHT/2-h1/2, WIDTH, h1))
                pyg.draw.rect(self.surface, 'black', (0, HEIGHT/2-h2/2, WIDTH, h2))
                render_text_on_screen(self.surface, "GAME PAUSED", WIDTH/2, HEIGHT/2, 85, BLUE, adjust=True)
                pyg.display.update()
                continue

            self.surface.fill(BLACK)
            render_text_on_screen(self.surface, f"FPS: {timer.get_fps():.0f}", 10, 10, 15, WHITE)
            render_text_on_screen(self.surface, f"WAVE: {self.wave}", WIDTH/2, 30, 15, WHITE, adjust=True)
            render_text_on_screen(self.surface, f"ENEMIES: {len(self.enemies)}", WIDTH/2, 60, 15, WHITE, adjust=True)
            render_text_on_screen(self.surface, f"SCORE: {self.score}", WIDTH/2, 90, 15, WHITE, adjust=True)
            render_text_on_screen(self.surface, "PAUSE: (P)", WIDTH/2, 120, 15, WHITE, adjust=True)
            
            if not self.enemies:
                render_text_on_screen(self.surface, f"NEXT WAVE IN {advance_wave.current_time}s", WIDTH/2, 170, 15, WHITE, adjust=True)

            self.borders()
            
            self.player.move()
            self.player.render()
            self.player.info()
            
            for projectile in self.player.projectiles[:]:
                projectile.move()
                projectile.render()

                if outside_bounds((projectile.x, projectile.y), (*self.pos, *self.size), 20):
                    self.player.projectiles.remove(projectile)

            for enemy in self.enemies[:]:
                death = False
                enemy.move_to_player(self.player.get_pos())
                enemy.render()
                
                if enemy.death(self.player):
                    self.player.damage(enemy.damage)
                    death = True

                for p in self.player.projectiles:
                    if enemy.death(p):
                        self.player.projectiles.remove(p)
                        death = True
                        self.score += 1

                if death:    
                    self.enemies.remove(enemy)
                
            pyg.display.update()

    def borders(self):
        w, h = self.size
        x, y = self.pos

        pyg.draw.line(self.surface, self.color, (x, y), (w, y), 1) # TOP

        pyg.draw.line(self.surface, self.color, (x, y), (x, h), 1) # LEFT
        
        pyg.draw.line(self.surface, self.color, (w, y), (w, h), 1) # RIGHT
        
        pyg.draw.line(self.surface, self.color, (x, h), (w, h), 1) # BOTTOM

    def rand_pos(self, s: int = 0) -> tuple[int, int]:
        x = rdc([rdi(-300, -100) - s, rdi(WIDTH+100,  WIDTH+300)  + s])
        y = rdc([rdi(-300, -100) - s, rdi(HEIGHT+100, HEIGHT+300) + s])

        return (x, y)

Game = Control(750, 750) # Border limit

if __name__  == '__main__':
    Game.start()