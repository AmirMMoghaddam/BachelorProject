#All the functions needed for 2 and 4 Dimensional QKD 
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
import QEC
import QuditObj
import QL
import CL

def AliceKeyGenerator(Dim,Bit,AliceBases,BobBases):
    if Dim > 2 :
      Dit = map_bits_to_numbers(Bit)
    Check_list = []
    length = len(Dit) if Dim > 2  else len(Bit)

    for i in range(length):
        if AliceBases[i] == BobBases[i]:
            appendble = Dit[i] if Dim > 2 else Bit[i]
            Check_list.append(appendble)
        Key = ''
    for item in Check_list:
        Key = Key + str(item)
    if Dim > 2:
      Key = map_numbers_to_bits(Key,len(Bit))
    return Key
def CheckSecurity(Key,Akey,Checklength):
    if Akey[-Checklength:] == Key[-Checklength:]:
        print("The Connection is Secure with the probability of:")
        print((1-((3/4)**Checklength))*100)
    else:
        print("The Connection is not Secure!")
def calculate_error_percentage(string1, string2):
    # Check if both strings are of the same length
    if len(string1) != len(string2):
        return '*'

    # Count the number of mismatched bits
    errors = sum(bit1 != bit2 for bit1, bit2 in zip(string1, string2))

    # Calculate the error percentage
    total_bits = len(string1)
    error_percentage = (errors / total_bits) * 100

    return error_percentage
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

    return bit_string
def generate_random_sequence(length):
    return [random.randint(0, 1) for _ in range(length)]
def statistic_calculator(results):
  count_stars = 0
  filtered_list = []
  
  for item in results:
      if item == '*':
          count_stars += 1
      else:
          filtered_list.append(item)
  sum = 0
  for Err in filtered_list:
    sum += Err
  return max(filtered_list) , min(filtered_list), sum/len(filtered_list), count_stars

def TwoD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,theta_radians,QChannel):
   SNR = 20
   EP = 0.0
   Base = 0
   if QChannel:
    RAliceBases = QL.SendQuantumOAMChannel(AliceBases,EP,Base,True)
   else:
    RAliceBases = CL.SendClassicalChannel(AliceBases,SNR,4,True)
   ListOfCounts = []
   EveListOfCounts = []
   if Eve==True:
    for i in range(length):
        Qubit = QuantumCircuit(1,1)
        #Getting that one photon with Alice's Basis ready to send
        Qubit = QL.POL_Modulation(Qubit,BitSequence[i],AliceBases[i],2*theta_radians)
        #Recive Single Photon
        counts = QL.POL_ReciviengSinglePhoton(Qubit,EveBases[i],Shots = 1)
        #Measure one Photon with Bob Basis
        EveListOfCounts.append(counts)
        del Qubit
    output_string = QL.POL_Getbits(EveListOfCounts)
    list_from_Key = [int(char) for char in output_string]
    ListOfCounts = []
    for i in range(length):
        Qubit = QuantumCircuit(1,1)
        #Getting that one photon with Alice's Basis ready to send
        Qubit = QL.POL_Modulation(Qubit,BitSequence[i],EveBases[i],2*theta_radians)
        #Recive Single Photon
        counts = QL.POL_ReciviengSinglePhoton(Qubit,BobBases[i],Shots = 1)
        #Measure one Photon with Bob Basis
        ListOfCounts.append(counts)
        del Qubit
    Check_list = []
    EveCheck_list = []
    for i in range(len(AliceBases)):
        if RAliceBases[i] == BobBases[i]:
            Check_list.append(ListOfCounts[i])
            EveCheck_list.append(EveListOfCounts[i])
    #print("The Bases checked list is : ",Check_list)
    output_string= QL.POL_Getbits(Check_list)
    Eveoutput_string= QL.POL_Getbits(EveCheck_list)
    return  output_string , Eveoutput_string
   else:
    for i in range(length):
        Qubit = QuantumCircuit(1,1)
        #Getting that one photon with Alice's Basis ready to send
        Qubit = QL.POL_Modulation(Qubit,BitSequence[i],AliceBases[i],2*theta_radians)
        #Recive Single Photon
        counts = QL.POL_ReciviengSinglePhoton(Qubit,BobBases[i],Shots = 1)
        #Measure one Photon with Bob Basis
        ListOfCounts.append(counts)
        del Qubit
    #Now Alice and Bob share their Bases
    #print("Raw List of count is : ",ListOfCounts)
    Check_list = []
    for i in range(len(AliceBases)):
        if RAliceBases[i] == BobBases[i]:
            Check_list.append(ListOfCounts[i])
    #print("The Bases checked list is : ",Check_list)
    output_string= QL.POL_Getbits(Check_list)
    return  output_string
