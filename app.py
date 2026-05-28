import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Collatz Chaos Lab", layout="wide")

st.title("🧪 Collatz Chaos Lab: Анализ устойчивости систем")
st.sidebar.header("Параметры эксперимента")

# Ввод данных
n = st.sidebar.number_input("Начальное число (n)", value=27, step=1)
power = st.sidebar.number_input("Возведение в степень (p)", value=1.0, step=0.1)
multiplier = st.sidebar.number_input("Множитель (m)", value=3.0, step=0.01)
max_steps = st.sidebar.number_input("Максимум шагов", value=500, step=1)

def calculate_path(n, m, p):
    # Используем float для работы с огромными числами
    curr = float(n**p)
    path = [curr]
    
    for _ in range(int(max_steps)):
        if curr == 1 and m == 3: break
        
        # Логика итерации
        if curr % 2 == 0:
            curr = curr / 2
        else:
            curr = m * curr + 1
        
        path.append(curr)
        
        # Если число ушло в бесконечность (inf), прерываем
        if np.isinf(curr): 
            break
            
    return path

# Расчет
path = calculate_path(n, multiplier, power)

# График с логарифмической шкалой
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(path, color='#00ff99', linewidth=2)

# Включаем логарифмическую шкалу для отображения экспоненциального роста
ax.set_yscale('log')

ax.set_title(f"Логарифмическая динамика: m={multiplier}, p={power}, n={n}")
ax.set_xlabel("Шаги")
ax.set_ylabel("log10(Значение числа)")
ax.grid(True, which="both", linestyle='--', alpha=0.3)
st.pyplot(fig)

# Аналитика
col1, col2 = st.columns(2)
col1.metric("Финальное число", f"{path[-1]:.2e}")
col2.metric("Количество шагов", len(path))

# Вердикт системы
if np.isinf(path[-1]):
    st.error("КРИТИЧЕСКИЙ ОТКАЗ: Система достигла математической бесконечности.")
elif path[-1] > 1e15:
    st.warning("Экспоненциальный рост: система за пределами контроля.")
elif path[-1] <= 2:
    st.success("Система стабилизирована.")
else:
    st.info("Состояние хаотического блуждания.")
