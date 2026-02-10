import pygame
import sys
from pygame import Vector2

pygame.init()

HEIGHT, WIDTH = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Assist Sim")
clock = pygame.time.Clock()

class Entity(pygame.sprite.Sprite):
    def __init__(self, position:Vector2, mass:float, velocity:Vector2, radius:int, color:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.diameter = radius * 2
        self.image = pygame.Surface((self.diameter, self.diameter)).convert_alpha()
        self.image.fill('white')
        self.image.set_colorkey('white')
        self.rect = self.image.get_rect(center=self.position)
        self.color = color
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

def main():
    fps = 60
    entity = Entity(Vector2(WIDTH / 2, HEIGHT / 2), 0, Vector2(50, 50), 20, (255,255,0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill('light blue')
        entity.draw(SCREEN)
        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    main()
