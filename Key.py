from PrimeNumber import PrimeNumber


from PrimeNumber import PrimeNumber

class Key:
    def __init__(self):
        self.size = 1024
        primeNumber = PrimeNumber()
        self.p = primeNumber.generate()
        self.q = primeNumber.generate()
        self.n = self.p *self.q