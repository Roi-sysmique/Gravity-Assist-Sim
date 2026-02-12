import pygame
import sys
from pygame import Vector2
import math

pygame.init()

HEIGHT, WIDTH = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SRCALPHA)
pygame.display.set_caption("Gravity Assist Sim")
clock = pygame.time.Clock()
gravity_constant = 10
font = pygame.font.SysFont("Arial", 30)

class Entity:
    def __init__(self, position:Vector2, mass:float, velocity:Vector2, acceleration:Vector2, radius:int, color:tuple,
                 mobile:bool):
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
        self.mobile = mobile

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
                force = (self.mass * entity.mass * gravity_constant) / (distance ** 2)
                force_vec = distance_vec.normalize() * force
                self.velocity += force_vec



    def update(self, entities):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.rect.center = self.position
        if self.mobile:
            self.gravity(entities)

class Spaceship(Entity):
    def __init__(self, position:Vector2, mass:float, velocity:Vector2, acceleration:Vector2, radius:int, color:tuple):
        super().__init__(position, mass, velocity, acceleration, radius, color, True)
        self.fuel = 200
        self.angle = 0
        self.color = (40, 40, 40)

    def movement(self, keys):
        if keys[pygame.K_SPACE] and self.fuel > 0:
            self.fuel -= 5
            self.velocity += Vector2(0.2*math.cos(math.radians(self.angle- 90)), 0.2*math.sin(math.radians(self.angle-90)))
        if keys[pygame.K_RIGHT]:
            self.angle += 10
        elif keys[pygame.K_LEFT]:
            self.angle -= 10

    def draw(self, surface):
        speed_txt  = font.render("Vitesse: " + str(round(self.velocity.length(), 2)), True, (255, 255, 255))
        speed_rect = speed_txt.get_rect(topleft=(10, 40))
        pygame.draw.rect(surface, (0, 0, 0, 255), (10, 10, 200, 25), border_radius=5)
        pygame.draw.rect(surface, (255, 0, 0, 255), (10, 10, self.fuel, 25), border_radius=5)
        surface.blit(self.image, self.rect)
        surface.blit(speed_txt, speed_rect)

    def update(self, entities):
        self.movement(pygame.key.get_pressed())

        canva = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.polygon(canva, self.color,
                            ((self.radius, 0),
                             (0, self.diameter),
                             (self.radius, self.diameter - 10),
                             (self.diameter, self.diameter)))
        self.image = pygame.transform.rotozoom(canva, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)

        super().update(entities)


def main():
    fps = 60
    entities = []
    entity = Entity(Vector2(WIDTH/2, HEIGHT / 2), 100, Vector2(0, 0), Vector2(0, 0),50, (255,255,0), False)
    entities.append(entity)

    spaceship = Spaceship(Vector2(WIDTH * 3 / 2, HEIGHT / 2), 5, Vector2(0, 0), Vector2(0, 0),20, (0,255,0))
    entities.append(spaceship)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((10, 10, 30))
        for entity in entities:
            entity.update(entities)
            entity.draw(SCREEN)
        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    main()
