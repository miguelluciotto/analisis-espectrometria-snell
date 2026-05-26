# Análisis Computacional - Laboratorio de Óptica

Este repositorio contiene el código fuente y los conjuntos de datos experimentales utilizados para el análisis estadístico y físico de los experimentos correspondientes a "Fuentes de Luz y Ley de Snell". 

El procesamiento computacional fue diseñado para garantizar la reproducibilidad de los resultados reportados en el documento principal, automatizando la extracción de información, la normalización de perfiles espectrales y la determinación de índices de refracción mediante ajustes de regresión lineal.

## Estructura del Repositorio

* **`data/`**: Contiene las mediciones directas obtenidas en el laboratorio. 
  * `espectrometria/`: Archivos de texto con intensidades y longitudes de onda medidos con el espectrómetro digital.
  * `snell/`: Archivos tabulares (`.csv`) con las mediciones angulares de incidencia, reflexión y refracción.
* **`scripts/`**: Rutinas de análisis y modelado escritas en Python.
  * `espectrometria/`: Scripts para la normalización de espectros continuos y la detección automatizada de picos de emisión atómica mediante el procesamiento de señales.
  * `snell/`: Scripts para la verificación cinemática de la reflexión, evaluación de la zona de Reflexión Interna Total (RIT) y cálculo del índice de refracción por mínimos cuadrados con propagación de errores.
* **`graphs/`**: Visualizaciones de datos y ajustes de curvas en alta resolución, generadas automáticamente para su integración en el reporte final.
* **`images/`**: Esquemas y diagramas teóricos utilizados como soporte gráfico.

## Dependencias

El análisis analítico y visual fue desarrollado utilizando Python 3.11.11. Para ejecutar los scripts y reproducir los modelos, se requiere el siguiente entorno de librerías científicas:

```bash
pip install numpy pandas matplotlib seaborn scipy
```
