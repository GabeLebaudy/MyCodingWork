import numpy as np


def forward_propagation(x_inputs, parameters):
    num_layers = len(parameters) // 2
    caches = {}
    
    #First Layer
    caches['Z1'] = np.dot(parameters['W1'], x_inputs) + parameters['b1']
    caches['A1'] = np.maximum(0, caches['Z1'])
    
    for layer in range(1, num_layers - 1):
        caches['Z' + str(layer + 1)] = np.dot(parameters['W' + str(layer + 1)], caches['A' + str(layer)]) + parameters['b' + str(layer + 1)]
        caches['A' + str(layer + 1)] = np.maximum(0, caches['Z' + str(layer + 1)])
    
    caches['Z' + str(num_layers)] = np.dot(parameters['W' + str(num_layers)], caches['A' + str(num_layers - 1)]) + parameters['b' + str(num_layers)]
    t = np.exp(caches['Z' + str(num_layers)])
    print(t)
    divFactor = np.sum(t)

    caches['A' + str(num_layers)] = t / divFactor
    
    return caches


x = np.array([
    [1, 0, 4, 8, 2],
    [7, 3, 2, 13, -6],
    [2, 0, 6, -4, 11],
    [6, 1, 2, 3, 6]
])
w1 = np.array([
    [6, 3, 0, -1],
    [4, 11, 7, 1],
    [2, 1, 0, 4],
    [7, 3, 12, 5]
])
w2 = np.array([
    [1, 4, 16, -3],
    [-7, 2, 6, 1]
])
w3 = np.array([
    [1, 4]
])
b1 = np.array([
    [1],
    [7],
    [-2],
    [3]
])
b2 = np.array([
    [1],
    [4]
])
b3 = np.array([2])

parameters = {}
parameters['W1'] = w1
parameters['W2'] = w2
parameters['W3'] = w3
parameters['b1'] = b1
parameters['b2'] = b2
parameters['b3'] = b3

caches = forward_propagation(x, parameters)
for cache in caches:
    print(cache, caches[cache])