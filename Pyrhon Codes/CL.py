#All the functions needed for a Simple Classical Channel link 
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from scipy.stats import norm
import CEC
def encode_MPSK(bits, M):
    # Calculate the number of bits per symbol
    bits_per_symbol = int(np.log2(M))
    # Ensure the bit stream length is a multiple of bits_per_symbol
    while len(bits) % bits_per_symbol != 0:
        bits = np.append(bits, 0)
    
    # Create the mapping from bit groups to symbols
    mapping = {}
    for i in range(M):
        # Calculate the phase angle for the i-th symbol
        phase = 2 * np.pi * i / M
        symbol = np.exp(1j * phase)  # Complex symbol on the unit circle
        # Get the corresponding bit group as a tuple
        bit_group = tuple(int(x) for x in format(i, f'0{bits_per_symbol}b'))
        mapping[bit_group] = symbol
    
    # Encode the bit stream
    symbols = []
    for i in range(0, len(bits), bits_per_symbol):
        bit_group = tuple(bits[i:i+bits_per_symbol])
        symbol = mapping[bit_group]
        symbols.append(symbol)
    
    return np.array(symbols)
# AWGN Channel
def add_awgn_noise(signal, snr_db):
    snr_linear = 10**(snr_db / 20)
    power_signal = np.mean(np.abs(signal)**2)
    noise_power = power_signal / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(signal)) + 1j * np.random.randn(len(signal)))
    return signal + noise
def decision_maker(symbols, M):
    # Generate the constellation for M-PSK
    constellation = np.array([np.exp(1j * 2 * np.pi * i / M) for i in range(M)])
    
    # Decide the nearest constellation point for each received symbol
    decided_symbols = []
    for symbol in symbols:
        distances = np.abs(symbol - constellation)
        decided_symbols.append(constellation[np.argmin(distances)])
    
    return np.array(decided_symbols)
def decode_MPSK(symbols, M):
    # Calculate the number of bits per symbol
    bits_per_symbol = int(np.log2(M))
    
    # Create the mapping from symbols to bit groups
    mapping = {}
    for i in range(M):
        # Calculate the phase angle for the i-th symbol
        phase = 2 * np.pi * i / M
        symbol = np.exp(1j * phase)  # Complex symbol on the unit circle
        # Get the corresponding bit group as a tuple
        bit_group = tuple(int(x) for x in format(i, f'0{bits_per_symbol}b'))
        mapping[symbol] = bit_group
    
    # Decode the symbols
    bits = []
    for symbol in symbols:
        # Find the closest symbol in the mapping (nearest neighbor)
        closest_symbol = min(mapping.keys(), key=lambda k: np.abs(k - symbol))
        bits.extend(mapping[closest_symbol])
    
    return np.array(bits)
def SendClassicalChannel(SendingList,SNR,M,EC):
  length = len(SendingList)
  if EC :
     Parity_added = CEC.add_parity_bits(convert_to_np_array(SendingList),length)
  else:
     Parity_added = convert_to_np_array(SendingList)
  Encoded_SendingData = encode_MPSK(Parity_added,M)
  Noisy_Encoded_SendigData = add_awgn_noise(Encoded_SendingData,SNR)
  Decided_Symbols = decision_maker(Noisy_Encoded_SendigData,M)
  Received_SendingData = decode_MPSK(Decided_Symbols,M)
  if EC:
    RData = convert_from_np_array(CEC.EC_with_parity(Received_SendingData,length),False)
  else:
    RData = convert_from_np_array(Received_SendingData,False)
  return RData
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
