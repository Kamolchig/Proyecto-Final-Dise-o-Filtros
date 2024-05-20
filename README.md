# Diseño de Filtros Pasivos

## Descripción
Este script automatiza el diseño de filtros pasivos (paso bajo, paso alto y paso banda) utilizando componentes comerciales (resistencias, capacitores e inductores). Las resistencias y capacitores son de Steren.

El script itera sobre las combinaciones posibles de componentes y encuentra la mejor combinación que cumpla con las especificaciones de frecuencia de corte deseadas.

## Instrucciones

### Configuración
Configura las especificaciones del filtro antes de ejecutar el script:

```python
frecuencia_corte_bajo = 60  # Frecuencia de corte para paso bajo en Hz
frecuencia_corte_alto = 3000  # Frecuencia de corte para paso alto en Hz
frecuencia_corte_paso_banda_bajo = 200  # Frecuencia de corte baja para paso banda en Hz
frecuencia_corte_paso_banda_alto = 600  # Frecuencia de corte alta para paso banda en Hz
tipo_filtro = 'paso_bajo'  # Tipo de filtro ('paso_bajo', 'paso_alto', 'paso_banda')
