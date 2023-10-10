#This file is an exercise from the data structures tutorial I am following online using arrays

if __name__ == "__main__":
    #--Question 1
    expenses = [2200, 2350, 2600, 2130, 2190]

    # a.
    print("In February, $%d more was spent than in January." % (expenses[1] - expenses[0]))
    
    # b.
    print("The total expenses from the first quarter are $%d." % sum(expenses[0:3]) )

    # c.
    isExact = False
    for i in range(len(expenses)):
        if expenses[i] == 2000:
            isExact = True

    if isExact:
        print("Exactly $2000 was spent at least once.")
    else:
        print("Exactly $2000 was never spent in any month.")

    # d.
    expenses.append(1980)
    print("The June monthly expenses were $%d" % expenses[5])

    # e.
    expenses[3] = expenses[3] - 200
    print("An Item bought for $200 in April was returned. The new expenses for April is $%d." % expenses[3])

    #--Question 2
    heroes=['spider man','thor','hulk','iron man','captain america']

    # a.
    print("The length of the list is %d items long." % len(heroes))

    # b.
    heroes.append('Black Panther')
    
    # c.
    heroes.remove('Black Panther')
    heroes.insert(3, 'Black Panther')
    print(heroes)

    # d.
    heroes[1:3] = ['Doctor Strange']
    print(heroes)

    # e.
    heroes.sort()
    print(heroes)

    #--Question 3
    maxNumber = int(input("Enter a max integer to generate values for: "))

    oddNumbers = []
    for i in range(0, maxNumber, 2):
        oddNumbers.append(i + 1)

    print(oddNumbers)






