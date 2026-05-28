import streamlit as st
import plotly.graph_objects as go # Меняем matplotlib на Plotly
import numpy as np

st.set_page_config(page_title="Collatz Chaos Lab Pro", layout="wide")

st.title("🧪 Collatz Chaos Lab: Анализ хаоса")
st.sidebar.header("Параметры эксперимента")

n = st.sidebar.number_input("Начальное число (n)", value=27, step=1)
power = st.sidebar.number_input("Степень (p)", value=1.0, step=0.01)
multiplier = st.sidebar.number_input("Множитель (m)", value=3.0, step=0.01)
max_steps = st.sidebar.number_input("Максимум шагов", value=1000, step=1)

def calculate_path(n, m, p):
    curr = float(n**p)
    path = [curr]
    for _ in range(int(max_steps)):
        if curr == 1 and m == 3: break
        if curr % 2 == 0: curr = curr / 2
        else: curr = m * curr + 1
        path.append(curr)
        if np.isinf(curr) or curr > 1e100: break
    return path

path = calculate_path(n, multiplier, power)

# ИНТЕРАКТИВНЫЙ ГРАФИК (Plotly)
fig = go.Figure()
fig.add_trace(go.Scatter(
    y=path, 
    mode='lines+markers', 
    line=dict(color='#00ff99', width=2),
    marker=dict(size=4)
))

fig.update_layout(
    title=f"Динамика системы: m={multiplier}, p={power}",
    yaxis_type="log", # Логарифмический масштаб
    template="plotly_dark", # Темная тема для «вау-эффекта»
    xaxis_title="Итерации",
    yaxis_title="Значение (log10)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
col1.metric("Финальное число", f"{path[-1]:.2e}")
col2.metric("Всего шагов", len(path))

if np.isinf(path[-1]): st.error("Дивергенция: система ушла в бесконечность.")
elif path[-1] <= 2: st.success("Система стабилизирована.")
else: st.info("Состояние динамического хаоса.")
