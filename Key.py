'''
File with Key class
'''
from prime_number import PrimeNumber
class Key:
    '''
    Class reprezents RSA key.
    '''
    def __init__(self,key_size_in_bytes):
        self.key_size_in_bytes = key_size_in_bytes
        self.prime_one = PrimeNumber.generate(key_size_in_bytes/2)
        self.prime_two = PrimeNumber.generate(key_size_in_bytes/2)
        self.key_modulus = self.prime_one * self.prime_two
        self.totient = (self.prime_one-1)*(self.prime_two-1)
        self.encryption_exponent = self.find_encryption_exponent()
        self.decryption_exponent = self.find_decryption_exponent()
        self.public = (self.encryption_exponent,self.key_modulus)
        self.private = (self.decryption_exponent, self.key_modulus)

    def find_encryption_exponent(self):
        '''
        Method finds encryption exponent.
        '''
        if self.totient >65537:
            return 65537
        exponent = self.totient-1
        while True:
            if PrimeNumber.is_prime(exponent):
                return exponent
            exponent = exponent-1

    def find_decryption_exponent(self):
        '''
        Method finds decryption exponent.
        '''
        u1, u2, u3 = 1, 0, self.encryption_exponent
        v1, v2, v3 = 0, 1, self.totient
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % self.totient
