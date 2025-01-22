import math
import pygame as pyg
import pygame.freetype as pygfont
from random import randint as rdi
from const import CENTER, WIDTH, HEIGHT
from colors import *
from functions import *

class BaseEntity():
    def __init__(self, surface, radius: tuple[int, int], pos: tuple[int, int], bounds: tuple[int, int, int, int], offset: int = 3, speed: int | float = 2, **kwargs):
        self.surface = surface
        self.radius = radius
        self.pos = pos
        self.x, self.y = pos
        self.bounds = bounds
        self.circle_width = kwargs.get('circle_width', 0)
        self.bound_offset = (radius + offset)
        self.speed = speed
    
    def render(self):
        pyg.draw.circle(self.surface, self.color, (self.x, self.y), self.radius, self.circle_width)

class Projectile(BaseEntity):
    def __init__(self, surface, radius: tuple[int, int], pos: tuple[int, int], bounds: tuple[int, int, int, int], **kwargs):
        super(Projectile, self).__init__(surface, radius, pos, bounds, **kwargs)
        self.color = BLUE

        mx, my = pyg.mouse.get_pos()
        self.dir = mx-self.x, my-self.y

        leng = math.hypot(*self.dir)
        
        if leng == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/leng, self.dir[1]/leng)
                
    def move(self):
        self.speed += 0.03
        self.x = self.x + self.dir[0] * self.speed
        self.y = self.y + self.dir[1] * self.speed
    
class Player(BaseEntity):
    def __init__(self, surface, radius: tuple[int, int], pos: tuple[int, int], bounds: tuple[int, int, int, int], color=WHITE, **kwargs):
        super(Player, self).__init__(surface, radius, pos, bounds, **kwargs)
        self.health = 100 
        self.color = color
        self.projectiles = [ ]
        self.projectiles_shoot = 0
        self.speed = 2.5
    
    def shoot(self, radius: tuple[int, int]):
        self.projectiles_shoot += 1
        self.projectiles.append(Projectile(self.surface, radius, (self.x, self.y), None))
    
    def move(self):
        x, y, w, h = self.bounds
        keys = pyg.key.get_pressed()

        if keys[pyg.K_w]:
            if self.y > y + self.bound_offset:
                self.y -= self.speed
        
        if keys[pyg.K_s]:
            if self.y < h - self.bound_offset:
                self.y += self.speed

        if keys[pyg.K_a]:
            if self.x > x + self.bound_offset:
                self.x -= self.speed
        
        if keys[pyg.K_d]:
            if self.x < w - self.bound_offset:
                self.x += self.speed 

    def get_pos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def damage(self, dmg: int):
        self.health = max(0, self.health-dmg)
    
    def info(self):
        font = pygfont.Font('JetBrains Mono Bold.ttf', 12)
        info = f'HP: {self.health}'
        surf, rect = font.render(info, 25)
        wid, hei = surf.get_width(), surf.get_height()
        pos = (self.x-wid/2, self.y-self.radius-hei-5)

        font.render_to(self.surface, pos, info, WHITE)
        
class Enemy(BaseEntity):
    def __init__(self, surface, radius: tuple[int, int], pos: tuple[int, int], bounds: tuple[int, int, int, int], **kwargs):
        super(Enemy, self).__init__(surface, radius, pos, bounds, **kwargs)
        self.color = random_color()
        self.damage = rdi(0, 10)
        self.speed = 3
    
    def move_to_player(self, pos: tuple[int, int]):
        self.speed += 0.02
        px, py = pos
        a, b = px-self.x, py-self.y

        angle = math.atan2(a, b)
        
        x = math.sin(angle)
        y = math.cos(angle)

        self.x += x * self.speed * .72
        self.y += y * self.speed * .72

    def death(self, target: BaseEntity) -> bool:
        if math.hypot(self.x-target.x, self.y-target.y) < self.radius + target.radius:
            return (True)
        return (False)
        
