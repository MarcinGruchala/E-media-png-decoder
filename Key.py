'''
File with Key class
'''
from prime_number import PrimeNumber
class Key:
    '''
    Class reprezents RSA key
    '''
    def __init__(self,key_size_in_bytes):
        self.key_size_in_bytes = key_size_in_bytes
        self.p = PrimeNumber.generate(key_size_in_bytes/2)
        self.q = PrimeNumber.generate(key_size_in_bytes/2)
        self.n = self.p * self.q
        self.totient = (self.p-1)*(self.q-1)
        self.e = self.find_e()
        self.d = self.find_d()
        self.public = (self.e,self.n)
        self.private = (self.d, self.n)

    def find_e(self):
        '''
        '''
        e = self.totient-1
        while True:
            if PrimeNumber.is_prime(e):
                return e
            e = e-2

    def find_d(self):
        '''
        '''
        u1, u2, u3 = 1, 0, self.e
        v1, v2, v3 = 0, 1, self.totient
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % self.totient
