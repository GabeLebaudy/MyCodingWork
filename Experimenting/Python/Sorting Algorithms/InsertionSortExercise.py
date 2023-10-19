#This file will be used for the insertion sort exercise

#Insertion Sort Method
def insertionSort(items):
    for i in range(1, len(items)): #Items [2, 1, 5, 7, 2, 0, 5]
        #i is the length of the sorted array
        if i % 2 == 1:
            median = items[i // 2]
            print(median)

        if i % 2 == 0:
            median = (items[(i // 2) - 1] + items[i // 2]) / 2
            print(median)

        anchor = items[i] #Anchor = 1
        j = i-1 #J = 0

        while j >= 0 and anchor < items[j]: #items[j] = 2
            items[j + 1] = items[j] #Items = [2, 1, 5, 7, 2, 0, 5]
            j = j - 1 #J = -1

        items[j + 1] = anchor

    length = len(items)
    if length % 2 == 1:
            median = items[i // 2]
            print(median)

    if length % 2 == 0:
        median = (items[(i // 2) - 1] + items[i // 2]) / 2
        print(median)

#Main Method
if __name__ == "__main__":
    elements = [2, 1, 5, 7, 2, 0, 5]
    insertionSort(elements)
    print('-----\n')
    print(elements)