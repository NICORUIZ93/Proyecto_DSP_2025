#!/usr/bin/env python3
"""
Módulo de visualización para el proyecto DSP
Orange Pi 5 Plus - Procesamiento Digital de Señales
"""

import matplotlib
matplotlib.use('Agg')  # Para uso sin interfaz gráfica
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

class Visualizador:
    """Clase para generar visualizaciones de señales y análisis espectral"""

    def __init__(self, config):
        """Inicializar visualizador con configuración"""
        self.config = config
        self.directorio_graficas = "graficas"

        # Crear directorio si no existe
        if not os.path.exists(self.directorio_graficas):
            os.makedirs(self.directorio_graficas)

        # Configurar estilo de gráficos
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10

    def graficas_comparativas(self, senal_original, senal_filtrada, fft_original, fft_filtrada, espectrograma, f, t):
        """Generar gráficas comparativas de señales y espectros"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1. Gráfico temporal: señal original vs filtrada
        plt.figure(figsize=(15, 6))

        plt.subplot(2, 1, 1)
        plt.plot(senal_original, 'b-', alpha=0.7, label='Señal Original')
        plt.title('Señal de Voz - Temporal')
        plt.xlabel('Muestras')
        plt.ylabel('Amplitud')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 1, 2)
        plt.plot(senal_filtrada, 'r-', alpha=0.7, label='Señal Filtrada')
        plt.title('Señal de Voz Filtrada - Temporal')
        plt.xlabel('Muestras')
        plt.ylabel('Amplitud')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{self.directorio_graficas}/senal_temporal_{timestamp}.png", dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✅ Gráfico temporal guardado: senal_temporal_{timestamp}.png")

        # 2. Comparación de FFT
        frecuencias = np.linspace(0, self.config.fs/2, len(fft_original))

        plt.figure(figsize=(15, 6))

        plt.subplot(2, 1, 1)
        plt.plot(frecuencias, 20 * np.log10(np.abs(fft_original)), 'b-', label='FFT Original')
        plt.title('Espectro de Frecuencia - Original')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.xlim(0, 8000)
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.subplot(2, 1, 2)
        plt.plot(frecuencias, 20 * np.log10(np.abs(fft_filtrada)), 'r-', label='FFT Filtrada')
        plt.title('Espectro de Frecuencia - Filtrada')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.xlim(0, 8000)
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{self.directorio_graficas}/fft_comparacion_{timestamp}.png", dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✅ Gráfico FFT guardado: fft_comparacion_{timestamp}.png")

        # 3. Espectrograma
        plt.figure(figsize=(12, 8))
        plt.pcolormesh(t, f, 10 * np.log10(espectrograma), shading='gouraud', cmap='viridis')
        plt.title('Espectrograma de la Señal Filtrada')
        plt.ylabel('Frecuencia (Hz)')
        plt.xlabel('Tiempo (s)')
        plt.colorbar(label='Potencia (dB)')
        plt.ylim(0, 4000)

        plt.tight_layout()
        plt.savefig(f"{self.directorio_graficas}/espectrograma_{timestamp}.png", dpi=150, bbox_inches='tight')
        plt.close()

        print(f"✅ Espectrograma guardado: espectrograma_{timestamp}.png")

    def graficar_senal_individual(self, senal, titulo="Señal", archivo_salida=None):
        """Graficar una señal individual"""
        plt.figure(figsize=(12, 6))
        plt.plot(senal, 'b-', alpha=0.8)
        plt.title(titulo)
        plt.xlabel('Muestras')
        plt.ylabel('Amplitud')
        plt.grid(True, alpha=0.3)

        if archivo_salida:
            plt.savefig(archivo_salida, dpi=150, bbox_inches='tight')
        plt.close()

    def graficar_fft(self, fft, frecuencias, titulo="FFT", archivo_salida=None):
        """Graficar FFT"""
        plt.figure(figsize=(12, 6))
        plt.plot(frecuencias, 20 * np.log10(np.abs(fft)), 'b-')
        plt.title(titulo)
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.grid(True, alpha=0.3)

        if archivo_salida:
            plt.savefig(archivo_salida, dpi=150, bbox_inches='tight')
        plt.close()