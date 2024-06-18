from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.visualization import *
from numpy import pi
import numpy as np
import math
from qiskit_aer import Aer
from qiskit import transpile
import qiskit.quantum_info as qi
import random
from qiskit.circuit.library import SdgGate
import matplotlib.pyplot as plt
import QuditObj
import CEC

def OAM_Modulation(Qudit,Dit,Basis):
  if Basis == 0:
    #print("Basis 0")
    if Dit == 1:
      Qudit.circuit.x(0)
    if Dit == 2:
      Qudit.circuit.x(1)
    if Dit == 3:
      Qudit.circuit.x(0)
      Qudit.circuit.x(1)
  else:
     #print("Basis 1")
     if Dit == 0:
      #print("Entered 0")
      Qudit.circuit.h(0)
      Qudit.circuit.h(1)
     elif Dit == 1:
      #print("Entered 1")
      Qudit.circuit.x(1)
      Qudit.circuit.h(1)
      Qudit.circuit.h(0)
      Qudit.circuit.s(0)
     elif Dit == 2:
      #print("Entered 2")
      Qudit.circuit.x(0)
      Qudit.circuit.h(0)
      Qudit.circuit.h(1)
     elif Dit == 3:
      #print("Entered 3")
      Qudit.circuit.x(0)
      Qudit.circuit.h(0)
      Qudit.circuit.s(0)
      Qudit.circuit.x(1)
      Qudit.circuit.h(1)
  return Qudit

def OAM_ReciviengSinglePhoton(Qudit,Basis,Shot):
  csgate = SdgGate().control(1) # the parameter is the amount of control points you want
  if Basis == 1:
     #print("Measure Basis 1")
     Qudit.circuit.h(1)
     Qudit.circuit.append(csgate, [1, 0])
     Qudit.circuit.h(0)
     Qudit.circuit.cx(1,0)
     Qudit.circuit.cx(0,1)
     Qudit.circuit.cx(1,0)
  Qudit.measure()
  Qudit.run(Shot)
  #print(Qudit.Counts)
def OAM_Getdits(QList):
    output_string = ""
    for d in QList:
      key = list(d.keys())[0]  # Extract the key from the dictionary
      output_string += key
    return  output_string
def OAM_CrossTalk(Qudit,EP):
  EA = math.sqrt(EP) * 1j
  NEA = math.sqrt(1-EP)
  Gate = [[NEA,EA,0,0],
          [EA,NEA,0,0],
          [0,0,NEA,EA],
          [0,0,EA,NEA]]
  Qudit.CT(Gate)
def OAM_Turbulance(Qudit):
    pass
def OAM_Misallignment(Qudit):
    pass
def OAM_Divergence(Qudit):
    pass
def OAM_FreeSpace(Qudit):
    pass
def OAM_Fiber(Qudit):
    pass

def POL_Modulation(cir,bit,basis,theta_radians):
#This is gettingready but with Alligment error
  cir.ry(theta_radians,0)
  if bit == 1:
    cir.x(0)
  if basis == 1:
    cir.h(0)
  return cir
def POL_ReciviengSinglePhoton(Qubit,Basis,Shots):
    #print("Bob Basis is : ", BobBasis)
    if Basis == 1:
        #print("Bob Basis is +-45")
        Qubit.h(0)
    Qubit.barrier()
    Qubit.measure(0,0)
     # Use Aer's qasm_simulator
    simulator = Aer.get_backend('qasm_simulator')
    # Execute the circuit on the qasm simulator
    new_circuit = transpile(Qubit, simulator)
    job = simulator.run(new_circuit, shots = Shots)
    # Grab results from the job
    result = job.result()
    # Return counts
    counts = result.get_counts(Qubit)
    return counts
def POL_Getbits(QList):
    output_string = ""
    for d in QList:
      key = list(d.keys())[0]  # Extract the key from the dictionary
      output_string += key
    return  output_string
def SendQuantumOAMChannel(SendingList,EP,Base,EC):
  length = len(SendingList)
  EC = True
  if EC :
      Parity_added = convert_from_np_array(CEC.add_parity_bits(convert_to_np_array(SendingList),length),False)
  else:
      Parity_added = SendingList
  DitSequence = map_bits_to_numbers(Parity_added)
  length2 = len(Parity_added)
  ListofCounts = []
  for dit in DitSequence:
    Qudit = QuditObj.QuditCircuit(4,1)
    Qudit = OAM_Modulation(Qudit,dit,Base)
    OAM_CrossTalk(Qudit,EP)
    OAM_ReciviengSinglePhoton(Qudit,Base,Shot=1)
    ListofCounts.append(Qudit.Counts2)
  RDits = OAM_Getdits(ListofCounts)
  RBits = map_numbers_to_bits(RDits,length2)
  if EC:
    CorrectedBits = convert_from_np_array(CEC.EC_with_parity(convert_to_np_array(RBits),length),False)
  else:
    CorrectedBits = RBits
    CorrectedBits = [int(num) for num in CorrectedBits]
  return CorrectedBits
def convert_to_np_array(data):
    """
    Converts a list or string of numbers into a numpy array of integers.

    Parameters:
    data (list or str): Input list or string of numbers.

    Returns:
    np.ndarray: Numpy array of integers from the input data.
    """
    if isinstance(data, str):
        data = [int(num) for num in data]
    elif isinstance(data, list):
        data = np.array(data, dtype=int)
    else:
        raise ValueError("Input must be a list or a string of numbers")
    return np.array(data, dtype=int)

def convert_from_np_array(np_array, to_string):
    """
    Converts a numpy array into a list or a string.

    Parameters:
    np_array (np.ndarray): Input numpy array.
    to_string (bool): If True, convert to string; if False, convert to list.

    Returns:
    list or str: Converted list or string from the numpy array.
    """
    if not isinstance(np_array, np.ndarray):
        raise ValueError("Input must be a numpy array")

    if to_string:
        return ''.join(map(str, np_array))
    else:
        return np_array.tolist()
def map_bits_to_numbers(bit_list):
    # Work on a copy of the input list to avoid modifying the original list
    modified_bit_list = bit_list.copy()
    # Ensure the list length is even by appending a 0 if necessary
    if len(modified_bit_list) % 2 != 0:
        modified_bit_list.append(0)

    # Map pairs of bits to numbers
    number_list = []
    for i in range(0, len(modified_bit_list), 2):
        pair = modified_bit_list[i:i+2]
        number = pair[0] * 2 + pair[1]
        number_list.append(number)
    return number_list # Return the original length as well

def map_numbers_to_bits(number_string, original_length):
    bit_string = ""
    for char in number_string:
        num = int(char)
        bits = f"{num:02b}"  # Convert number to its 2-bit binary representation
        bit_string += bits

    # If the original bit list length was odd, remove the last bit

    if original_length % 2 != 0:
        bit_string = bit_string[:-1]