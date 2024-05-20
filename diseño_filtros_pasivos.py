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
import matplotlib.pyplot as plt
from scipy.signal import bode, TransferFunction

# Cargar datos de componentes
resistencias = pd.read_csv('resistencias.csv')['value'].values  # Lista de resistencias de steren en ohmios
capacitores = pd.read_csv('capacitores.csv')  # Lista de capacitores de steren con sus valores en faradios, tipo y tensión nominal en voltios
inductores = pd.read_csv('inductores_comerciales.csv')['value'].values  # Lista de inductores comerciales con sus valores en henrios y tensión nominal en voltios (estos no son de steren sopas)

# Definir especificaciones del filtro
frecuencia_corte_bajo = 60  # Frecuencia de corte para paso bajo en Hz
frecuencia_corte_alto = 3000  # Frecuencia de corte para paso alto en Hz
frecuencia_corte_paso_banda_bajo = 200  # Frecuencia de corte baja para paso banda en Hz
frecuencia_corte_paso_banda_alto = 600  # Frecuencia de corte alta para paso banda en Hz
tipo_filtro = 'paso_bajo'  # Tipo de filtro ('paso_bajo', 'paso_alto', 'paso_banda')

# Funciones para calcular las frecuencias de corte
def calcular_frecuencia_corte_paso_bajo(R, C):
    return 1 / (2 * np.pi * R * C)

def calcular_frecuencia_corte_paso_alto(R, C):
    return 1 / (2 * np.pi * R * C)

def calcular_frecuencia_corte_paso_banda(R, L, C):
    f_resonancia = 1 / (2 * np.pi * np.sqrt(L * C))
    ancho_banda = R / (2 * np.pi * L)
    return f_resonancia, ancho_banda

# Iterar sobre los valores de componentes para encontrar la mejor combinación
mejor_combinacion = None
mejor_error = float('inf')

for R in resistencias:
    for _, row in capacitores.iterrows():
        C = row['value']
        tipo_capacitor = row['type']
        voltage_capacitor = row['voltage']
        
        if tipo_filtro == 'paso_bajo':
            fc = calcular_frecuencia_corte_paso_bajo(R, C)
            error = abs(fc - frecuencia_corte_bajo)
        elif tipo_filtro == 'paso_alto':
            fc = calcular_frecuencia_corte_paso_alto(R, C)
            error = abs(fc - frecuencia_corte_alto)
        elif tipo_filtro == 'paso_banda':
            for L in inductores:
                f_resonancia, ancho_banda = calcular_frecuencia_corte_paso_banda(R, L, C)
                error = abs(f_resonancia - frecuencia_corte_paso_banda_bajo) + abs(ancho_banda - (frecuencia_corte_paso_banda_alto - frecuencia_corte_paso_banda_bajo))
                if error < mejor_error:
                    mejor_error = error
                    mejor_combinacion = (R, L, C, f_resonancia, ancho_banda, tipo_capacitor, voltage_capacitor)
        else:
            continue
        
        if error < mejor_error and tipo_filtro != 'paso_banda':
            mejor_error = error
            mejor_combinacion = (R, C, fc, tipo_capacitor, voltage_capacitor)

# Mostrar la mejor combinación encontrada y plotea la gráfica de Bode
if mejor_combinacion:
    if tipo_filtro == 'paso_bajo' or tipo_filtro == 'paso_alto':
        R, C, fc, tipo_capacitor, voltage_capacitor = mejor_combinacion
        print(f"Mejor combinación para un filtro {tipo_filtro} con frecuencia de corte {frecuencia_corte_bajo if tipo_filtro == 'paso_bajo' else frecuencia_corte_alto} Hz:")
        print(f"Resistencia: {R} ohmios")
        print(f"Capacitor: {C} faradios ({tipo_capacitor}, {voltage_capacitor}V)")
        print(f"Frecuencia de corte obtenida: {fc:.2f} Hz")
        
        # Crear la función de transferencia para el filtro
        num = [1]
        den = [R*C, 1]
        system = TransferFunction(num, den)
        w, mag, phase = bode(system)
        
        # Graficar la respuesta en frecuencia (diagrama de Bode)
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.semilogx(w, mag)    # Bode magnitude plot
        plt.title(f'Filtro {tipo_filtro.capitalize()} - Diagrama de Bode')
        plt.ylabel('Magnitud (dB)')
        plt.grid(which='both', axis='both')

        plt.subplot(2, 1, 2)
        plt.semilogx(w, phase)  # Bode phase plot
        plt.ylabel('Fase (grados)')
        plt.xlabel('Frecuencia (rad/s)')
        plt.grid(which='both', axis='both')
        plt.show()
    
    elif tipo_filtro == 'paso_banda':
        R, L, C, f_resonancia, ancho_banda, tipo_capacitor, voltage_capacitor = mejor_combinacion
        print(f"Mejor combinación para un filtro paso banda con frecuencias de corte {frecuencia_corte_paso_banda_bajo} Hz a {frecuencia_corte_paso_banda_alto} Hz:")
        print(f"Resistencia: {R} ohmios")
        print(f"Inductor: {L} henrios")
        print(f"Capacitor: {C} faradios ({tipo_capacitor}, {voltage_capacitor}V)")
        print(f"Frecuencia de resonancia obtenida: {f_resonancia:.2f} Hz")
        print(f"Ancho de banda obtenido: {ancho_banda:.2f} Hz")
        
        # Crear la función de transferencia para el filtro paso banda
        num = [R/L, 0]
        den = [1, R/L, 1/(L*C)]
        system = TransferFunction(num, den)
        w, mag, phase = bode(system)
        
        # Graficar la respuesta en frecuencia (diagrama de Bode)
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.semilogx(w, mag)    # Bode magnitude plot
        plt.title(f'Filtro Paso Banda - Diagrama de Bode')
        plt.ylabel('Magnitud (dB)')
        plt.grid(which='both', axis='both')

        plt.subplot(2, 1, 2)
        plt.semilogx(w, phase)  # Bode phase plot
        plt.ylabel('Fase (grados)')
        plt.xlabel('Frecuencia (rad/s)')
        plt.grid(which='both', axis='both')
        plt.show()
else:
    print("No se encontró una combinación adecuada.")
