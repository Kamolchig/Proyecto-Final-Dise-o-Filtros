# Powered by Kamila G
# Diseño de Filtros Pasivos

Este proyecto automatiza el diseño de filtros pasivos (paso bajo, paso alto y paso banda) utilizando componentes comerciales (resistencias, capacitores e inductores). El script permite seleccionar el tipo de filtro y las frecuencias de corte, y muestra la mejor combinación de componentes junto con la respuesta en frecuencia del filtro en un diagrama de Bode.

## Requisitos

- Python 3.x
- Pandas
- NumPy
- SciPy
- Plotly
- Tkinter (incluido en la instalación estándar de Python)

## Archivos CSV

El script utiliza tres archivos CSV para cargar los valores de los componentes:

1. `resistencias.csv`: Contiene una columna `value` con los valores de las resistencias en ohmios.
2. `capacitores.csv`: Contiene tres columnas `value`, `type` y `voltage` con los valores, tipos y voltajes de los capacitores.
3. `inductores.csv`: Contiene una columna `value` con los valores de los inductores en henrios.

## Uso

1. Clona este repositorio o descarga los archivos en tu máquina local.
2. Asegúrate de tener los archivos `resistencias.csv`, `capacitores.csv` e `inductores.csv` en el mismo directorio que el script.
3. Instala las dependencias necesarias ejecutando:

    ```sh
    pip install pandas numpy scipy plotly
    ```

4. Ejecuta el script:

    ```sh
    python filtro_pasivo_gui.py
    ```

5. Se abrirá una interfaz gráfica de usuario. Selecciona el tipo de filtro que deseas diseñar (`paso bajo`, `paso alto`, `paso banda`).
6. Ingresa la(s) frecuencia(s) de corte en los campos correspondientes.
7. Haz clic en el botón "Calcular Filtro".
8. La mejor combinación de componentes se mostrará en la interfaz, junto con la respuesta en frecuencia del filtro en un diagrama de Bode.

## Modificación de Componentes

Si deseas iterar con otros componentes, simplemente modifica los archivos CSV (`resistencias.csv`, `capacitores.csv`, `inductores.csv`) con los nuevos valores. Asegúrate de mantener el mismo formato de columnas:

- `resistencias.csv`: Debe contener una columna `value` con los valores de las resistencias.
- `capacitores.csv`: Debe contener tres columnas `value`, `type` y `voltage`.
- `inductores.csv`: Debe contener una columna `value` con los valores de los inductores.

## Ejemplo de Contenido de Archivos CSV

### resistencias.csv

```csv
value
100
220
330
470
