#This file will be used to demonstrate recursion(Just following video course)

#Find Sum Function
def findSum(n):
    if n == 1:
        return 1
    
    return n + findSum(n - 1)

#Fibonnaci Sequence
def fib(n):
    if n == 0 or n == 1:
        return n
    
    return n + fib(n - 1) + fib(n - 2)

#Main Method
if __name__ == "__main__":
    print(findSum(6))
    print(fib(6))
    print(fib(4))