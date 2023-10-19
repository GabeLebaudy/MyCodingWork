#This file will be used to demonstrate the shell sort algorithm

#Shell Sort Algorithm
def shellSort(items):
    size = len(items)
    gap = size // 2
    while gap > 0:
        for i in range(gap, size):
            anchor = items[i]
            j = i
            while j >= gap and items[j-gap] > anchor:
                items[j] = items[j - gap]
                j -= gap
            
            items[j] = anchor
        gap = gap // 2
        

#Main Method
if __name__ == "__main__":
    elements = [21, 38, 29, 17, 4, 25, 11, 32, 9]
    shellSort(elements)
    print(elements)
