import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Collatz Chaos Lab", layout="wide")

st.title("🧪 Collatz Chaos Lab: Анализ устойчивости систем")
st.sidebar.header("Параметры эксперимента")

# Ввод данных вручную — максимальная гибкость
n = st.sidebar.number_input("Начальное число (n)", value=27, step=1)
power = st.sidebar.number_input("Возведение в степень (p)", value=1.0, step=0.1)
multiplier = st.sidebar.number_input("Множитель (m)", value=3.0, step=0.01)
max_steps = st.sidebar.number_input("Максимум шагов", value=500, step=1)

def calculate_path(n, m, p):
    # Работаем с float для поддержки дробных множителей и степеней
    curr = float(n**p)
    path = [curr]
    
    for _ in range(int(max_steps)):
        if curr == 1 and m == 3: break
        # Логика: если четное — делим, иначе — множитель + 1
        if curr % 2 == 0:
            curr = curr / 2
        else:
            curr = m * curr + 1
        path.append(curr)
        # Защита от переполнения
        if curr > 1e15: 
            break 
    return path

# Логика расчета
path = calculate_path(n, multiplier, power)

# График
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(path, color='#00ff99', linewidth=2)
ax.set_title(f"Динамика системы: m={multiplier}, p={power}")
ax.set_xlabel("Шаги")
ax.set_ylabel("Значение числа")
ax.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

# Аналитическая панель
col1, col2 = st.columns(2)
col1.metric("Финальное число", f"{path[-1]:.2e}")
col2.metric("Количество шагов", len(path))

if path[-1] > 1e10:
    st.error("Дивергенция: система вышла за пределы вычислительной стабильности.")
elif path[-1] <= 2:
    st.success("Система стабилизирована.")
else:
    st.warning("Состояние неопределенности (Хаос).")
