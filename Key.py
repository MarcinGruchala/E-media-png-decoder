from PrimeNumber import PrimeNumber


class Key:
    def __init__(self):
        self.size = 32
        self.p = PrimeNumber.generate()
        self.q = PrimeNumber.generate()
        self.n = self.p * self.q
        self.totient = (self.p-1)*(self.q-1)
        self.e = self.find_e()
        self.d = self.find_d()
        self.public = (self.e,self.n)
        self.private = (self.d, self.n)

    def find_e(self):
        e = self.totient-1
        while True:
            if PrimeNumber.isPrime(e):
                return e
            e = e-2
    
    def find_d(self):
        u1, u2, u3 = 1, 0, self.e
        v1, v2, v3 = 0, 1, self.totient
        while v3 != 0:
            q = u3 // v3 
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % self.totient

    

    