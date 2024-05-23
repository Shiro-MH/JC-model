import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import warnings

# 讀取 Excel 文件
file_path = 'JC-model.xlsx'
df = pd.read_excel(file_path, sheet_name='5e8')

# 篩選應變為正的數據
df = df[df['strain'] >= 0]

# 提取數據
temperature = df['K'].values
strain_rate = df['sr'].values
stress = df['stress'].values
strain = df['strain'].values
room_temp = df['K room'].values[0]
melt_temp = df['K melt'].values[0]

# 設定參考應變率
reference_strain_rate = 1.0  # 根據具體情況設置

# 定義擬合函數
def strain_hardening(eps, A, B, n):
    return A + B * eps**n

def strain_rate_effect(log_eps_dot, C):
    return 1 + C * log_eps_dot

def temperature_effect(temp, m):
    # 防止無效值
    temp_normalized = (temp - room_temp) / (melt_temp - room_temp)
    temp_normalized[temp_normalized < 0] = 0  # 防止無效的負值
    return 1 - temp_normalized**m

# 擬合 A, B, n
low_strain_rate_mask = strain_rate == min(strain_rate)  # 假設最低應變率下的數據用於擬合
try:
    popt, _ = curve_fit(strain_hardening, strain[low_strain_rate_mask], stress[low_strain_rate_mask])
    A, B, n = popt
    # 如果 B 為負，重設初始值並加上邊界限制進行擬合
    if B < 0:
        initial_guess = [0.1, 0.1, 0.1]
        bounds = (0, [np.inf, np.inf, np.inf])
        popt, _ = curve_fit(strain_hardening, strain[low_strain_rate_mask], stress[low_strain_rate_mask], p0=initial_guess, bounds=bounds)
        A, B, n = popt
except RuntimeError as e:
    print(f"Error in fitting A, B, n: {e}")
    A, B, n = np.nan, np.nan, np.nan

if not np.isnan(A) and not np.isnan(B) and not np.isnan(n):
    # 擬合 C
    normalized_stress = stress / (A + B * strain**n)
    log_eps_dot = np.log(strain_rate / reference_strain_rate)
    try:
        popt, _ = curve_fit(strain_rate_effect, log_eps_dot, normalized_stress)
        C = popt[0]
    except RuntimeError as e:
        print(f"Error in fitting C: {e}")
        C = np.nan

    # 擬合 m
    if not np.isnan(C):
        normalized_stress = stress / ((A + B * strain**n) * (1 + C * log_eps_dot))
        try:
            popt, _ = curve_fit(temperature_effect, temperature, normalized_stress)
            m = popt[0]
        except RuntimeError as e:
            print(f"Error in fitting m: {e}")
            m = np.nan
    else:
        m = np.nan
else:
    C, m = np.nan, np.nan

# 打印結果
print(f"Fitted Johnson-Cook parameters:\nA = {A}\nB = {B}\nn = {n}\nC = {C}\nm = {m}")
