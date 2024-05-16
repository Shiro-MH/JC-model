import numpy as np
from scipy.optimize import curve_fit

def johnson_cook(strain, A, B, n, C, m):
    epsilon_dot_star = 5.00E+08  # Normalized strain rate
    T = 0  # Dimensionless temperature
    return (A + B * strain**n) * (1 + C * np.log(epsilon_dot_star)) * (1 - T**m)

# Given data
strain_data = np.array([0.058993436])
stress_data = np.array([0.007609965])  # 實際應力數據

# Initial guesses for A, B, n, C, m
initial_guesses = [0.007, 0.001, 0.1, 0.01, 0.01]

# Perform the curve fit
params, params_covariance = curve_fit(johnson_cook, strain_data, stress_data, p0=initial_guesses)

print("Fitted parameters:", params)
