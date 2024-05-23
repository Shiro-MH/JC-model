import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.optimize import minimize


# 定義 Johnson-Cook 模型的函數
def johnson_cook(epsilon, strain_rate, T, A, B, n, C, m):
    # 計算溫度因子 (假設 T_room 和 T_melt 已在數據框中給出)
    T_factor = (T - data['K room']) / (data['K melt'] - data['K room'])
    return (A + B * epsilon**n) * (1 + C * np.log(strain_rate)) * (1 - T_factor**m)

# 定義目標函數
def objective(params, stress, epsilon, strain_rate, T):
    A, B, n, C, m = params
    predicted_stress = johnson_cook(epsilon, strain_rate, T, A, B, n, C, m)
    return np.sum((stress - predicted_stress)**2)

# 加載數據
file_path = 'JC-model.xlsx'
data = pd.read_excel(file_path, sheet_name='main')

# 過濾數據以去除負應變
data = data[data['strain'] >= 0]

# 準備擬合所需的數據
epsilon = data['strain'].values
strain_rate = data['sr'].values
T = data['K'].values
stress = data['stress'].values

# 初始參數
initial_params = [500, 100, 0.1, 0.02, 0.1]  # 根據實際情況可能需要調整

# 使用 minimize 進行優化
result = minimize(objective, initial_params, args=(stress, epsilon, strain_rate, T), method='BFGS')

# 輸出優化結果
if result.success:
    fitted_params = result.x
    print("Optimized parameters: A, B, n, C, m:", fitted_params)
else:
    print("Optimization failed:", result.message)

# 優化參數的協方差矩陣
if hasattr(result, 'hess_inv'):
    pcov = result.hess_inv
    print("Covariance of the parameters:\n", pcov)

    