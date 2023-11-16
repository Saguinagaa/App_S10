import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import pandas as pd

st.title('Solver App')

# Function to solve quadratic equation
def quadratic_eq_solver(a, b, c):
    def equation(x):
        return a * x ** 2 + b * x + c

    roots = fsolve(equation, 0)
    return roots

# Function to plot quadratic equation
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

# User input for coefficients
a = st.number_input('Coefficient a', value=1)
b = st.number_input('Coefficient b', value=1)
c = st.number_input('Coefficient c', value=1)

# Solve button
if st.button('Solve'):
    roots = quadratic_eq_solver(a, b, c)
    df = pd.DataFrame({'Roots': roots})
    st.write(df)

    plot_quadratic_eq(a, b, c)
