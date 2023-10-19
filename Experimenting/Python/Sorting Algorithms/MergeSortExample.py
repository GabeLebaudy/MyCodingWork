#This file will be used to showcase the merge sort algorithm


#Merge Two Sorted Lists
def mergeSortedArr(a, b, arr):
    sortedList = []
    lengthA = len(a)
    lengthB = len(b)
    i = j = 0
    k = 0

    while i < lengthA and j < lengthB:
        if a[i] <= b[j]:
            arr[k] = a[i]
            i += 1
            k += 1
        else:
            arr[k] = b[j]
            j += 1
            k += 1
    
    while i < lengthA:
        arr[k] = a[i]
        i += 1
        k += 1

    while j < lengthB:
        arr[k] = b[j]
        j += 1
        k += 1
    

#Merge Sort Algorithm
def mergeSort(items):
    if len(items) <= 1:
        return 
    
    mid = len(items) // 2

    left = items[:mid]
    right = items[mid:]

    mergeSort(left)
    mergeSort(right)

    mergeSortedArr(left, right, items)

#Main Method
if __name__ == "__main__":
    array = [10, 3, 15, 7, 8, 23, 98, 29]
    mergeSort(array)
    print(array)
