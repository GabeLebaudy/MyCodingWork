#This file will be used to demonstrate the selection sort algorithm

#Find Minimum Element (Not used but shows part of selection short)
def findMin(arr):
    min = arr[-1]
    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i] 

    return min

#Selection sort
def selectionSort(items):
    for i in range(len(items)):
        minIndex = i
        for j in range(minIndex + 1, len(items)):
            if items[j] < items[minIndex]:
                minIndex = j

        if i != minIndex:
            items[i], items[minIndex] = items[minIndex], items[i]

#Main Method
if __name__ == "__main__":
    elements = [78, 12, 15, 8, 2, 61, 53, 23, 27]
    selectionSort(elements)
    print(elements)