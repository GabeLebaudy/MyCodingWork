#This file will be used for the bubble sort exercise

#Sorting Algorithm
def bubbleSort(elements, key='name'):
    size = len(elements)
    
    for i in range(size - 1):
        count = False
        for i in range(size - 1 - i):
            if elements[i][key] > elements[i + 1][key]:
                tmp = elements [i]
                elements[i] = elements[i + 1]
                elements[i + 1] = tmp
                count = True
        if not count:
            break

#Main Method
if __name__ == "__main__":
    elements = [
        { 'name': 'mona',   'transaction_amount': 1000, 'device': 'iphone-10'},
        { 'name': 'dhaval', 'transaction_amount': 400,  'device': 'google pixel'},
        { 'name': 'kathy',  'transaction_amount': 200,  'device': 'vivo'},
        { 'name': 'aamir',  'transaction_amount': 800,  'device': 'iphone-8'},
    ]

    bubbleSort(elements, key='device')
    print(elements)

