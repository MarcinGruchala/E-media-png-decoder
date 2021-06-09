from PrimeNumber import PrimeNumber


class Key:
    def __init__(self):
        self.size = 1024
        self.primeNumber = PrimeNumber()
        self.p = self.primeNumber.generate()
        self.q = self.primeNumber.generate()
        self.n = self.p * self.q
        self.totient = (self.p-1)*(self.q-1)
        self.e = self.totient-1
        self.d = self.find_d()
        self.publicKey = (self.e,self.n)
        self.privateKey = (self.d, self.n)

    def find_d(self):
        u1, u2, u3 = 1, 0, self.e
        v1, v2, v3 = 0, 1, self.totient
        while v3 != 0:
            q = u3 // v3 
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % self.totient

    

    