#This functions are used for classical Error Correction 
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from scipy.stats import norm

def add_parity_bits(data, k):
    p = int(np.ceil(np.sqrt(k)))
    n = p ** 2
    if n > k:
        data = np.append(data, np.zeros(n - k))
    # Pad the data with zeros to meet the divisibility requirement
    data_matrix = data.reshape((p, p))
    parity_rows = np.mod(np.sum(data_matrix, axis=1), 2)
    parity_cols = np.mod(np.sum(data_matrix, axis=0), 2)

    # Append parity bits for rows and columns to the original matrix
    data_matrix_with_parity = np.column_stack((data_matrix, parity_rows))
    parity_cols = np.append(parity_cols, 0)  # Parity of parity bits
    data_matrix_with_parity = np.vstack((data_matrix_with_parity, parity_cols))

    # Flatten the matrix and return
    return data_matrix_with_parity.flatten()
def EC_with_parity(bits,k):
    p = int(np.ceil(np.sqrt(k)))
    n = (p+1) ** 2
    if n <= len(bits):
      bits = bits[:n]
    else:
      print("Something is Wrong")
    data_matrix = bits.reshape((p+1, p+1))
    parity_rows = np.mod(np.sum(data_matrix, axis=1), 2)
    parity_cols = np.mod(np.sum(data_matrix, axis=0), 2)
    for i in range(len(parity_rows)):
      if parity_rows[i] == 1:
        j = 0
        while parity_cols[j] != 1:
          j = j+1
          if j >= len(parity_cols):
            break;
        if j != len(parity_cols):
          data_matrix[i,j] = 1 - data_matrix[i,j]
        parity_rows = np.mod(np.sum(data_matrix, axis=1), 2)
        parity_cols = np.mod(np.sum(data_matrix, axis=0), 2)
    return data_matrix[:-1, :-1].flatten()