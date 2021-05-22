def sum(a, b):
    return a + b

def avg(a, b):
    return (a + b)/2

def armstrong(n):
    # n = int(input("Enter the number "))
    sum = 0 
    order = len(str(n))
    copy_n = n
    
    while(n > 0):
        d = n%10
        sum += d ** order
        n /= 10
    if copy_n == sum:
        print(f"{copy_n} is an armstrong number")
    else:
        print(f"{copy_n} is not an armstrong number")