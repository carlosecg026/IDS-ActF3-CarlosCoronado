Diseño y análisis de filtros digitales en Python

Descripción
Este proyecto implementa y compara tres filtros digitales Butterworth de tipo IIR:
- Pasa bajos: frecuencia de corte de 30 Hz.
- Pasa altos: frecuencia de corte de 80 Hz.
- Pasa bandas: banda de paso entre 40 y 70 Hz.

La señal de prueba contiene componentes sinusoidales de 5 Hz, 50 Hz y 120 Hz, además de ruido blanco. Se analizan las señales filtradas en el dominio del tiempo, sus espectros de amplitud y la respuesta en frecuencia de cada filtro.

Objetivo
Diseñar filtros digitales y evaluar su comportamiento al conservar las frecuencias de interés y atenuar componentes fuera de las bandas seleccionadas.

Herramientas
- Python 3
- NumPy
- SciPy
- Matplotlib

Cómo ejecutar el proyecto

1. Instala Python 3 si aún no lo tienes.
2. Descarga o clona este repositorio.
3. Abre una terminal en la carpeta del proyecto.
4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta el programa:

   ```bash
   python main.py
   ```

El programa mostrará en la terminal los valores RMS y guardará tres gráficas en la carpeta `resultados/`.

Alternativa: Google Colab
También puedes abrir Google Colab, cargar `main.py` o copiar el contenido en una celda. Si trabajas en Colab, instala las bibliotecas que falten con:

```python
!pip install numpy scipy matplotlib
```

Parámetros de simulación

| Parámetro | Valor |
|---|---:|
| Frecuencia de muestreo | 500 Hz |
| Duración de la señal | 2 segundos |
| Orden de los filtros | 4 |
| Componentes sinusoidales | 5, 50 y 120 Hz |
| Corte pasa bajos | 30 Hz |
| Corte pasa altos | 80 Hz |
| Banda pasa bandas | 40–70 Hz |

Resultados esperados
- El pasa bajos conserva principalmente la componente de 5 Hz.
- El pasa altos conserva principalmente la componente de 120 Hz.
- El pasa bandas conserva principalmente la componente de 50 Hz.

Los filtros atenúan frecuencias fuera de sus bandas de paso, pero no eliminan necesariamente todo el ruido blanco, porque parte del ruido puede coincidir con las frecuencias que el filtro permite pasar.

Métrica RMS
El programa calcula el valor RMS de la señal original y de cada salida. La reducción relativa del RMS describe el cambio en la magnitud global de la señal, **no** el porcentaje exacto de ruido eliminado, ya que también influyen las componentes útiles que conserva cada filtro.

Nota técnica
Se utiliza `sosfiltfilt`, que aplica el filtrado en ambos sentidos y evita el desfase de fase en el resultado. Este procedimiento es útil para análisis fuera de línea; para sistemas de tiempo real normalmente se requiere un método de filtrado causal.

Archivos
- `main.py`: código de la simulación.
- `requirements.txt`: bibliotecas necesarias.
- `resultados/`: gráficas generadas al ejecutar el código.

Autor
Carlos Eduardo Coronado Godina
