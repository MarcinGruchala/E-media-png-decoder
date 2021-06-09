from PrimeNumber import PrimeNumber


class Key:
    def __init__(self):
        self.size = 1024
        self.primeNumber = PrimeNumber()
        self.p = self.primeNumber.generate()
        self.q = self.primeNumber.generate()
        self.totient = (self.p-1)*(self.q-1)
        self.e = self.totient-1
    