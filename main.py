import pygame
import sys
import visualize
import neat
from car import Car
from settings import *


def run_car(genomes, config):
    # Init my game
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    font = pygame.font.SysFont("Arial", 30)
    map = pygame.image.load(racetrack)

    # Init NEAT
    nets = []
    cars = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        # Init my cars
        cars.append(Car())

    # Main loop
    global generation
    generation += 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # Input my data and get result from network
        for index, car in enumerate(cars):
            #print("CAR " + str(index))
            output = nets[index].activate(car.get_data())
            #print("OUTPUT")
            #print(output)
            if output[0] > steering_thr:
                car.angle += steer_speed_car
            elif output[1] > steering_thr:
                car.angle -= steer_speed_car
            if output[2] > acc_thr and car.speed < max_speed_car:
                car.speed += acc_car
            elif output[3] > brake_thr:
                car.speed -= brake_car
                if car.speed < 0:
                    car.speed = 0;

        # Update car and fitness
        remain_cars = 0
        for i, car in enumerate(cars):
            if car.get_alive():
                remain_cars += 1
                car.update(map)
                genomes[i][1].fitness = car.get_reward()

        # check
        if remain_cars == 0:
            break

        # Drawing
        screen.blit(map, (0, 0))
        for car in cars:
            if car.get_alive():
                car.draw(screen)

        text = generation_font.render("Generation : " + str(generation), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1100, 20)
        screen.blit(text, text_rect)

        text = font.render("alive: " + str(remain_cars), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width - 70, screen_height - 20)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(0)


if __name__ == "__main__":
    generation = 0

    # Set configuration file
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    winner = p.run(run_car, n_gen)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    print(winner)
    node_names = {-1: 'S1', -2: 'S2', -3: 'S3', -4: 'S4', -5: 'S5', -6: 'Speed', 0: 'Left', 1: 'Right', 2: 'Accelarate', 3: 'Brake'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
