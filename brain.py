import numpy as np

# the brain is a neural network that takes a few inputs and returns movement outputs for the purpose of simulation
class Brain():
    input_size = 8
    output_size = 2
    layer_size = 5

    def __init__(self, layers, weights=np.array([]), biases=np.array([])):
        self.weights = weights
        self.biases = biases
        self.layers = layers
    
    def init_rand_weights(self):
        self.weights = []
        self.biases = []
        for i in range(self.layers):
            if i == 0:
                self.weights.append(
                    np.random.randn(self.layer_size, self.input_size)
                )
                self.biases.append(np.random.rand(self.layer_size))

            elif i == self.layers - 1:
                self.weights.append(
                    np.random.randn(self.output_size, self.layer_size)
                )
                self.biases.append(np.random.rand(self.output_size))


            else:

                self.weights.append(
                    np.random.randn(self.layer_size, self.layer_size)
                )
                self.biases.append(np.random.rand(self.layer_size))


    def inference(self, inputs):
        layer_output = inputs
        for i in range(self.layers):   
            #print(f"layer {i} weights: {self.weights[i]}")     
            #print(f"layer {i} inputs: {layer_output}")
            layer_output = np.matmul(layer_output, self.weights[i].T) + self.biases[i]
            
        return layer_output


    def mutate(self):
        """randomly modify some weights and biases"""
        new_weights = []
        for weight_matrix in self.weights:
            for i in range(len(weight_matrix)):
                for j in range(len(weight_matrix[i])):
                    if np.random.rand() < 0.05:
                        weight_matrix[i][j] += np.random.randn()
            new_weights.append(weight_matrix)

        self.weights = new_weights
        
            

if __name__ == '__main__':
    brain = Brain(3)
    
    brain.init_rand_weights()
    a = brain.inference(np.array([1]*brain.input_size).T)
    print(a)