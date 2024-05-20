import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Load the data
data = pd.read_excel('JC-model.xlsx')

# Filter data to remove negative strains if needed
data = data[data['strain'] >= 0]

# Define the Johnson-Cook model function
def johnson_cook(stress, epsilon, strain_rate, T, A, B, n, C, m):
    # Calculate temperature factor (assuming T_room and T_melt are provided in the dataframe)
    T_factor = (T - data['K room']) / (data['K melt'] - data['K room'])
    return (A + B * epsilon**n) * (1 + C * np.log(strain_rate)) * (1 - T_factor**m)

# Initial guess for the parameters
initial_guess = [500, 100, 0.1, 0.02, 0.1]  # Example initial guesses for A, B, n, C, m

# Preparing data for curve fitting
epsilon = data['strain'].values
strain_rate = data['sr'].values
T = data['K'].values
stress = data['stress'].values

# Perform curve fitting
popt, pcov = curve_fit(lambda stress, A, B, n, C, m: johnson_cook(stress, epsilon, strain_rate, T, A, B, n, C, m),
                       stress, epsilon, p0=initial_guess)

# Output the optimal parameters
print("Fitted parameters: A, B, n, C, m:", popt)
