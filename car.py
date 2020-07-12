import pygame
import math
from settings import *
import copy

class Car:
    def __init__(self):
        self.surface = pygame.image.load("img/car.png")
        self.surface = pygame.transform.scale(self.surface, (car_size, car_size))
        self.rotate_surface = self.surface
        self.pos = [640, 660]
        self.angle = 0
        self.speed = 0
        self.center = [self.pos[0] + car_size / 2, self.pos[1] + car_size / 2]
        self.radars = []
        self.radars_for_draw = []
        self.is_alive = True
        self.goal = False
        self.distance = 0
        self.time_spent = 0
        self.speed_counter = 0

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
        self.draw_radar(screen)

    def draw_radar(self, screen):
        for r in self.radars:
            pos, dist = r
            pygame.draw.aaline(screen, (255, 200, 50), self.center, pos)
            pygame.draw.circle(screen, (255, 200, 50), pos, 5)

    def check_collision(self, map):
        self.is_alive = True
        for p in self.four_points:
            if map.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
                self.is_alive = False
                break

    def check_radar(self, degree, map):
        len = 10
        x = round(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
        y = round(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        while not map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
            len = len + 1
            x = round(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = round(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        dist = round(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self, map):

        old_pos = copy.deepcopy(self.pos)

        # check position
        self.rotate_surface = self.rot_center(self.surface, self.angle)
        self.pos[0] += round(math.cos(math.radians(360 - self.angle)) * self.speed)
        if self.pos[0] < 0:
            self.pos[0] = 0
        elif self.pos[0] > screen_width - 20:
            self.pos[0] = screen_width - 20
        self.distance += self.speed
        self.time_spent += 1
        self.pos[1] += round(math.sin(math.radians(360 - self.angle)) * self.speed)
        if self.pos[1] < 0:
            self.pos[1] = 20
        elif self.pos[1] > screen_height - 20:
            self.pos[1] = screen_height - 20

        # caclulate 4 collision points
        self.center = [round(self.pos[0]) + car_size / 2, round(self.pos[1]) + car_size / 2]
        len = collision_corner_dist
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * len,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * len,
                     self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * len,
                       self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * len,
                        self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        self.four_points = [left_top, right_top, left_bottom, right_bottom]

        self.check_collision(map)
        self.radars.clear()
        for d in range(-90, 91, 45):
            self.check_radar(d, map)

        if self.speed > 0:
            self.speed_counter = 0
        else:
            self.speed_counter += 1


    def get_data(self):
        radars = self.radars
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(radars):
            ret[i] = r[1] / 300
        ret.append(self.speed/max_speed_car)
        #print("RETURN DATA:")
        #print(ret)
        return ret

    def get_alive(self):
        if self.time_spent > timeout or self.speed_counter > car_timeout:
            self.is_alive = False
        return self.is_alive

    def get_reward(self):
        if time_weight != 0:
            #print(self.distance/self.time_spent)
            return self.distance * distance_weight / (time_weight * self.time_spent)
        else:
            n_bonus = int(self.distance / bonus_dist)
            return self.distance * distance_weight + n_bonus * bonus * n_bonus

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image