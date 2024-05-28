# Kamila G
# Descripción: Este script automatiza el diseño de filtros pasivos (paso bajo, paso alto y paso banda)
# utilizando componentes comerciales (resistencias, capacitores e inductores). 

import pandas as pd
import numpy as np
from scipy.signal import bode, TransferFunction
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk, messagebox

# Funciones de cálculo y búsqueda de componentes
def cargar_componentes():
    resistencias = pd.read_csv('resistencias.csv')['value'].values
    capacitores = pd.read_csv('capacitores.csv')
    inductores = pd.read_csv('inductores.csv')['value'].values
    return resistencias, capacitores, inductores

def calcular_frecuencia_corte_paso_bajo(R, C):
    return 1 / (2 * np.pi * R * C)

def calcular_frecuencia_corte_paso_alto(R, C):
    return 1 / (2 * np.pi * R * C)

def calcular_frecuencia_corte_paso_banda(R, L, C):
    f_resonancia = 1 / (2 * np.pi * np.sqrt(L * C))
    ancho_banda = R / (2 * np.pi * L)
    return f_resonancia, ancho_banda

def buscar_mejor_combinacion(resistencias, capacitores, inductores, tipo_filtro, frecuencias_corte):
    mejor_combinacion = None
    mejor_error = float('inf')
    for R in resistencias:
        for _, row in capacitores.iterrows():
            C = row['value']
            tipo_capacitor = row['type']
            voltage_capacitor = row['voltage']
            if tipo_filtro == 'paso_bajo':
                fc = calcular_frecuencia_corte_paso_bajo(R, C)
                error = abs(fc - frecuencias_corte[0])
            elif tipo_filtro == 'paso_alto':
                fc = calcular_frecuencia_corte_paso_alto(R, C)
                error = abs(fc - frecuencias_corte[0])
            if tipo_filtro != 'paso_banda' and error < mejor_error:
                mejor_error = error
                mejor_combinacion = (R, C, fc, tipo_capacitor, voltage_capacitor)
            elif tipo_filtro == 'paso_banda':
                for L in inductores:
                    f_resonancia, ancho_banda = calcular_frecuencia_corte_paso_banda(R, L, C)
                    error = abs(f_resonancia - frecuencias_corte[0]) + abs(ancho_banda - (frecuencias_corte[1] - frecuencias_corte[0]))
                    if error < mejor_error:
                        mejor_error = error
                        mejor_combinacion = (R, L, C, f_resonancia, ancho_banda, tipo_capacitor, voltage_capacitor)
    return mejor_combinacion

def graficar_respuesta_frecuencia_plotly(w, mag, phase, tipo_filtro):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=w, y=mag, mode='lines', name='Magnitud (dB)'))
    fig.add_trace(go.Scatter(x=w, y=phase, mode='lines', name='Fase (grados)', yaxis='y2'))
    fig.update_layout(title=f'Respuesta en Frecuencia del Filtro {tipo_filtro.capitalize()} - Diagrama de Bode',
                      xaxis=dict(title='Frecuencia (rad/s)'), yaxis=dict(title='Magnitud (dB)'),
                      yaxis2=dict(title='Fase (grados)', overlaying='y', side='right'),
                      xaxis_type='log', legend_title_text='Variable')
    fig.show()

# Interfaz gráfica de usuario

def calcular_filtro():
    tipo_filtro = filtro_var.get()
    frecuencias_corte = [int(fc1_entry.get())]
    if tipo_filtro == 'paso_banda':
        frecuencias_corte.append(int(fc2_entry.get()))
    else:
        frecuencias_corte.append(None)
    
    resistencias, capacitores, inductores = cargar_componentes()
    mejor_combinacion = buscar_mejor_combinacion(resistencias, capacitores, inductores, tipo_filtro, frecuencias_corte)

    if mejor_combinacion:
        if tipo_filtro in ['paso_bajo', 'paso_alto']:
            R, C, fc, tipo_capacitor, voltage_capacitor = mejor_combinacion
            result_label.config(text=f"Mejor combinación para un filtro {tipo_filtro}:\n"
                                     f"Resistencia: {R} ohmios, Capacitor: {C} faradios ({tipo_capacitor}, {voltage_capacitor}V)\n"
                                     f"Frecuencia de corte calculada: {fc:.2f} Hz")
            if tipo_filtro == 'paso_bajo':
                num = [1]
            else:  # Paso Alto
                num = [R * C, 0]
            den = [R * C, 1]
        elif tipo_filtro == 'paso_banda':
            R, L, C, f_resonancia, ancho_banda, tipo_capacitor, voltage_capacitor = mejor_combinacion
            result_label.config(text=f"Mejor combinación para un filtro paso banda:\n"
                                     f"Resistencia: {R} ohmios, Inductor: {L} henrios, Capacitor: {C} faradios ({tipo_capacitor}, {voltage_capacitor}V)\n"
                                     f"Frecuencias de resonancia: {f_resonancia:.2f} Hz, Ancho de banda: {ancho_banda:.2f} Hz")
            num = [1 / L, 0]
            den = [1, R / L, 1 / (L * C)]
        system = TransferFunction(num, den)
        w, mag, phase = bode(system)
        graficar_respuesta_frecuencia_plotly(w, mag, phase, tipo_filtro)
    else:
        messagebox.showerror("Error", "No se encontró una combinación adecuada.")


# Configuración de la ventana principal de la GUI
root = tk.Tk()
root.title("Diseño de Filtros Pasivos")

filtro_var = tk.StringVar(value='paso_bajo')
tipos_filtro = [('Paso Bajo', 'paso_bajo'), ('Paso Alto', 'paso_alto'), ('Paso Banda', 'paso_banda')]

tk.Label(root, text="Tipo de Filtro:").grid(row=0, column=0, sticky=tk.W)
for idx, (text, mode) in enumerate(tipos_filtro):
    tk.Radiobutton(root, text=text, variable=filtro_var, value=mode).grid(row=0, column=idx+1, sticky=tk.W)

tk.Label(root, text="Frecuencia de Corte 1 (Hz):").grid(row=1, column=0, sticky=tk.W)
fc1_entry = tk.Entry(root)
fc1_entry.grid(row=1, column=1)

tk.Label(root, text="Frecuencia de Corte 2 (Hz) (Solo para paso banda):").grid(row=2, column=0, sticky=tk.W)
fc2_entry = tk.Entry(root)
fc2_entry.grid(row=2, column=1)

tk.Button(root, text="Calcular Filtro", command=calcular_filtro).grid(row=3, column=0, columnspan=2)

result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.grid(row=4, column=0, columnspan=3, sticky=tk.W)

root.mainloop()
