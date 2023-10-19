#This file will be used for the binary search algorithm 

#Recursive Binary Search
def findAllIndex(numberList, num, leftInd, rightInd):
    indexes = []

    if leftInd > rightInd:
        return -1
    
    midInd = (leftInd + rightInd) // 2
    if midInd >= len(numberList) or midInd < 0:
        return -1
    
    midNum = numberList[midInd]

    if midNum == num:
        #Check left side
        leftIndexes = findAllIndex(numberList, num, leftInd, midInd - 1)

        if leftIndexes != -1:
            indexes += leftIndexes
        
        #Add current index
        indexes += [midInd]

        #Check Right Side
        rightIndexes = findAllIndex(numberList, num, midInd + 1, rightInd)
        if rightIndexes != -1:
            indexes += rightIndexes
        
        return indexes
    
    if midNum < number:
        leftInd = midInd + 1
    else:
        rightInd = midInd - 1

    return findAllIndex(numberList, num, leftInd, rightInd)


#Main Method
if __name__ == "__main__":
    numbers = [1,4,6,9,11,15,15,15,15,15,17,21,34,34,56]
    number = 15

    indexes = findAllIndex(numbers, number, 0, len(numbers))
    print(indexes)
    