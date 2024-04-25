from brain import Brain
import numpy as np
import random

class Glob():
    def __init__(self, name, brain, pos, health=10):
        self.name = name
        self.brain = brain
        self.health = health
        self.color = (255, 255, 255)
        self.pos = pos



    def think(self, inputs):
        return self.brain.inference(inputs)
    
    def generate_brain(self):
        self.brain = Brain(1)
        self.brain.init_rand_weights()

    def perceive(self, food_array):
        """Uses position of self, and casts 8 rays in all directions to detect food."""
        # rays are equally spaced, food array is pos of all food circles
        # detect if rays intersect with food circles
        dist = 0
        rays = [
            (dist, 0),
            (dist, dist),
            (0, dist),
            (-dist, dist),
            (-dist, 0),
            (-dist, -dist),
            (0, -dist),
            (dist, -dist)
        ]

        # calculate proj of ray onto food
        inputs = []
        for ray in rays:
            min_dist = float('inf')
            for food in food_array:
                global_ray = (self.pos[0] + ray[0], self.pos[1] + ray[1])
                global_ray = np.array(global_ray)
                food = np.array(food)
                proj_ray = np.dot(global_ray, food) / np.dot(food, food)
                proj_ray = proj_ray * food
                dist = np.dot(proj_ray, proj_ray)/100000
                if dist < min_dist:
                    min_dist = dist

            inputs.append(min_dist)
        return np.array(inputs).T
    
    def mutate(self):
        self.brain.mutate()

    def crossover(self, other):
        new_weights = []
        new_biases = []
        for i in range(self.brain.layers):
            if random.random() < .5:
                new_weights.append(self.brain.weights[i])
                new_biases.append(self.brain.biases[i])

            else:
                new_weights.append(other.brain.weights[i])
                new_biases.append(other.brain.biases[i])
        new_brain = Brain(self.brain.layers, new_weights, new_biases)
        return new_brain

    
    def __repr__(self) -> str:
        return f"Glob({self.name}, {self.brain}, {self.health})"
    
if __name__ == '__main__':
    glob1 = Glob("Glob1", Brain(1), (0, 0))
    glob2 = Glob("Glob2", Brain(1), (0, 0))

    glob1.generate_brain()
    glob2.generate_brain()

    glob1.crossover(glob2)
    print(glob1)
    print(glob2)
    