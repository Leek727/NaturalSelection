import pygame
import glob
from random import randint

class World:
    def __init__(self, width, height, creatures):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.creatures = creatures
        self.food = []

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # draw all creatures as boxes
        for creature in self.creatures:
            pygame.draw.rect(
                screen,
                creature.color,
                (creature.pos[0], creature.pos[1], 10, 10)
            )
        
        # draw all food as circles
        for food in self.food:
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                food,
                5
            )

    def update(self):
        for i,creature in enumerate(self.creatures):
            # move the creature
            movement = creature.think(creature.perceive(self.food))
            max_speed = 6
            if movement[0] > max_speed:
                movement[0] = max_speed
            if movement[1] > max_speed:
                movement[1] = max_speed

            if movement[0] < -max_speed:
                movement[0] = -max_speed

            if movement[1] < -max_speed:
                movement[1] = -max_speed
        
            creature.pos = (creature.pos[0] + movement[0], creature.pos[1] + movement[1])

        # detect if creature is on food
        for i,creature in enumerate(self.creatures):
            for food in self.food:
                # check if food radius is within creature radius
                if (creature.pos[0] - food[0])**2 + (creature.pos[1] - food[1])**2 < 100:

                    creature.health += 1
                    self.food.remove(food)
                    self.food.append((randint(0, self.width), randint(0, self.height)))
                    
        # check if creature is out of bounds
        for i,creature in enumerate(self.creatures):
            if creature.pos[0] < 0 or creature.pos[0] > self.width or creature.pos[1] < 0 or creature.pos[1] > self.height:
                creature.health -= 100

    def rand_populate(self):
        self.creatures = []
        for i in range(100):
            rand_pos = (randint(0, self.width), randint(0, self.height))
            self.creatures.append(
                glob.Glob("Glob" + str(i), None, rand_pos)
            )

        for creature in self.creatures:
            creature.generate_brain()

        self.populate_food()


    def populate_food(self):
        # generate food positions
        for i in range(10):
            # generate rand pos
            rand_pos = (randint(0, self.width), randint(0, self.height))
            self.food.append(rand_pos)


    def end_generation(self):
        # keep only the ones that got food
        new_creatures = []
        for creature in self.creatures:
            if creature.health > 10:
                new_creatures.append(creature)

            else:
                print(f"Creature {creature.name} {creature.health} health")

        self.creatures = new_creatures

        # crossover all survivors
        for i in range(len(self.creatures)):
            rand_pos = (randint(0, self.width), randint(0, self.height))
            creature = glob.Glob("glob", self.creatures[i].crossover(self.creatures[i+1]), rand_pos)
            self.creatures.append(creature)
            self.creatures.append(creature)
            self.creatures.append(creature)
            creature.color = (0,255,255)
 


        # mutate all
        for i in range(len(self.creatures)):
            self.creatures[i].mutate()


        # add new random creatures
        for i in range(100 - len(self.creatures)):
            rand_pos = (randint(0, self.width), randint(0, self.height))
            creature = glob.Glob("Glob" + str(i), None, rand_pos)
            creature.generate_brain()
            self.creatures.append(
                creature
            )


        # populate food
        self.food = []
        self.populate_food()

        # reset positions
        #for creature in self.creatures:
        #    creature.pos = (randint(0, self.width), randint(0, self.height))


world = World(800, 600, [])
world.rand_populate()

# pygame intialization
pygame.init()
screen = pygame.display.set_mode((world.width, world.height))
pygame.display.set_caption("Natural Selection")

timer = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    
    world.update()
    world.draw(screen)
    pygame.display.flip()

    timer += 1
    if timer > 100:
        world.end_generation()
        timer = 0
        print("Generation Ended")
