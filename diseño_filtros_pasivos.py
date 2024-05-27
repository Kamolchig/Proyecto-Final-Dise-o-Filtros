# Kamila G
# Descripción: Este script automatiza el diseño de filtros pasivos (paso bajo, paso alto y paso banda)
# utilizando componentes comerciales (resistencias, capacitores e inductores). 
# Las resistencias y capacitores son de Steren jeje
# Itera sobre las combinaciones posibles de componentes y encuentra la mejor combinación que cumpla con 
# las especificaciones de frecuencia de corte deseadas.

#    Configura las especificaciones del filtro antes de ejecutar el script:

#    frecuencia_corte_bajo = 60  # Frecuencia de corte para paso bajo en Hz
#    frecuencia_corte_alto = 3000  # Frecuencia de corte para paso alto en Hz
#    frecuencia_corte_paso_banda_bajo = 200  # Frecuencia de corte baja para paso banda en Hz
#    frecuencia_corte_paso_banda_alto = 600  # Frecuencia de corte alta para paso banda en Hz
#    tipo_filtro = 'paso_bajo'  # Tipo de filtro ('paso_bajo', 'paso_alto', 'paso_banda') #Especificar el tipo

import pandas as pd
import numpy as np
from scipy.signal import bode, TransferFunction
import plotly.graph_objects as go

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

# Código principal
resistencias, capacitores, inductores = cargar_componentes()
tipo_filtro = 'paso_bajo'  # Ajusta esto según necesidad
frecuencias_corte = [60,100]  # Ajusta las frecuencias de corte según el tipo de filtro
mejor_combinacion = buscar_mejor_combinacion(resistencias, capacitores, inductores, tipo_filtro, frecuencias_corte)

if mejor_combinacion:
    if tipo_filtro in ['paso_bajo', 'paso_alto']:
        R, C, fc, tipo_capacitor, voltage_capacitor = mejor_combinacion
        print(f"Mejor combinación para un filtro {tipo_filtro} con frecuencia de corte {fc} Hz:")
        print(f"Resistencia: {R} ohmios, Capacitor: {C} faradios ({tipo_capacitor}, {voltage_capacitor}V)")
        if tipo_filtro == 'paso_bajo':
            num = [1]
        else:  # Paso Alto
            num = [R * C, 0]
        den = [R * C, 1]
    elif tipo_filtro == 'paso_banda':
        R, L, C, f_resonancia, ancho_banda, tipo_capacitor, voltage_capacitor = mejor_combinacion
        print(f"Mejor combinación para un filtro paso banda con frecuencias de corte {frecuencias_corte[0]} Hz a {frecuencias_corte[1]} Hz:")
        print(f"Resistencia: {R} ohmios, Inductor: {L} henrios, Capacitor: {C} faradios ({tipo_capacitor}, {voltage_capacitor}V)")
        num = [1 / L, 0]
        den = [1, R / L, 1 / (L * C)]
    system = TransferFunction(num, den)
    w, mag, phase = bode(system)
    graficar_respuesta_frecuencia_plotly(w, mag, phase, tipo_filtro)
else:
    print("No se encontró una combinación adecuada.")
