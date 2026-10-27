"""
Proyecto: Diseño y análisis de filtros digitales Butterworth
Autor: [Escribe tu nombre]
Descripción:
Genera una señal con componentes de 5, 50 y 120 Hz más ruido blanco.
Aplica filtros pasa bajos, pasa altos y pasa bandas, y guarda las gráficas.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt, sosfreqz

OUTPUT_DIR = "resultados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Parámetros de simulación
fs = 500
duracion = 2
t = np.arange(0, duracion, 1 / fs)
np.random.seed(42)
orden = 4

# 2. Construcción de la señal de prueba
senal_5hz = 1.0 * np.sin(2 * np.pi * 5 * t)
senal_50hz = 0.7 * np.sin(2 * np.pi * 50 * t)
senal_120hz = 0.5 * np.sin(2 * np.pi * 120 * t)
ruido = 0.5 * np.random.normal(size=len(t))
senal_original = senal_5hz + senal_50hz + senal_120hz + ruido

# 3. Diseño de filtros Butterworth IIR en formato SOS
filtro_bajos = butter(orden, 30, btype="lowpass", fs=fs, output="sos")
filtro_altos = butter(orden, 80, btype="highpass", fs=fs, output="sos")
filtro_bandas = butter(orden, [40, 70], btype="bandpass", fs=fs, output="sos")

# 4. Aplicación de filtros (filtrado de fase cero, apropiado para análisis offline)
salida_bajos = sosfiltfilt(filtro_bajos, senal_original)
salida_altos = sosfiltfilt(filtro_altos, senal_original)
salida_bandas = sosfiltfilt(filtro_bandas, senal_original)

# 5. Gráficas en el dominio del tiempo
fig, axes = plt.subplots(4, 1, figsize=(12, 9), sharex=True)
series = [
    (senal_original, "Señal original: 5, 50 y 120 Hz + ruido"),
    (salida_bajos, "Filtro pasa bajos (30 Hz)"),
    (salida_altos, "Filtro pasa altos (80 Hz)"),
    (salida_bandas, "Filtro pasa bandas (40–70 Hz)")
]
for ax, (senal, titulo) in zip(axes, series):
    ax.plot(t, senal, linewidth=0.8)
    ax.set_title(titulo)
    ax.set_ylabel("Amplitud")
    ax.grid(True)
axes[-1].set_xlabel("Tiempo (s)")
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "senales_tiempo.png"), dpi=160)
plt.close(fig)

# 6. Espectros de amplitud
def espectro_amplitud(senal, frecuencia_muestreo):
    n = len(senal)
    frecuencias = np.fft.rfftfreq(n, d=1 / frecuencia_muestreo)
    amplitudes = 2 * np.abs(np.fft.rfft(senal)) / n
    amplitudes[0] /= 2
    if n % 2 == 0:
        amplitudes[-1] /= 2
    return frecuencias, amplitudes

frecs, espectro_original = espectro_amplitud(senal_original, fs)
_, espectro_bajos = espectro_amplitud(salida_bajos, fs)
_, espectro_altos = espectro_amplitud(salida_altos, fs)
_, espectro_bandas = espectro_amplitud(salida_bandas, fs)

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
espectros = [
    (espectro_original, "Espectro de la señal original"),
    (espectro_bajos, "Espectro después del pasa bajos"),
    (espectro_altos, "Espectro después del pasa altos"),
    (espectro_bandas, "Espectro después del pasa bandas")
]
for ax, (espectro, titulo) in zip(axes.flat, espectros):
    ax.plot(frecs, espectro)
    ax.set_title(titulo)
    ax.set_xlim(0, 180)
    ax.set_xlabel("Frecuencia (Hz)")
    ax.set_ylabel("Amplitud")
    ax.grid(True)
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "espectros.png"), dpi=160)
plt.close(fig)

# 7. Respuesta en frecuencia
f1, h1 = sosfreqz(filtro_bajos, worN=2048, fs=fs)
f2, h2 = sosfreqz(filtro_altos, worN=2048, fs=fs)
f3, h3 = sosfreqz(filtro_bandas, worN=2048, fs=fs)

fig, ax = plt.subplots(figsize=(12, 6))
for f, h, label in [
    (f1, h1, "Pasa bajos: 30 Hz"),
    (f2, h2, "Pasa altos: 80 Hz"),
    (f3, h3, "Pasa bandas: 40–70 Hz")
]:
    magnitud_db = 20 * np.log10(np.maximum(np.abs(h), 1e-10))
    ax.plot(f, magnitud_db, label=label)
ax.axhline(-3, linestyle="--", linewidth=0.8, label="Referencia de -3 dB")
ax.set_title("Respuesta en frecuencia de los filtros Butterworth")
ax.set_xlabel("Frecuencia (Hz)")
ax.set_ylabel("Magnitud (dB)")
ax.set_xlim(0, 180)
ax.set_ylim(-80, 5)
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(OUTPUT_DIR, "respuesta_frecuencia.png"), dpi=160)
plt.close(fig)

# 8. Comparación numérica RMS
def valor_rms(senal):
    return np.sqrt(np.mean(senal ** 2))

resultados = {
    "Señal original": valor_rms(senal_original),
    "Filtro pasa bajos": valor_rms(salida_bajos),
    "Filtro pasa altos": valor_rms(salida_altos),
    "Filtro pasa bandas": valor_rms(salida_bandas),
}

print("COMPARACIÓN DE VALORES RMS")
print("-" * 40)
for nombre, valor in resultados.items():
    print(f"{nombre:22s}: {valor:.4f}")

rms_original = resultados["Señal original"]
print("\nReducción relativa del RMS respecto a la señal original:")
for nombre in ["Filtro pasa bajos", "Filtro pasa altos", "Filtro pasa bandas"]:
    reduccion = (1 - resultados[nombre] / rms_original) * 100
    print(f"{nombre:22s}: {reduccion:.1f}%")

print("\nParámetros de simulación:")
print(f"Frecuencia de muestreo: {fs} Hz")
print(f"Duración: {duracion} s")
print(f"Orden de filtros: {orden}")
print(f"Gráficas guardadas en la carpeta '{OUTPUT_DIR}'.")
