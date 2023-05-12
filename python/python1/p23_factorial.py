def factorial(n):
    in n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


n = input("Input number : ")
print("{} factorial is {}".format(n, factorial(int(n))))