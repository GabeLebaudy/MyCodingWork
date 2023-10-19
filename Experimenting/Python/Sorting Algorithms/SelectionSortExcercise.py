#This file will be used for the selection sort algorithm exercise

#Selection sort
def selectionSort(items, preferences):
    for i in range(len(items)):
        minIndex = i
        for j in range(minIndex + 1, len(items)):
            prefCounter = 0
            while items[j][preferences[prefCounter]] == items[minIndex][preferences[prefCounter]]:
                prefCounter += 1
            
            if items[j][preferences[prefCounter]] < items[minIndex][preferences[prefCounter]]:
                minIndex = j
            
        if i != minIndex:
            items[i], items[minIndex] = items[minIndex], items[i]

#Main Method
if __name__ == "__main__":
    elements = [
        {'First Name': 'Raj', 'Last Name': 'Nayyar'},
        {'First Name': 'Suraj', 'Last Name': 'Sharma'},
        {'First Name': 'Karan', 'Last Name': 'Kumar'},
        {'First Name': 'Jade', 'Last Name': 'Canary'},
        {'First Name': 'Raj', 'Last Name': 'Thakur'},
        {'First Name': 'Raj', 'Last Name': 'Sharma'},
        {'First Name': 'Kiran', 'Last Name': 'Kamla'},
        {'First Name': 'Armaan', 'Last Name': 'Kumar'},
        {'First Name': 'Jaya', 'Last Name': 'Sharma'},
        {'First Name': 'Ingrid', 'Last Name': 'Galore'},
        {'First Name': 'Jaya', 'Last Name': 'Seth'},
        {'First Name': 'Armaan', 'Last Name': 'Dadra'},
        {'First Name': 'Ingrid', 'Last Name': 'Maverick'},
        {'First Name': 'Aahana', 'Last Name': 'Arora'}
    ]
    selectionSort(elements, ['First Name', 'Last Name'])
    print(elements)
