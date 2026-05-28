import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Collatz Chaos Lab", layout="wide")

st.title("🧪 Collatz Chaos Lab: Анализ устойчивости систем")
st.sidebar.header("Параметры эксперимента")

# Настройки пользователя
n = st.sidebar.number_input("Начальное число (n)", value=27)
power = st.sidebar.slider("Возведение в степень (p)", 1, 3, 1)
multiplier = st.sidebar.selectbox("Множитель (m)", [1.9, 2.0, 2.1, 3, 5, 7])
max_steps = st.sidebar.slider("Максимум шагов", 100, 2000, 500)

def calculate_path(n, m, p):
    path = [n**p]
    curr = n**p
    for _ in range(max_steps):
        if curr == 1 and m == 3: break
        if curr % 2 == 0:
            curr = curr // 2
        else:
            curr = m * curr + 1
        path.append(curr)
        if curr > 10**10: break # Защита от переполнения
    return path

# Логика расчета
path = calculate_path(n, multiplier, power)

# Эффект "Вау" — график
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

if path[-1] > 10**8:
    st.error("Система ушла в экспоненциальный рост (Дивергенция).")
elif path[-1] == 1:
    st.success("Система достигла стабильного аттрактора.")
else:
    st.warning("Система в состоянии хаотического блуждания.")
