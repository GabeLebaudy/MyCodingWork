#This file will be used to implement a Nueral Network from Scratch

#Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import random

#Time decorator
def TimeWrapper(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        stop_time = time.time() - start_time
        print("Time for function:", f.__name__, "-", stop_time)
        return result
    return wrapper


#Constants
#Local path (Once Git LFS is generated)
#TRAIN_PATH = os.path.join(os.path.dirname(__file__), 'mnist_train.csv')
#TEST_PATH = os.path.join(os.path.dirname(__file__), 'mnist_test.csv')

#PC Path
TRAIN_PATH = r"E:\Work\MNIST\mnist_train.csv"
TEST_PATH = r"E:\Work\MNIST\mnist_test.csv"

#Laptop
#TRAIN_PATH = r"C:\Users\Gabe\Documents\MNIST\mnist_train.csv"
#TEST_PATH =  r"C:\Users\Gabe\Documents\MNIST\mnist_test.csv"

#Helper Methods
def train_model(layer_dims, learning_rate, beta, num_iterations = 8_000, doTrain = False):
    if not doTrain:
        return
    
    #Read training data
    data = pd.read_csv(TRAIN_PATH, header = None)
    x_inputs = np.array(data.iloc[:30000, 1:])
    y_values = np.array(data.iloc[:30000, 0])
    y_values = y_values.reshape(y_values.shape[0], 1)
    y_true = np.zeros((y_values.shape[0], 10))
    y_true[np.arange(y_values.shape[0]), y_values.flatten()] = 1
    
    #Transpose Matrices to fit dimensions
    x_inputs, y_true = x_inputs.T, y_true.T
    
    #Normalize Data
    x_inputs = x_inputs / 255
    
    #Initialize Parameters
    parameters = initiate_parameters(layer_dims, x_inputs)
    
    #For Momentum
    velocity = initate_dissent_parameters(parameters)
    
    costs = []
    for i in range(num_iterations):
        #Forward Propogation
        caches = forward_propagation(x_inputs, parameters)
        
        #Calculating Cost
        cost = calculate_cost(caches, y_true, len(layer_dims))
        costs.append(cost)
        
        if i % 1000 == 0:
            print("Cost after epoch:", i, '-', cost)
        
        
        #Backward Propogation
        grads = backward_propogation(caches, parameters, y_true, x_inputs)
        
        #Calculate Velocity of gradient descent
        velocity = backprop_with_momentum(grads, velocity, beta)
        
        #Update Parameters
        parameters = update_parameters(parameters, velocity, learning_rate)
    
    #Remove Old Files
    parameters_path = os.path.join(os.path.dirname(__file__), "Parameters")

    for file in os.listdir(parameters_path):
        file_path = os.path.join(parameters_path, file)
        os.remove(file_path)

    #Save parameters
    for parameter in parameters:
        file_path = os.path.join(parameters_path, "{}.csv".format(parameter))
        np.savetxt(file_path, parameters[parameter], delimiter = ',')
    
    plotCost(costs, num_iterations)
    
        
#Shapes Confirmed Correct
def initiate_parameters(layer_dims, X):
    parameters = {}
    
    #First Layer
    parameters['W1'] = np.random.randn(layer_dims[0], X.shape[0]) * 0.01
    parameters['b1'] = np.zeros((layer_dims[0], 1))
    
    #Last Parameters
    for layer in range(1, len(layer_dims)):
        parameters['W' + str(layer + 1)] = np.random.randn(layer_dims[layer], layer_dims[layer - 1]) * 0.01
        parameters['b' + str(layer + 1)] = np.zeros((layer_dims[layer], 1))
    
    return parameters

#For Gradient Dissent With Momentum
def initate_dissent_parameters(parameters):
    caches = {}
    num_layers = len(parameters) // 2
    for i in range(num_layers):
        caches['dW' + str(i + 1)] = np.zeros((parameters['W' + str(i + 1)].shape[0], parameters['W' + str(i + 1)].shape[1]))
        caches['db' + str(i + 1)] = np.zeros((parameters['b' + str(i + 1)].shape[0], parameters['b' + str(i + 1)].shape[1]))
        
    return caches

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
    divFactor = np.sum(t, keepdims=True, axis=0)

    caches['A' + str(num_layers)] = t / divFactor
    
    return caches

def calculate_cost(activations, Y, last_layer_num):
    m = Y.shape[0]
    cost = -1 / m * np.sum(Y * np.log(activations['A' + str(last_layer_num)]))
    return cost

def backward_propogation(activations, parameters, Y, X):
    grads = {}
    
    last_layer_num = len(activations) // 2
    m = X.shape[1]
    
    #Last layer
    grads['dZ' + str(last_layer_num)] = activations['A' + str(last_layer_num)] - Y
    grads['dW' + str(last_layer_num)] = 1 / m * np.dot(grads['dZ' + str(last_layer_num)], activations['A' + str(last_layer_num - 1)].T)
    grads['db' + str(last_layer_num)] = 1 / m * np.sum(grads['dZ' + str(last_layer_num)], keepdims=True, axis=1)
    
    #Middle Layers
    for layer in range(last_layer_num - 1, 1, -1):
        grads['dZ' + str(layer)] = np.dot(parameters['W' + str(layer + 1)].T, grads['dZ' + str(layer + 1)]) * np.where(activations['Z' + str(layer)] <= 0, 0, 1)
        grads['dW' + str(layer)] = 1 / m * np.dot(grads['dZ' + str(layer)], activations['A' + str(layer - 1)].T)
        grads['db' + str(layer)] = 1 / m * np.sum(grads['dZ' + str(layer)], keepdims=True, axis=1)
        
    #First Layer
    grads['dZ1'] = np.dot(parameters['W2'].T, grads['dZ2']) * np.where(activations['Z1'] <= 0, 0, 1)
    grads['dW1'] = 1 / m * np.dot(grads['dZ1'], X.T)
    grads['db1'] = 1 / m * np.sum(grads['dZ1'], keepdims=True, axis=1)
    
    return grads

def backprop_with_momentum(grads, velocity, beta):
    num_layers = len(grads) // 3
    
    for i in range(num_layers):
        velocity['dW' + str(i + 1)] = beta * velocity['dW' + str(i + 1)] + (1 - beta) * grads['dW' + str(i + 1)]
        velocity['db' + str(i + 1)] = beta * velocity['db' + str(i + 1)] + (1 - beta) * grads['db' + str(i + 1)]
    
    return velocity
 
def update_parameters(parameters, grads, learning_rate):
    layers = len(parameters) // 2
    
    for layer in range(layers):
        parameters['W' + str(layer + 1)] = parameters['W' + str(layer + 1)] - learning_rate * grads['dW' + str(layer + 1)]
        parameters['b' + str(layer + 1)] = parameters['b' + str(layer + 1)] - learning_rate * grads['db' + str(layer + 1)]

    return parameters

def test_model():
    #Read test file data
    data = pd.read_csv(TEST_PATH, header = None)
    x_inputs = np.array(data.iloc[:1000, 1:])
    y_values = np.array(data.iloc[:1000, 0])
    y_values = y_values.reshape(y_values.shape[0], 1)
    y_true = np.zeros((y_values.shape[0], 10))
    y_true[np.arange(y_values.shape[0]), y_values.flatten()] = 1
    
    #Transpose Matrices to fit dimensions
    x_inputs, y_true = x_inputs.T, y_true.T
    
    #Normalize Data
    x_inputs = x_inputs / 255

    #Get parameters from file data
    parameters = {}
    folder_path = os.path.join(os.path.dirname(__file__), 'Parameters')
    num_layers = len([name for name in os.listdir(folder_path)]) // 2

    for i in range(num_layers):
        parameters['W' + str(i + 1)] = np.loadtxt(os.path.join(folder_path, 'W{}.csv'.format(i + 1)), delimiter = ',')
        parameters['b' + str(i + 1)] = np.loadtxt(os.path.join(folder_path, 'b{}.csv'.format(i + 1)), delimiter = ',')
        parameters['b' + str(i + 1)] = parameters['b' + str(i + 1)].reshape(parameters['b' + str(i + 1)].shape[0], 1)
    
    #Determine AI Outputs for test data
    last_layer_num = len(parameters) // 2
    activations = forward_propagation(x_inputs, parameters)
    ai_output = activations['A' + str(last_layer_num)]
    
    #Find the index of which number the AI has the highest value for each example
    guess_indexes = np.argmax(ai_output, keepdims = True, axis = 0)
    ai_true_guess = np.zeros((10, ai_output.shape[1]))
    ai_true_guess[guess_indexes.flatten(), np.arange(guess_indexes.shape[1])] = 1

    #Compare to true y-values
    num_equal_columns = np.sum(ai_true_guess == y_true, axis=0)

    #Count the number of columns where all elements are equal
    num_identical_columns = np.sum(num_equal_columns == ai_true_guess.shape[0])
    
    accuracy = (num_identical_columns / y_true.shape[1]) * 100

    #print("AI Accuracy: %.2f%%" % accuracy)
    
    return accuracy

def plotCost(costs, num_examples):
    x_values = np.arange(1, num_examples + 1)
    plt.plot(x_values, costs)
    plt.xlabel('Iteration')
    plt.ylabel('Cost')
    plt.title('Cost over time')

    plt.show()

#Main Method
if __name__ == "__main__":
    output_file = os.path.join(os.path.dirname(__file__), 'parameter_values.csv')
    #Prep the file
    with open(output_file, 'w') as f:
        f.write("{},{},{},{},{}\n".format("Learning Rate", "Momentum Constant", "Train Iterations", "Layer Dimemsions", "Accuracy"))
    
    for i in range(1):
        alpha_base = random.randint(2, 4)
        alpha_variance = random.randint(1, 9)
        alpha = (10 ** -(alpha_base)) * alpha_variance 
        
        if alpha_base == 2:
            train_iterations = 10_000
        if alpha_base == 3:
            train_iterations = 50_000
        if alpha_base == 4:
            train_iterations = 1_000_000
        
        beta_base = random.randint(0, 1)
        beta = random.random()
        beta = (beta * 0.25) + 0.75
        
        num_hidden_layers = random.randint(1, 4)
        start_point, stop_point = 128, 256
        
        layers = []
        for j in range(num_hidden_layers):
            layers.append(random.randint(start_point, stop_point))
            start_point = int(start_point * 0.5)
            stop_point = int(stop_point * 0.5)
            
        layers.append(10)
        
        print('Test {}. Alpha:{}, Beta:{}, Training Iterations:{}, Layers:{}'.format(i + 1, alpha, beta, train_iterations, layers))
        final_parameters = train_model(layer_dims = [175, 64, 10], learning_rate = 0.005, beta = 0.9, num_iterations = 150_000, doTrain = True)
        accuracy = test_model()
        print('Test {} accuracy: {}'.format(i + 1, accuracy))
        
        with open(output_file, 'a') as f:
            layers_string = ""
            for i in range(len(layers)):
                if i < len(layers) - 1:
                    layers_string += "{} ".format(layers[i])
                else:
                    layers_string += "{}".format(layers[i])
            f.write("{},{},{},{},{}\n".format(alpha, beta, train_iterations, layers_string, accuracy))
            