def FourD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,CrossT,QChannel):
   SNR = 20
   EP = 0.0
   Base = 0
   if QChannel:
    RAliceBases = QL.SendQuantumOAMChannel(AliceBases,EP,Base,True)
   else:
    RAliceBases = CL.SendClassicalChannel(AliceBases,SNR,4,True)
   DitSequence = map_bits_to_numbers(BitSequence)
   #print(DitSequence)
   length2 = len(DitSequence)
   EveListOfCounts = []
   if Eve==True:
    for i in range(length2):
        #print("for bit number : ", i)
        Qudit = QuditObj.QuditCircuit(4,1)
        #Getting that one photon with Alice's Basis ready to send
        Qudit = QL.OAM_Modulation(Qudit,DitSequence[i],AliceBases[i])
        #circuit = GettingReady(circuit,BitSequence[i],AliceBases[i])
        #Sending Single photon
        QL.OAM_CrossTalk(Qudit,EP) if CrossT else None
        #Recive Single Photon
        QL.OAM_ReciviengSinglePhoton(Qudit,EveBases[i],Shot=1)
        #Measure one Photon with Bob Basis
        EveListOfCounts.append(Qudit.Counts2)
    output_string = QL.OAM_Getdits(EveListOfCounts)
    list_from_Key = [int(char) for char in output_string]
    ListOfCounts = []
    for i in range(length2):
        #print("for bit number : ", i)
        Qudit = QuditObj.QuditCircuit(4,1)
        #Getting that one photon with Alice's Basis ready to send
        Qudit = QL.OAM_Modulation(Qudit,DitSequence[i],EveBases[i])
        #circuit = GettingReady(circuit,BitSequence[i],AliceBases[i])
        #Sending Single photon
        QL.OAM_CrossTalk(Qudit,EP) if CrossT else None
        #Recive Single Photon
        QL.OAM_ReciviengSinglePhoton(Qudit,BobBases[i],Shot=1)
        #Measure one Photon with Bob Basis
        ListOfCounts.append(Qudit.Counts2)
    countstring = QL.OAM_Getdits(ListOfCounts)
    countbit = map_numbers_to_bits(countstring,length)
    countlist = [int(char) for char in countbit]
    Evecountstring = QL.OAM_Getdits(EveListOfCounts)
    Evecountbit = map_numbers_to_bits(Evecountstring,length)
    Evecountlist = [int(char) for char in Evecountbit]
    Check_list = []
    EveCheck_list = []
    for i in range(len(AliceBases)):
       if RAliceBases[i] == BobBases[i]:
           Check_list.append(countlist[2*i])
           Check_list.append(countlist[(2*i)+1])
           EveCheck_list.append(Evecountlist[2*i])
           EveCheck_list.append(Evecountlist[(2*i)+1])
    #print("The Bases checked list is : ",Check_list)
    output_string = ''.join(str(bit) for bit in Check_list)
    Eveoutput_string = ''.join(str(bit) for bit in EveCheck_list)
    return output_string , Eveoutput_string
   else:
    ListOfCounts = []
    for i in range(length2):
        #print("for bit number : ", i)
        Qudit = QuditObj.QuditCircuit(4,1)
        #Getting that one photon with Alice's Basis ready to send
        Qudit = QL.OAM_Modulation(Qudit,DitSequence[i],AliceBases[i])
        #circuit = GettingReady(circuit,BitSequence[i],AliceBases[i])
        #Sending Single photon
        QL.OAM_CrossTalk(Qudit,EP) if CrossT else None
        #Recive Single Photon
        QL.OAM_ReciviengSinglePhoton(Qudit,BobBases[i],Shot=1)
        #Measure one Photon with Bob Basis
        #print("Dit is : ",DitSequence[i]," Alice : ",AliceBases[i]," Bob : ", BobBases[i]," Measuered : ",Qudit.Counts2)

        ListOfCounts.append(Qudit.Counts2)
    countstring = QL.OAM_Getdits(ListOfCounts)
    #print(countstring)
    countbit = map_numbers_to_bits(countstring,length)
    #print(countbit)
    countlist = [int(char) for char in countbit]
    #print(countlist)
    Check_list = []
    #count = 0
    for i in range(len(AliceBases)):
       if RAliceBases[i] == BobBases[i]:
           Check_list.append(countlist[2*i])
           Check_list.append(countlist[(2*i)+1])
           #count += 1
    #print("The Bases checked list is : ",Check_list)

    output_string = ''.join(str(bit) for bit in Check_list)
    #print(count)
    return output_string



def RunningQKD(Dimension,BitSequence,AliceBases,BobBases,EveBases,length,Eve,Error):
  QC = True
  Evekey="0"
  if Dimension == 2:
    if Error:
      if Eve :
        Bobkey,Evekey = TwoD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,np.radians(25.84193276),QC)
      else:
        Bobkey = TwoD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,np.radians(25.84193276),QC)
    else:
      if Eve:
        Bobkey,Evekey = TwoD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,0,QC)
      else:
        Bobkey = TwoD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,0,QC)
  if Dimension == 4:
    if Error:
      if Eve:
        Bobkey,Evekey = FourD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,True,QC)
      else:
        Bobkey = FourD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,True,QC)
    else:
      if Eve:
        Bobkey,Evekey = FourD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,False,QC)
      else:
        Bobkey = FourD_BB84(BitSequence,AliceBases,BobBases,EveBases,length,Eve,False,QC)
  return Bobkey,Evekey

