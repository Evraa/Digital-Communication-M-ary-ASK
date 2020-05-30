import math
import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfc


def generateRandomProcess(elementCount):
    '''
    This function returns random process of streaming bits 0 an 1.

    eg. [1, 0, 0, 1,....]
    and we know for sure that the main
    function is checking that the elementCount
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


def mapper():
    '''
        Function:
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
        elemCount = int(input("Please enter the desired count of elements,\
            and make sure it is divisible by 3: "))

    Bits = generateRandomProcess (elemCount)
   
    Symbols = [-7,-5,-3,-1,1,3,5,7]
    Symbols = [i * math.sqrt(E0) for i in Symbols]

    Bits_to_Symbols = []
    for i in range (0,elemCount, 3):
        stack_of_elements = ""
        stack_of_elements += str(Bits[i])
        stack_of_elements += str(Bits[i+1])
        stack_of_elements += str(Bits[i+2])

        if stack_of_elements == "000":
            Bits_to_Symbols.append([Symbols[4]])
        elif stack_of_elements == "001":
            Bits_to_Symbols.append([Symbols[5]])
        elif stack_of_elements == "010":
            Bits_to_Symbols.append([Symbols[7]])
        elif stack_of_elements == "011":
            Bits_to_Symbols.append([Symbols[6]])
        elif stack_of_elements == "100":
            Bits_to_Symbols.append([Symbols[3]])
        elif stack_of_elements == "101":
            Bits_to_Symbols.append([Symbols[2]])
        elif stack_of_elements == "110":
            Bits_to_Symbols.append([Symbols[0]])
        elif stack_of_elements == "111":
            Bits_to_Symbols.append([Symbols[1]])
        else:
            print ("error occured in mapping")
    return Bits, Bits_to_Symbols, elemCount


def Channel (mean, variance, length):
    '''
    Function:
        This Function is responsible for simulating the AWGN channel effect
        of adding random noise to the 
    transmitted signal.

    Inputs:
        mean: the mean of awgn channel
        variance: the varinace of awgn channel
        length: Length of the time steps
    Outputs:
        generated random noise
    '''
    return math.sqrt(variance/2)*np.random.randn(length)
    # return np.random.normal(mean, np.sqrt(variance), length)


def DeMapper(Noisy_Bits_to_Symbols):
    '''
    Function:
        Demap/Decode the symbols into their actual bits

    Inputs:
        Noisy_Bits_to_Symbols: Symbols representing the bits added to noise

    Output:
        Received_Bits: The mapped bits
    '''
    Received_Bits = []
    E0 = 1/7
    Symbols_boundry = [-6,-4,-2,0,2,4,6]
    Symbols_boundry = [i * math.sqrt(E0) for i in Symbols_boundry]

    for symbole in Noisy_Bits_to_Symbols:
        if symbole <= Symbols_boundry[0]:
            Received_Bits.append(1)
            Received_Bits.append(1)
            Received_Bits.append(0)
        elif symbole > Symbols_boundry[0] and symbole <= Symbols_boundry[1]:
            Received_Bits.append(1)
            Received_Bits.append(1)
            Received_Bits.append(1)
        elif symbole > Symbols_boundry[1] and symbole <= Symbols_boundry[2]:
            Received_Bits.append(1)
            Received_Bits.append(0)
            Received_Bits.append(1)
        elif symbole > Symbols_boundry[2] and symbole <= Symbols_boundry[3]:
            Received_Bits.append(1)
            Received_Bits.append(0)
            Received_Bits.append(0)
        elif symbole > Symbols_boundry[3] and symbole <= Symbols_boundry[4]:
            Received_Bits.append(0)
            Received_Bits.append(0)
            Received_Bits.append(0)
        elif symbole > Symbols_boundry[4] and symbole <= Symbols_boundry[5]:
            Received_Bits.append(0)
            Received_Bits.append(0)
            Received_Bits.append(1)
        elif symbole > Symbols_boundry[5] and symbole <= Symbols_boundry[6]:
            Received_Bits.append(0)
            Received_Bits.append(1)
            Received_Bits.append(1)
        elif symbole > Symbols_boundry[6]:
            Received_Bits.append(0)
            Received_Bits.append(1)
            Received_Bits.append(0)
        else:
            print("error occured in Demapping")
        
    return Received_Bits
    
def BER (Bits, Received_Bits):
    '''
    Function:
        Calculate the BER for each bit sent

    Inputs:
        Bits: The actual transmitted bits
        Received_Bits: The received bits

    Output:
        actual_ber: the sum of all errors occurred
    '''
    error = 0
    #Converting them to ndarray
    for i in range (len(Received_Bits)):
        if (Bits[i] != Received_Bits[i]):
            error += 1
    
    return error/len(Received_Bits)


if __name__ == "__main__":
    ###VARIABLES###
    Eb_No_dB_Min = -4  # min E/No alowed in db
    Eb_No_dB_Max = 16  # max E/No alowed in db
    '''
        Eb_No_dB: Array of values from Eb_No_dB_Min to Eb_No_dB_Max
        with step_size = 2

        To plot(simulate) the vertical access for BER and Theoritical BER (Pe)
    '''
    Eb_No_dB = np.arange(start=Eb_No_dB_Min, stop=Eb_No_dB_Max+1, step=2)
    
    # Linearize Eb/N0
    '''
        Liniarizing Eb/No in order to get the Variance of AWGN at this point
    '''
    Eb_No = 10**(Eb_No_dB/10.0)

    #Theoritcal and Actual Errors:
    #Bit error rates of different Eb/N0
    BERs = []
    #Probability of errors of different Eb/N0
    PEs = []
    #1- Mapper is always the same as E0 = 1/7 all the time
    Bits, Bits_to_Symbols, length = mapper()

    mean = 0
    for E_N0 in Eb_No:
        #2- Channel
        # variance = math.sqrt((1/E_N0)/2)
        variance = (1/E_N0)
        #length//3 ==> floor(length/3)
        Noise = Channel(mean, variance, length//3)
        #Adding the noise to Symbolic Bits ELEMENT WISE
        Noisy_Bits_to_Symbols = []
        for i in range (len(Bits_to_Symbols)):
            Noisy_Bits_to_Symbols.append(Bits_to_Symbols[i] + Noise[i])
        
        #3- Demapping
        Received_Bits = DeMapper(Noisy_Bits_to_Symbols)

        #4- BER
        actual_ber =  BER(Bits, Received_Bits)
        BERs.append(actual_ber)
        PEs.append( (7/8)* (erfc(math.sqrt(E_N0/7))) *(1/3))

    #Plotting1/3)
    plt.rcParams["figure.figsize"] = (20,20)
    plt.rcParams.update({'font.size': 35})
    
    plt.semilogy(Eb_No_dB, PEs,linestyle = 'solid',linewidth=4)
    plt.semilogy(Eb_No_dB, BERs,linestyle = 'dashed',linewidth=4)
    plt.grid(True)
    plt.legend(('theoritical','simulation'))    
    plt.xlabel('Eb/No (dB)')
    plt.ylabel('BER')
    plt.title("BER and Pe vs Eb/N0")
    # plt.show()
    plt.savefig("Figures/Figure_1")
    print ("figure is saved at Figures/Figure_1.png")