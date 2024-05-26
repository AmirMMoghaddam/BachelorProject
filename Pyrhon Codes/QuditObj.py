# All Qudit related functions and objects


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

def base4_sort(key):
    return int(key, 4)
class QuditCircuit:
    def __init__(self, d, n):
        # Calculate the total number of qubits
        self.num_qudits = n
        self.dimension = d
        self.num_qubits = n * d/2
        self.Counts = []
        self.Counts2 = []
        # Create a QuantumCircuit object with the specified dimensions
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
    def measure(self):
        # Add a barrier to separate the measurement operations
        self.circuit.barrier()
        # Measure all qubits
        qubit_indices = list(range(int(self.num_qubits)))
        self.circuit.measure(qubit_indices, qubit_indices)
    def CT(self,Gate):
      CT_Gate = qi.Operator(Gate)
      for i in range(0, int(self.num_qubits), 2):
        self.circuit.unitary(CT_Gate, [i,i+1], label="CrossTalk")
    def Translate(self):
      # Translate each key into the desired format
      translated_data = {}
      for key, value in self.Counts.items():
          translated_key = ''.join([str(int(key[i:i+2], 2)) for i in range(0, len(key), 2)])
          translated_data[translated_key] = value
      sorted_data = {k: v for k, v in sorted(translated_data.items(), key=lambda item: base4_sort(item[0]))}
      self.Counts2 = sorted_data
    def run(self,Shot):
      # Use Aer's qasm_simulator
      simulator = Aer.get_backend('qasm_simulator')
      # Execute the circuit on the qasm simulator
      new_circuit = transpile(self.circuit, simulator)
      job = simulator.run(new_circuit, shots = Shot)
      # Grab results from the job
      result = job.result()
      # Return counts
      self.Counts = result.get_counts(self.circuit)
      self.Translate()
    def test(self):
      self.circuit.x(1)


