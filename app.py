import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Collatz Chaos Lab Pro", layout="wide")

# Заголовок и описание
st.title("🧪 Collatz Chaos Lab: Анализ хаоса")
st.sidebar.header("Параметры эксперимента")

# Ввод данных
n = st.sidebar.number_input("Начальное число (n)", value=27, step=1)
power = st.sidebar.number_input("Степень (p)", value=1.0, step=0.01)
multiplier = st.sidebar.number_input("Множитель (m)", value=3.0, step=0.01)
max_steps = st.sidebar.number_input("Максимум шагов", value=1000, step=1)

# Вычислительный движок
def calculate_path(n, m, p):
    curr = float(n**p)
    path = [curr]
    
    for _ in range(int(max_steps)):
        # Условие завершения для классического цикла
        if curr == 1 and m == 3: break
        
        # Основная логика Коллатца
        if curr % 2 == 0:
            curr = curr / 2
        else:
            curr = m * curr + 1
        
        path.append(curr)
        
        # Проверка на выход в бесконечность
        if np.isinf(curr) or curr > 1e100: 
            break
            
    return path

# Запуск расчета
path = calculate_path(n, multiplier, power)

# Визуализация
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(path, color='#00ff99', linewidth=1.5, alpha=0.8)
ax.set_yscale('log') # Логарифмический масштаб для анализа роста
ax.set_title(f"Траектория системы: n={n}, m={multiplier}, p={power}")
ax.set_xlabel("Количество итераций")
ax.set_ylabel("log10(Значение числа)")
ax.grid(True, which="both", linestyle='--', alpha=0.3)
st.pyplot(fig)

# Аналитическая панель
col1, col2, col3 = st.columns(3)
col1.metric("Финальное число", f"{path[-1]:.2e}")
col2.metric("Шагов до конца", len(path))
col3.metric("Пиковое значение", f"{max(path):.2e}")

# Вердикт системы (логика анализа)
if np.isinf(path[-1]):
    st.error("КРИТИЧЕСКИЙ ОТКАЗ: Система дивергировала в бесконечность.")
elif path[-1] <= 2:
    st.success("СТАТУС: Стабильный аттрактор достигнут.")
else:
    st.info("СТАТУС: Состояние динамического хаоса.")

# Вывод данных для глубокого анализа
with st.expander("Посмотреть сырые данные траектории"):
    st.write(path)
