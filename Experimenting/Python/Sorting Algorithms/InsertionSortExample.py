#This file will be used to demonstrate the insertion sorting algorithm

#Insertion Sort Method
def insertionSort(items):
    for i in range(1, len(items)): #Items [9, 11, 29, 7, 2, 15, 28, 29] i = 3
        anchor = items[i] #Anchor = 7
        j = i-1 #J = 2

        while j >= 0 and anchor < items[j]: #items[j] = 11
            items[j + 1] = items[j] #Items = [9, 11, 11, 29, 2, 15, 28, 28]
            j = j - 1 #J = 0

        items[j + 1] = anchor

#Main method
if __name__ == "__main__":
    elements = [11, 9, 29, 7, 2, 15, 28]
    insertionSort(elements)
    print(elements)