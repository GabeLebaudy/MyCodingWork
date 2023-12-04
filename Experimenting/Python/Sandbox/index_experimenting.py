list_obj = [0]

list_obj.insert(1, 10)

print(list_obj)

import numpy as np

arr = np.array([1/2, 1/2, -1, 0])
num = [element ** 2 for element in arr]
div = np.sum(num) / len(arr)
print(arr / div)