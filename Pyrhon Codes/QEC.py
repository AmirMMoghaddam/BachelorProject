#These functions are used for Quantum Error Corections Using Shor Alghorithm 
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import *
from numpy import pi
import numpy as np
import math
from qiskit_aer import Aer
from qiskit import transpile
import qiskit.quantum_info as qi
import random



# --- All Noise Related Functions ---
def generate_random_angle():
    # Generate a random number from a Gaussian distribution
    # Parameters
    mu = 0  # Mean of the Gaussian distribution
    sigma = 0.15 # Standard deviation of the Gaussian distribution
    while True:
        angle = np.random.normal(mu, sigma)
        if -np.pi <= angle <= np.pi:
            break
    return angle
def generate_custom_random():
    # Define the probabilities for each number
    probabilities = [1/25**i for i in range(1, 9)]

    # Normalize probabilities to sum to 1
    probabilities = [p / sum(probabilities) for p in probabilities]

    # Generate a random integer using the defined probabilities
    return np.random.choice(np.arange(1, 9), p=probabilities)
def TarqetNoise(number):
  if number == 1:
    return [8];
  elif number == 2:
    return [8,3]
  else:
    return [8,0,3]
def BitNoise(cir):
    for i in TarqetNoise(generate_custom_random()):
      cir.rx(np.radians(10),i)
    return cir
def PhaseNoise(cir):
    for i in TarqetNoise(generate_custom_random()):
      cir.rz(np.radians(10),i)
    return cir
#This function uses one Logical qubit to encode 8 other qubits so that we can use it for bit and phase flip encoding
def Encoding(cir):
    # Phase- flip
    cir.cx(8,5)
    cir.cx(8,2)
    cir.h(2)
    cir.h(5)
    cir.h(8)
    #Bit-flip
    cir.cx(8,6)
    cir.cx(8,7)
    cir.cx(5,3)
    cir.cx(5,4)
    cir.cx(2,0)
    cir.cx(2,1)
    return cir
#This function Decodes the qubits so it can be used again
def Decoding(cir):
    #Bit-flip
    cir.cx(8,6)
    cir.cx(8,7)
    cir.cx(5,3)
    cir.cx(5,4)
    cir.cx(2,0)
    cir.cx(2,1)
    #Phase-flip
    cir.h(2)
    cir.h(5)
    cir.h(8)
    cir.cx(8,5)
    cir.cx(8,2)
    return cir
#Its time for bit flip for that we use a parity check function
def BitParityCheck(cir,SQubit,AuxQubit):
    cir.cx(SQubit,AuxQubit)
    cir.cx(SQubit+1,AuxQubit)
    cir.cx(SQubit+1,AuxQubit+1)
    cir.cx(SQubit+2,AuxQubit+1)
    return cir
#And We need a CorrectionBlock
def BitCorrectionBlock(cir,SQubit,AuxQubit):
    cir.x(AuxQubit)
    cir.ccx(AuxQubit+1,AuxQubit,SQubit+2)
    cir.x(AuxQubit)
    cir.ccx(AuxQubit+1,AuxQubit,SQubit+1)
    cir.x(AuxQubit+1)
    cir.ccx(AuxQubit+1,AuxQubit,SQubit)
    cir.x(AuxQubit+1)
    cir.measure(AuxQubit,AuxQubit)
    cir.measure(AuxQubit+1,AuxQubit+1)
    cir.reset(AuxQubit)
    cir.reset(AuxQubit+1)
    return cir
#Now bringing it all toghether we construct the Error Correction function
def BitErrorCorrection(cir,AuxQubit):
    for i in range(3):
        cir = BitParityCheck(cir,i*3,AuxQubit)
        cir.barrier()
        cir = BitCorrectionBlock(cir,i*3,AuxQubit)
    return cir
def PhaseParityCheck(cir,AuxQubit):
    #Storing the data in Q8,5,2
    cir.cx(8,6)
    cir.cx(8,7)
    cir.cx(5,3)
    cir.cx(5,4)
    cir.cx(2,0)
    cir.cx(2,1)
    cir.h(2)
    cir.h(5)
    cir.h(8)
    #Getting the parity stored in the Aux Qubits
    cir.cx(2,AuxQubit)
    cir.cx(5,AuxQubit)
    cir.cx(5,AuxQubit+1)
    cir.cx(8,AuxQubit+1)
    #restoring the Encoded Form
    cir.h(2)
    cir.h(5)
    cir.h(8)
    cir.cx(8,6)
    cir.cx(8,7)
    cir.cx(5,3)
    cir.cx(5,4)
    cir.cx(2,0)
    cir.cx(2,1)
    return cir
def PhaseCorrectionBlock(cir,AuxQubit):
    cir.x(AuxQubit)
    cir.ccz(AuxQubit+1,AuxQubit,8)
    cir.x(AuxQubit)
    cir.ccz(AuxQubit+1,AuxQubit,5)
    cir.x(AuxQubit+1)
    cir.ccz(AuxQubit+1,AuxQubit,2)
    cir.x(AuxQubit+1)
    cir.measure(AuxQubit,AuxQubit)
    cir.measure(AuxQubit+1,AuxQubit+1)
    cir.reset(AuxQubit)
    cir.reset(AuxQubit+1)
    return cir
def PhaseErrorCorrection(cir,AuxQubit):
    cir = PhaseParityCheck(cir,AuxQubit)
    cir.barrier()
    cir = PhaseCorrectionBlock(cir,AuxQubit)
    return cir