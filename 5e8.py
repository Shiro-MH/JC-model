import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def johnson_cook(strain, A, B, n, C, m):
    epsilon_dot_star = 5.00E+08  # Normalized strain rate
    T = 0  # Dimensionless temperature
    # 使用 np.power 防止溢出問題
    strain_term = np.power(strain, n) if n >= 0 else np.power(strain, -n)
    return (A + B * strain_term) * (1 + C * np.log(epsilon_dot_star)) * (1 - T**m)

# C
data = pd.read_excel('JC-model.xlsx', sheet_name='5e8')
filtered_data = data[data['strain'] > 0]
strain_data = filtered_data['strain'].values
stress_data = filtered_data['stress'].values

# 初始猜測值與參數限制
initial_guesses = [0.007, 0.001, 0.1, 0.01, 0.01]
param_bounds = ([0, 0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf, np.inf])  # 設置參數範圍

# 增加 maxfev 設定
params, params_covariance = curve_fit(
    johnson_cook, strain_data, stress_data, 
    p0=initial_guesses, bounds=param_bounds, maxfev=10000
)

print("Fitted parameters:", params)
