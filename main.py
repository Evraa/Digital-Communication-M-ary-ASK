import math
import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc


def generateRandomProcess(elementCount):
    '''
    This function returns random process of streaming bits 0 an 1.

    eg. [1, 0, 0, 1,....]
    and we know for sure that the main function is checking that the elementCount
    is divisible by 3
    '''
    XofT = []
    for _ in range(elementCount):
        XofT.append(math.floor(0.5 + random.uniform(0, 1)))
    return XofT


def generateTimeSteps(elementCount, width):
    '''
    This function returns time steps
    '''
    return np.linspace(0, elementCount, elementCount, endpoint=False)

def AWGN(length, mean_noise, variance):
    '''
    Generate AWGN with SNR = 1/Eb_No[0] and SNR = 1/Eb_N0[n] to show the difference.

    Generate noise samples
    '''
    return np.random.normal(mean_noise, np.sqrt(variance), length)


def mapper():
    '''
        Here you can find the Mapper Code and Logic

        Since M = 3 and Eb = 1, then E0 = 1/7

        Logic:
            Simply reading an input from the user count of bits
            Making sure its divisible by three
            Generating random bits of that size
            Returns M-ary of size bits.size/3

        Returns:
            Bits: the randomly generated bits
            Mapped: the mapped M-ary values
    '''
    E0 = 1/7
    elemCount = 1
    while elemCount%3 != 0:
        elemCount = int(input("Please enter the desired count of elements, and make sure it is divisible by 3: "))

    Bits = generateRandomProcess (elemCount)
   
    Symbols = [-7,-5,-3,-1,1,3,5,7]
    Symbols = [i * math.sqrt(E0) for i in Symbols]

    stack_of_elements = []
    for i in range (0,elemCount, 3):
        stack_of_elements.clear()
        stack_of_elements.append(Bits[i])
        stack_of_elements.append(Bits[i+1])
        stack_of_elements.append(Bits[i+2])




if __name__ == "__main__":
    mapper()
    ###VARIABLES###
    Eb_No_dB_Min = -4  # min E/No alowed in db
    Eb_No_dB_Max = 16  # max E/No alowed in db
    '''
        Eb_No_dB: Array of values from Eb_No_dB_Min to Eb_No_dB_Max
        with step_size = 2

        To plot the vertical access for BER and Theoritical BER (Pe)
    '''
    Eb_No_dB = np.arange(start=Eb_No_dB_Min, stop=Eb_No_dB_Max+1, step=2)
    
    # Linearize Eb/N0
    '''
        Liniarizing Eb/No inorder to get the Variance of AWGN at this point
    '''
    Eb_No = 10**(Eb_No_dB/10.0)
    Pe = []  # Probability of error
    BER = []  # Bit error rate
    count = 300  # no of tests/time steps


