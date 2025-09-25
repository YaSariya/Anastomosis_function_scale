#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import math

# Константы
rho = 1060  # Плотность крови кг/м³
mu = 0.0035  # Динамическая вязкость крови Па·с

def calculate_reynolds(diameter, velocity):
    """Рассчитывает число Рейнольдса"""
    if diameter == 0:
        return 0
    return (rho * velocity * diameter) / mu

def classify_flow(re):
    """Классифицирует тип потока по числу Рейнольдса"""
    if re < 2000:
        return "Ламинарный", "🟢"
    elif re < 4000:
        return "Переходный", "🟡"
    else:
        return "Турбулентный", "🔴"

def calculate_wall_shear_stress(diameter, velocity):
    """Рассчитывает напряжение сдвига на стенке сосуда"""
    if diameter == 0:
        return 0
    return (8 * mu * velocity) / diameter

def main():
    st.set_page_config(page_title="Анализатор анастомоза", layout="wide")
    st.title("🧠 Гемодинамический анализатор анастомоза")
    st.write("Исследуйте параметры потока в сосудистом анастомозе")
    
    # Создаем колонки для ввода параметров
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("Донорская артерия")
        d_donor = st.number_input("Диаметр (мм)", min_value=0.1, max_value=5.0, value=1.2, key="d_donor")
        v_donor = st.number_input("Скорость (см/с)", min_value=1.0, max_value=100.0, value=8.0, key="v_donor")
        p_donor = st.number_input("Давление (мм рт.ст.)", min_value=10.0, max_value=200.0, value=80.0, key="p_donor")
    
    with col2:
        st.header("Акцепторная артерия")
        d_acceptor = st.number_input("Диаметр (мм)", min_value=0.1, max_value=5.0, value=1.0, key="d_acceptor")
        v_acceptor = st.number_input("Скорость (см/с)", min_value=1.0, max_value=100.0, value=10.0, key="v_acceptor")
        p_acceptor = st.number_input("Давление (мм рт.ст.)", min_value=10.0, max_value=200.0, value=75.0, key="p_acceptor")
    
    with col3:
        st.header("Отводящая артерия")
        d_out = st.number_input("Диаметр (мм)", min_value=0.1, max_value=5.0, value=1.2, key="d_out")
        v_out = st.number_input("Скорость (см/с)", min_value=1.0, max_value=100.0, value=15.0, key="v_out")
        p_out = st.number_input("Давление (мм рт.ст.)", min_value=10.0, max_value=200.0, value=78.0, key="p_out")
    
    # Конвертация единиц
    d_donor_m = d_donor * 0.001
    d_acceptor_m = d_acceptor * 0.001
    d_out_m = d_out * 0.001
    
    v_donor_ms = v_donor * 0.01
    v_acceptor_ms = v_acceptor * 0.01
    v_out_ms = v_out * 0.01
    
    # Расчет параметров
    re_donor = calculate_reynolds(d_donor_m, v_donor_ms)
    re_acceptor = calculate_reynolds(d_acceptor_m, v_acceptor_ms)
    re_out = calculate_reynolds(d_out_m, v_out_ms)
    
    flow_donor, emoji_donor = classify_flow(re_donor)
    flow_acceptor, emoji_acceptor = classify_flow(re_acceptor)
    flow_out, emoji_out = classify_flow(re_out)
    
    # Расчет напряжений сдвига
    tau_donor = calculate_wall_shear_stress(d_donor_m, v_donor_ms)
    tau_acceptor = calculate_wall_shear_stress(d_acceptor_m, v_acceptor_ms)
    tau_out = calculate_wall_shear_stress(d_out_m, v_out_ms)
    
    # Проверка баланса потоков
    q_donor = v_donor_ms * (math.pi * (d_donor_m/2)**2)
    q_acceptor = v_acceptor_ms * (math.pi * (d_acceptor_m/2)**2)
    q_out = v_out_ms * (math.pi * (d_out_m/2)**2)
    
    flow_balance_error = abs((q_donor + q_acceptor) - q_out) / q_out * 100 if q_out > 0 else 100
    
    # Проверка баланса давлений
    pressure_diff = abs(p_donor - p_acceptor)
    
    # Визуализация результатов
    st.markdown("---")
    st.header("📊 Результаты анализа")
    
    # Отображение результатов в виде метрик
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.subheader("Донорская артерия")
        st.metric("Тип потока", f"{emoji_donor} {flow_donor}")
        st.metric("Число Рейнольдса", f"{re_donor:.0f}")
        st.metric("Напряжение сдвига", f"{tau_donor:.2f} Па")
        st.metric("Объемный расход", f"{q_donor*1e6:.2f} мл/с")
    
    with col5:
        st.subheader("Акцепторная артерия")
        st.metric("Тип потока", f"{emoji_acceptor} {flow_acceptor}")
        st.metric("Число Рейнольдса", f"{re_acceptor:.0f}")
        st.metric("Напряжение сдвига", f"{tau_acceptor:.2f} Па")
        st.metric("Объемный расход", f"{q_acceptor*1e6:.2f} мл/с")
    
    with col6:
        st.subheader("Отводящая артерия")
        st.metric("Тип потока", f"{emoji_out} {flow_out}")
        st.metric("Число Рейнольдса", f"{re_out:.0f}")
        st.metric("Напряжение сдвига", f"{tau_out:.2f} Па")
        st.metric("Объемный расход", f"{q_out*1e6:.2f} мл/с")
    
    # Визуализация с помощью progress bars
    st.subheader("Визуализация параметров")
    
    st.write("**Числа Рейнольдса:**")
    st.progress(min(re_donor / 5000, 1.0), text=f"Донорская: {re_donor:.0f}")
    st.progress(min(re_acceptor / 5000, 1.0), text=f"Акцепторная: {re_acceptor:.0f}")
    st.progress(min(re_out / 5000, 1.0), text=f"Отводящая: {re_out:.0f}")
    
    st.write("**Напряжения сдвига (Па):**")
    st.progress(min(tau_donor / 5, 1.0), text=f"Донорская: {tau_donor:.2f} Па")
    st.progress(min(tau_acceptor / 5, 1.0), text=f"Акцепторная: {tau_acceptor:.2f} Па")
    st.progress(min(tau_out / 5, 1.0), text=f"Отводящая: {tau_out:.2f} Па")
    
    # Оценка стабильности
    st.subheader("📈 Оценка стабильности анастомоза")
    
    stability_score = 0
    feedback = []
    
    # Критерий 1: Тип потока
    if all(re < 2000 for re in [re_donor, re_acceptor, re_out]):
        stability_score += 2
        feedback.append("✅ Все потоки ламинарные")
    elif all(re < 4000 for re in [re_donor, re_acceptor, re_out]):
        stability_score += 1
        feedback.append("⚠️ Потоки в переходной зоне")
    else:
        feedback.append("❌ Обнаружена турбулентность")
    
    # Критерий 2: Напряжение сдвига
    if all(1.5 < tau < 2.5 for tau in [tau_donor, tau_acceptor, tau_out]):
        stability_score += 2
        feedback.append("✅ Напряжения сдвига в норме")
    elif all(0.5 < tau < 4.0 for tau in [tau_donor, tau_acceptor, tau_out]):
        stability_score += 1
        feedback.append("⚠️ Напряжения сдвига близки к границам нормы")
    else:
        feedback.append("❌ Критическое напряжение сдвига")
    
    # Критерий 3: Баланс потоков
    if flow_balance_error < 5:
        stability_score += 1
        feedback.append("✅ Отличный баланс потоков")
    elif flow_balance_error < 10:
        stability_score += 1
        feedback.append("⚠️ Умеренный дисбаланс потоков")
    else:
        feedback.append("❌ Значительный дисбаланс потоков")
    
    # Критерий 4: Баланс давлений
    if pressure_diff < 5:
        stability_score += 1
        feedback.append("✅ Идеальный баланс давлений")
    elif pressure_diff < 10:
        stability_score += 1
        feedback.append("⚠️ Умеренная разница давлений")
    else:
        feedback.append("❌ Большая разница давлений")
    
    # Отображение оценки
    col7, col8 = st.columns([1, 3])
    
    with col7:
        st.metric("Оценка стабильности", f"{stability_score}/6")
        
        if stability_score >= 5:
            st.success("✅ Анастомоз стабилен")
        elif stability_score >= 3:
            st.warning("⚠️ Анастомоз требует наблюдения")
        else:
            st.error("❌ Высокий риск закрытия анастомоза")
    
    with col8:
        st.write("**Детальный анализ:**")
        for item in feedback:
            st.write(item)
    
    # Рекомендации
    st.subheader("💡 Рекомендации")
    
    if any(re > 2000 for re in [re_donor, re_acceptor, re_out]):
        st.write("**Для стабилизации потока:**")
        if re_donor > 2000:
            st.write("- Увеличьте диаметр донорской артерии или уменьшите скорость потока")
        if re_acceptor > 2000:
            st.write("- Увеличьте диаметр акцепторной артерии или уменьшите скорость потока")
        if re_out > 2000:
            st.write("- Увеличьте диаметр отводящей артерии")
    
    if any(tau < 0.5 or tau > 4.0 for tau in [tau_donor, tau_acceptor, tau_out]):
        st.write("**Для оптимизации напряжения сдвига:**")
        if tau_donor < 0.5 or tau_acceptor < 0.5 or tau_out < 0.5:
            st.write("- Увеличьте скорость потока в сосудах с низким напряжением сдвига")
        if tau_donor > 4.0 or tau_acceptor > 4.0 or tau_out > 4.0:
            st.write("- Уменьшите скорость потока в сосудах с высоким напряжением сдвига")
    
    if flow_balance_error > 10:
        st.write("- Скорректируйте диаметры сосудов для соблюдения баланса потоков")
    
    if pressure_diff > 10:
        st.write("- Добейтесь большего равенства давлений в донорской и акцепторной артериях")

if __name__ == "__main__":
    main()


# In[ ]:




