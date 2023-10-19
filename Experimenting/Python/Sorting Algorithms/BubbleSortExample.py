#This file will be used to demonstrate the bubble sort algorithm

def bubbleSort(elements):
    size = len(elements)

    for i in range(size - 1):
        count = False
        for i in range(size - 1 - i):
            if elements[i] > elements[i + 1]:
                tmp = elements [i]
                elements[i] = elements[i + 1]
                elements[i + 1] = tmp
                count = True
        if not count:
            break

#Main Method
if __name__ == "__main__":
    elements = [5, 9, 2, 1, 67, 34, 88, 34]

    bubbleSort(elements)
    print(elements)