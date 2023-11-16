import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, curve_fit
import pandas as pd

# Función para el ajuste de la curva
def quadratic_func(x, a, b, c):
    return a * x**2 + b * x + c

def quadratic_eq_solver(a, b, c):
    def equation(x):
        return a * x ** 2 + b * x + c

    roots = fsolve(equation, 0)
    return roots

def plot_quadratic_eq(a, b, c):
    x = np.linspace(-10, 10, 400)
    y = a * x ** 2 + b * x + c

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'{a}x^2 + {b}x + {c} = 0')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Quadratic Equation')
    plt.grid()
    plt.legend()
    st.pyplot(plt)

st.title('Solver App')
menu_option = st.sidebar.selectbox(
    "Menú",["Resolver ecuaciones de segundo grado o menor",
            "ajustar ecuación cuadrática segun los datos"])
if menu_option == "Resolver ecuaciones de segundo grado o menor":

    st.sidebar.header('Input')
    a = st.sidebar.number_input('Coefficient a', value=1)
    b = st.sidebar.number_input('Coefficient b', value=1)
    c = st.sidebar.number_input('Coefficient c', value=1)

    if st.sidebar.button('Solve'):
        roots = quadratic_eq_solver(a, b, c)
        df = pd.DataFrame({'Roots': roots})
        st.write(df)

        plot_quadratic_eq(a, b, c)

if menu_option == "Ajustar ecuación cuadrática segun los datos":

    st.title('Ajuste de una Ecuación Cuadrática a Datos')

    # Inicializar un DataFrame vacío para almacenar los puntos
    data = pd.DataFrame(columns=['X', 'Y'])

    st.header('Ingresar Puntos (X, Y)')

    # Entrada para ingresar múltiples puntos separados por comas o espacios
    points_input = st.text_input('Ingrese los puntos (X Y, separados por comas o espacios):')
    add_button = st.button('Agregar Puntos')

    if add_button:
        # Dividir la entrada en puntos individuales y agregarlos al DataFrame
        points = [p.strip() for p in points_input.split(',')] if ',' in points_input else points_input.split()
        for point in points:
            x, y = map(float, point.split())
            data = data._append({'X': x, 'Y': y}, ignore_index=True)
        st.success(f'Se han agregado los puntos: {points}')

    st.header('Puntos Ingresados')
    st.write(data)


    # Realizar el ajuste de la curva si hay al menos 3 puntos
    if len(data) >= 3:
        st.header('Ajuste de la Curva Cuadrática')

        # Obtener los valores de X e Y
        x_values = data['X'].values
        y_values = data['Y'].values

        # Realizar el ajuste de la curva
        popt, _ = curve_fit(quadratic_func, x_values, y_values)

        # Mostrar los coeficientes de la ecuación cuadrática
        st.write(f'La ecuación cuadrática ajustada es: Y = {popt[0]} * X^2 + {popt[1]} * X + {popt[2]}')

    # Graficar los puntos y la curva ajustada
        plt.figure(figsize=(8, 6))
        plt.scatter(x_values, y_values, label='Datos')
        x_curve = np.linspace(min(x_values), max(x_values), 100)
        y_curve = quadratic_func(x_curve, *popt)
        plt.plot(x_curve, y_curve, 'r', label='Curva Ajustada')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        st.pyplot(plt)

    else:
        st.warning('Se necesitan al menos 3 puntos para ajustar una curva cuadrática.')
