#This file will be used to demonstrate the binary search algorithm

#Linear Search
def linearSearch(numberList, number):
    for index, element in enumerate(numberList):
        if element == number:
            return index
        
    return -1


#Binary Search
def binarySearch(numberList, numberToFind):
    leftInd = 0
    rightInd = len(numberList) - 1
    midIndex = 0

    while leftInd <= rightInd:
        midIndex = (leftInd + rightInd) // 2
        midNumber = numberList[midIndex]

        if midNumber == number:
            return midIndex
        
        if midNumber < number:
            leftInd = midIndex + 1
        else:
            rightInd = midIndex - 1

    return -1

#Recursive Binary Search
def recBinSearch(numberList, num, leftInd, rightInd):
    if leftInd > rightInd:
        return -1
    
    midInd = (leftInd + rightInd) // 2
    if midInd >= len(numberList) or midInd < 0:
        return -1
    
    midNum = numberList[midInd]

    if midNum == num:
        return midInd
    
    if midNum < number:
        leftInd = midInd + 1
    else:
        rightInd = midInd - 1

    return recBinSearch(numberList, num, leftInd, rightInd)


#Main Method
if __name__ == "__main__":
    numbers = [12, 15, 17, 19, 21, 24, 45, 67]
    number = 21

    index = linearSearch(numbers, number)
    print(index)
    print('---')

    secondIndex = binarySearch(numbers, number)
    print(secondIndex)
    print('---')

    thirdIndex = recBinSearch(numbers, number, 0, len(numbers))
    print(thirdIndex)
