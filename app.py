import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Función para el ajuste de la curva
def quadratic_func(x, a, b, c):
    return a * x**2 + b * x + c

# Función principal de la app

st.title('Ajuste de una Ecuación Cuadrática a Datos')

# Inicializar un DataFrame vacío para almacenar los puntos
data = pd.DataFrame(columns=['X', 'Y'])

st.header('Ingresar Puntos (X, Y)')

# Entrada para ingresar puntos
x_input = st.number_input('Ingrese el valor de X:')
y_input = st.number_input('Ingrese el valor de Y:')
add_button = st.button('Agregar Punto')

if add_button:
    data = data._append({'X': x_input, 'Y': y_input}, ignore_index=True)
    st.success(f'Se ha agregado el punto: ({x_input}, {y_input})')

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

