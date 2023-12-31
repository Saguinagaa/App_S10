import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, curve_fit
import pandas as pd



# La aplicación utiliza la libreria scipy para
# realizar cálculos de resolver ecuaciones hallando
# sus raíces y para ajustar una curva según los puntos
# que el usuario suministre. Además utiliza la librería
# matplotlib para graficar información sobre los cálculos
# que el usuario esté realizando. Y por último usa
# la librería pandas para almacenar los puntos que el
# usuario ingrese para ajustar una curva, se eligió
# pandas por encima de numpy debito a que ésta
# es más versátil.

# Función para el ajuste de la curva
def quadratic_func(x, a, b, c):
    """Ésta función recibe todos los parametros
    para calcular una función cuadrática y retorna
    el cálculo hecho"""
    return a * x**2 + b * x + c

def quadratic_eq_solver(a, b, c):
    """Ésta función recibe todos los parametros
    para calcular una función cuadrática, posteriormente
    calcula las raíces de la ecuación para por
    úlitmo retornarlas"""
    def equation(x):
        return a * x ** 2 + b * x + c

    roots = fsolve(equation, 0)
    return roots


def plot_quadratic_eq(a, b, c):
    """La función recibe los parámetros
    necesarios para graficar una ecuación
    cuadrática y luego la grafica por medio
    de la librería matplot"""
    x = np.linspace(-10, 10, 400)
    y = a * x ** 2 + b * x + c

    plt.figure(figsize=(8, 6))
    plt.plot(x, y,label=f'{round(a, 2)}x^2\
              + {round(b, 2)}x^1+ {round(c, 2)} = 0')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Ecuación')
    plt.grid()
    plt.legend()
    st.pyplot(plt)

st.title('Solver App')
menu_option = st.sidebar.selectbox(
    "Menú",["Resolver ecuaciones de segundo grado o menor",
            "Ajustar ecuación cuadrática segun los datos"])
if menu_option == "Resolver ecuaciones de segundo grado o menor":

    # User input for coefficients
    a = st.number_input('Coeficiente de a/x^2', value=1)
    b = st.number_input('Coeficient e de b/^1', value=1)
    c = st.number_input('Coeficient e de c/constante', value=1)

    # Solve button
    if st.button('Solve'):
        roots = quadratic_eq_solver(a, b, c)
        df = pd.DataFrame({'Raíces': roots})
        st.write(df)

        plot_quadratic_eq(a, b, c)

if menu_option == "Ajustar ecuación cuadrática segun los datos":

    st.title('Ajuste de una Ecuación Cuadrática a Datos')

    # Inicializar un DataFrame vacío para almacenar los puntos
    data = pd.DataFrame(columns=['X', 'Y'])

    st.header('Ingresar Puntos (X, Y)')

    # Entrada para ingresar múltiples puntos separados por comas o espacios
    points_input = st.text_input(
        'Ingrese los puntos con el siguiente formato \
            X1 Y1, X2 Y2, X3 Y3')
    add_button = st.button('Agregar Puntos')

    if add_button:
        # Dividir la entrada en puntos individuales y agregarlos al DataFrame
        points = [
            p.strip() for p in points_input.split(',')] if ',' in points_input else points_input.split()
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
        st.write(f'La ecuación cuadrática \
                 ajustada es: Y = {round(popt[0], 2)} * X^2 + \
                    {round(popt[1], 2)} * X + {round(popt[2], 2)}')

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
        st.warning('Se necesitan al menos 3 puntos\
                    para ajustar una curva cuadrática.')
