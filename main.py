import pygame
import sys
from pygame import Vector2

pygame.init()

HEIGHT, WIDTH = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Assist Sim")
clock = pygame.time.Clock()
gravity_constant = 0.1

class Entity(pygame.sprite.Sprite):
    def __init__(self, position:Vector2, mass:int, velocity:Vector2, acceleration:Vector2, radius:int, color:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
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

    def gravity(self, entities):
        for entity in entities:
            if entity == self:
                continue
            distance_vec = entity.position - self.position
            distance = distance_vec.length()
            radius_sum = self.radius + entity.radius
            if distance <= radius_sum:
                penetration = radius_sum - distance
                normal = -distance_vec.normalize()
                self.position += normal * (penetration / 2)
                entity.position -= normal * (penetration / 2)
                relative_speed = self.velocity - entity.velocity
                vn = relative_speed.dot(normal)
                if vn > 0:
                    return
                impulse = -vn * normal
                self.velocity += impulse
                entity.velocity -= impulse
            else:
                force = int(self.mass * entity.mass * gravity_constant) / distance**2
                force_vec = distance_vec.normalize() * force
                self.velocity += force_vec



    def update(self, entities):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.rect.center = self.position
        self.gravity(entities)

def main():
    fps = 60
    entities = []
    entity = Entity(Vector2(WIDTH / 2, HEIGHT / 2), 50, Vector2(1, 1), Vector2(0, 0),20, (255,255,0))
    entities.append(entity)

    entity_2 = Entity(Vector2(WIDTH / 3, HEIGHT / 2), 100, Vector2(0, 0), Vector2(0, 0),20, (0,255,0))
    entities.append(entity_2)

    entity_3 = Entity(Vector2((WIDTH * 3) / 4, HEIGHT / 2), 200, Vector2(0, 0), Vector2(0, 0),40, (255,0,0))
    entities.append(entity_3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill('light blue')
        for entity in entities:
            entity.draw(SCREEN)
            entity.update(entities)
        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    main()
