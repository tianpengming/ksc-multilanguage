def IsUgly(number):
    while number%2 == 0:
        number = number/2
    while number%3 == 0:
        number = number/3
    while number%5 == 0:
        number = number/5
    if number == 1:
        return 1
    else:
        return 0
def GetUglyNumber(index):
    if index <= 0:
        return 0
    number = 1
    count = 0
    while count < index:
        count = count + IsUgly(number)
        number = number + 1
    return number
a = GetUglyNumber(100)
print(a)