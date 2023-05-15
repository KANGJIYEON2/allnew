class Calculate(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def add(self):
        result = self.first + self.second
        return 'add result : %d' % result

    def sub(self):
        result = self.first - self.second
        return 'sub result : %d' % result

    def mul(self):
        result = self.first * self.second
        return 'multiply : %d' % result

    def div(self):
        if self.second == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = self.first / self.second
        return 'div result : %.3f' % result


calc = Calculate(14, 0)

print(calc.add())
print(calc.sub())
print(calc.mul())
print(calc.div())
