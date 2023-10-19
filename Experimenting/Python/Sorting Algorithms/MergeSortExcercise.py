#This file will be used for the merge sort algorithm exercise

#Merge Two Sorted Lists
def mergeSortedArr(a, b, arr, key, flag):
    sortedList = []
    i = j = 0
    k = 0

    while i < len(a) and j < len(b):
        if not flag:
            if a[i][key] <= b[j][key]:
                arr[k] = a[i]
                i += 1
            else:
                arr[k] = b[j]
                j += 1
        else:
            if a[i][key] >= b[j][key]:
                arr[k] = a[i]
                i += 1
            else:
                arr[k] = b[j]
                j += 1

        k += 1
    
    while i < len(a):
        arr[k] = a[i]
        i += 1
        k += 1

    while j < len(b):
        arr[k] = b[j]
        j += 1
        k += 1
    

#Merge Sort Algorithm
def mergeSort(items, key, flag=False):
    if len(items) <= 1:
        return 
    
    mid = len(items) // 2

    left = items[:mid]
    right = items[mid:]

    mergeSort(left, key, flag)
    mergeSort(right, key, flag)

    mergeSortedArr(left, right, items, key, flag)

#Main Method
if __name__ == "__main__":
    elements = [
        {'name': 'rajab', 'age': 12, 'time_hours': 3},
        {'name': 'vignesh', 'age': 21, 'time_hours': 2.5},
        {'name': 'chinmay', 'age': 24, 'time_hours': 1.5},
        {'name': 'vedanth', 'age': 17, 'time_hours': 1},
    ]
    
    mergeSort(elements, 'name')
    print(elements)

