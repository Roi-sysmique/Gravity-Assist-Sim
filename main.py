from os import fspath

import pygame
import sys

pygame.init()

HEIGHT, WIDTH = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Assist Sim")
clock = pygame.time.Clock()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pass

def main():
    fps = 60
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill('light blue')
        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    main()
