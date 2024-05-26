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

# ---- All the functions that provide a noise-less 2-D BB84 Protocol with Alligment Error ----

def AlligmentError(cir,bit,basis,theta_radians):
#This is gettingready but with Alligment error
  cir.ry(theta_radians,8)
  if bit == 1:
    cir.x(8)
  if basis == 1:
    cir.h(8)
  return cir
def GettingReady(cir,bit,basis):
    if bit == 1:
        print("bit is 1")
        cir.x(8)
    if basis == 1:
        print("base is +-45")
        cir.h(8)
    return cir
def MeasureSinglePhoton(cir):
    # Use Aer's qasm_simulator
    simulator = Aer.get_backend('qasm_simulator')
    # Execute the circuit on the qasm simulator
    new_circuit = transpile(cir, simulator)
    job = simulator.run(new_circuit, shots = 1000)
    # Grab results from the job
    result = job.result()
    # Return counts
    counts = result.get_counts(cir)
    return counts
def ExctarctKey(Checked_List):
  length = len(Checked_List)
  result = []
  for d in Checked_List:
      new_d = {}
      for key, value in d.items():
          third_bit = key[2]  # Extract the third bit from the left
          new_d[third_bit] = value
      result.append(new_d)
  output_string = ""
  for d in result:
    key = list(d.keys())[0]  # Extract the key from the dictionary
    output_string += key
  return output_string
def SendSinglePhoton(cir,BNoise,PNoise):
    cir = QEC.Encoding(cir)
    if BNoise:
      cir = QEC.BitNoise(cir)
      cir = QEC.BitErrorCorrection(cir,9)
    if PNoise:
      cir = QEC.PhaseNoise(cir)
      cir = QEC.PhaseCorrectionBlock(cir,9)
    return cir
def ReciviengSinglePhoton(cir,BobBasis):
    cir = QEC.Decoding(cir)
    #print("Bob Basis is : ", BobBasis)
    if BobBasis == 1:
        #print("Bob Basis is +-45")
        cir.h(8)
    cir.barrier()
    cir.measure([0,1,2,3,4,5,6,7,8,9,10],[0,1,2,3,4,5,6,7,8,9,10])
    return cir
def BB84_2D(BitSequence,AliceBases,BobBases,EveBases,length,theta_radians,Eve):
   ListOfCounts = []
   EveListOfCounts = []
   if Eve==True:
    for i in range(length):
        circuit = QuantumCircuit(11,11)
        #Getting that one photon with Alice's Basis ready to send
        circuit = AlligmentError(circuit,BitSequence[i],AliceBases[i],2*theta_radians)
        #Sending Single photon
        circuit = SendSinglePhoton(circuit,False,False)
        #Recive Single Photon
        circuit = ReciviengSinglePhoton(circuit,EveBases[i])
        #Measure one Photon with Bob Basis
        counts = MeasureSinglePhoton(circuit)
        EveListOfCounts.append(counts)
        del circuit
    output_string = ExctarctKey(EveListOfCounts)
    list_from_Key = [int(char) for char in output_string]
    ListOfCounts = []
    for i in range(length):
        #print("for bit number : ", i)
        circuit = QuantumCircuit(11,11)
        #Getting that one photon with Alice's Basis ready to send
        circuit = AlligmentError(circuit,list_from_Key[i],EveBases[i],2*theta_radians)
        #circuit = GettingReady(circuit,BitSequence[i],AliceBases[i])
        #Sending Single photon
        circuit = SendSinglePhoton(circuit,False,False)
        #Recive Single Photon
        circuit = ReciviengSinglePhoton(circuit,BobBases[i])
        #Measure one Photon with Bob Basis
        counts = MeasureSinglePhoton(circuit)
        ListOfCounts.append(counts)
        #print("-----------")
        del circuit
    Check_list = []
    EveCheck_list = []
    for i in range(len(ListOfCounts)):
        if AliceBases[i] == BobBases[i]:
            Check_list.append(ListOfCounts[i])
            EveCheck_list.append(EveListOfCounts[i])
    #print("The Bases checked list is : ",Check_list)
    output_string= ExctarctKey(Check_list)
    Eveoutput_string= ExctarctKey(EveCheck_list)
    return  output_string , Eveoutput_string
   else:
    for i in range(length):
        #print("for bit number : ", i)
        circuit = QuantumCircuit(11,11)
        #Getting that one photon with Alice's Basis ready to send
        circuit = AlligmentError(circuit,BitSequence[i],AliceBases[i],2*theta_radians)
        #circuit = GettingReady(circuit,BitSequence[i],AliceBases[i])
        #Sending Single photon
        circuit = SendSinglePhoton(circuit,False,False)
        #Recive Single Photon
        circuit = ReciviengSinglePhoton(circuit,BobBases[i])
        #Measure one Photon with Bob Basis
        counts = MeasureSinglePhoton(circuit)
        ListOfCounts.append(counts)
        #print("-----------")
        del circuit
    #Now Alice and Bob share their Bases
    #print("Raw List of count is : ",ListOfCounts)
    Check_list = []
    for i in range(len(ListOfCounts)):
        if AliceBases[i] == BobBases[i]:
            Check_list.append(ListOfCounts[i])
    #print("The Bases checked list is : ",Check_list)
    output_string= ExctarctKey(Check_list)
    return  output_string
#Alice And Bob Share Some of their Key to check the Seciruty
def CheckSecurity(Key,Akey,Checklength):
    if Akey[-Checklength:] == Key[-Checklength:]:
        print("The Connection is Secure with the probability of:")
        print((1-((3/4)**Checklength))*100)
    else:
        print("The Connection is not Secure!")
def AliceKey_2D(Bit,AliceBases,BobBases):
    Check_list = []
    for i in range(len(Bit)):
        if AliceBases[i] == BobBases[i]:
            Check_list.append(Bit[i])
        Key = ''
    for item in Check_list:
        Key = Key + str(item)
    return Key


