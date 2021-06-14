'''
File with PrimeNumber class.
'''
import random

class PrimeNumber:
    '''
    Class generates prime numbers and checks if the number is a prime number.
    '''
    @staticmethod
    def generate(number_size_in_bits):
        '''
        Method generates a prime number within given bits length.
        For better performance method generates only odd numbers.

        '''
        while True:
            number = random.randrange(2**(number_size_in_bits-1)+1,2**number_size_in_bits-1)
            if PrimeNumber.is_prime(number):
                return number

    @staticmethod
    def is_prime(number):
        '''
        Method checks if the number is prime using the Miller-Rabin primality test.
        If method returns true, the given number probably is a prime number.
        '''
        small_not_prime_numbers = [0,1,4,6,8,9]
        small_prime_numbers = [2,3,5,7]

        if number!=int(number):
            return False
        number=int(number)
        if number in small_not_prime_numbers:
            return False

        if number in small_prime_numbers:
            return True
        s = 0
        d = number-1
        while d%2==0:
            d>>=1
            s+=1
        assert(2**s * d == number-1)

        def trial_composite(a):
            if pow(a, d, number) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, number) == number-1:
                    return False
            return True

        for _ in range(8):
            a = random.randrange(2, number)
            if trial_composite(a):
                return False

        return True
