#This file will be used to demonstrate the quick sort algorithm

#Swap two elements
def swap(a, b, arr):
    arr[a], arr[b] = arr[b], arr[a]

#Partition Function
def partition(elements, start, end):
    pivotInd = start
    pivot = elements[pivotInd]

    start = pivotInd + 1
    end = len(elements) - 1
    while start < end:
        while elements[start] <= pivot:
            start += 1

        while elements[end] > pivot:
            end -= 1

        if start < end:
            swap(start, end, elements)

    swap(pivotInd, end, elements)

    return end

#Sorting Algorithm
def quickSort(elements, start, end):
    if start < end:
        pi = partition(elements, start, end)

        quickSort(elements, start, pi -1) #Left Partition
        quickSort(elements, pi + 1, end) #Right Partition

#Main Method
if __name__ == "__main__":
    elements = [11, 9, 20, 7, 2, 15, 28, 4, 30]
    
    quickSort(elements, 0, len(elements) - 1)
    print(elements)