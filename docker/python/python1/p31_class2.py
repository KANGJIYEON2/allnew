class SmartPhone(object):
    def __init__(self, brand, details):
        self.brand = brand
        self.details = details
    def __str__(self):
        retrun f'str : {self.brand} - {self.details} '
    def __repr__(self):
        return f'repr : {self.brand} - smmartPhone, {self.details}'

    SmartPhone1 = SmartPhone('Iphone'{'color:':'While','price:10000'})
    SmartPhone2 = SmartPhone('Galaxy'{'color:':'Black','price:8000'})
    SmartPhone3 = SmartPhone('Blackberry'{'color:':'Sliver','price:6000'})

    print(SmartPhone)
    print(SmartPhone2__dict__)
    print(SmartPhone3dict__)

    print(id(SmartPhone1)
    print(id(SmartPhone2)
    print(id(SmartPhone3

print(SmartPhone1.brand == SmartPhone2.brand)
print(SmartPhone1 is SmartPhone2)

print(SmartPhone.__str__(SmartPhone1))
print(SmartOhinde.__repr__(SmartPhone2))
print(SmartPhone.__doc__)