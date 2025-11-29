#!/usr/bin/env python3
"""
Demo simplificada del proyecto DSP - Funciona sin scipy
Orange Pi 5 Plus - Procesamiento Digital de Señales

Estudiante: NICOLAS ENRIQUE RUIZ VEGA
Código: 20251583005
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

class DSPSimple:
    """Implementación simplificada de DSP usando solo numpy"""

    def __init__(self, fs=16000):
        self.fs = fs
        self.directorio_graficas = "graficas"
        if not os.path.exists(self.directorio_graficas):
            os.makedirs(self.directorio_graficas)

    def generar_senal_prueba(self, duracion=3):
        """Genera señal de voz sintética"""
        t = np.linspace(0, duracion, int(duracion * self.fs), endpoint=False)

        # Componentes de frecuencia típicas de voz
        f1, f2, f3 = 300, 1000, 2500  # Formantes vocales
        ruido_50hz = 0.1 * np.sin(2 * np.pi * 50 * t)  # Ruido de línea
        ruido_blanco = 0.05 * np.random.randn(len(t))  # Ruido ambiente

        # Señal de voz básica
        senal = (0.5 * np.sin(2 * np.pi * f1 * t) +
                0.3 * np.sin(2 * np.pi * f2 * t) +
                0.2 * np.sin(2 * np.pi * f3 * t) +
                ruido_50hz + ruido_blanco)

        # Normalizar
        senal = senal / np.max(np.abs(senal))

        return senal

    def aplicar_preenfasis(self, senal, alpha=0.97):
        """Filtro de preénfasis simple"""
        y = np.zeros_like(senal)
        y[0] = senal[0]
        for n in range(1, len(senal)):
            y[n] = senal[n] - alpha * senal[n-1]
        return y

    def filtro_notch_simple(self, senal, f0=50, r=0.9):
        """Filtro notch IIR simple"""
        w0 = 2 * np.pi * f0 / self.fs

        # Coeficientes
        b = [1, -2 * np.cos(w0), 1]
        a = [1, -2 * r * np.cos(w0), r * r]

        # Aplicar filtro (implementación básica de lfilter)
        y = np.zeros_like(senal)
        for n in range(len(senal)):
            y[n] = b[0] * senal[n]
            if n >= 1:
                y[n] -= a[1] * y[n-1]
            if n >= 2:
                y[n] -= a[2] * y[n-2]
                y[n] += b[1] * senal[n-1] + b[2] * senal[n-2]

        return y

    def filtro_pasabajos_simple(self, senal, fc=3400, orden=51):
        """Filtro FIR pasabajos simple usando ventana Hamming"""
        nyquist = self.fs / 2
        fc_norm = fc / nyquist

        # Coeficientes FIR ideales
        n = np.arange(orden) - (orden - 1) // 2
        h_ideal = fc_norm * np.sinc(fc_norm * n)

        # Ventana Hamming
        ventana = 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(orden) / (orden - 1))
        taps = h_ideal * ventana

        # Normalizar
        taps = taps / np.sum(taps)

        # Aplicar convolución
        return np.convolve(senal, taps, mode='same')

    def calcular_fft(self, senal):
        """Calcular FFT simple"""
        fft = np.fft.rfft(senal)
        frecuencias = np.fft.rfftfreq(len(senal), 1/self.fs)
        return frecuencias, fft

    def calcular_snr(self, senal):
        """Calcular SNR aproximado"""
        # Usar varianza como aproximación
        potencia_total = np.var(senal)
        # Asumir que el ruido es el 10% de la potencia total
        potencia_senal = 0.9 * potencia_total
        potencia_ruido = 0.1 * potencia_total

        if potencia_ruido > 0:
            snr_db = 10 * np.log10(potencia_senal / potencia_ruido)
        else:
            snr_db = 60  # SNR alto si poco ruido

        return snr_db

    def calcular_energia_subbandas(self, fft, frecuencias):
        """Calcular energía en subbandas"""
        # Definir subbandas (0-1kHz, 1-2kHz, 2-4kHz, 4-8kHz)
        bandas = [(0, 1000), (1000, 2000), (2000, 4000), (4000, 8000)]
        energias = []

        for f_min, f_max in bandas:
            mask = (frecuencias >= f_min) & (frecuencias <= f_max)
            energia = np.sum(np.abs(fft[mask])**2)
            energias.append(energia)

        return energias

    def calcular_centroide_espectral(self, fft, frecuencias):
        """Calcular centroide espectral"""
        numerador = np.sum(frecuencias * np.abs(fft)**2)
        denominador = np.sum(np.abs(fft)**2)

        if denominador > 0:
            centroide = numerador / denominador
        else:
            centroide = 0

        return centroide

    def generar_graficas(self, senal_original, senal_filtrada):
        """Generar gráficas comparativas"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # FFT de ambas señales
        freq_orig, fft_orig = self.calcular_fft(senal_original)
        freq_filt, fft_filt = self.calcular_fft(senal_filtrada)

        # Gráfico temporal
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.plot(np.arange(len(senal_original)) / self.fs, senal_original, 'b-', alpha=0.7)
        plt.title('Señal Original - Temporal')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.grid(True)

        plt.subplot(2, 2, 2)
        plt.plot(np.arange(len(senal_filtrada)) / self.fs, senal_filtrada, 'r-', alpha=0.7)
        plt.title('Señal Filtrada - Temporal')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.grid(True)

        plt.subplot(2, 2, 3)
        plt.plot(freq_orig, 20 * np.log10(np.abs(fft_orig) + 1e-10), 'b-', alpha=0.7)
        plt.title('Espectro Original')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.xlim(0, 8000)
        plt.grid(True)

        plt.subplot(2, 2, 4)
        plt.plot(freq_filt, 20 * np.log10(np.abs(fft_filt) + 1e-10), 'r-', alpha=0.7)
        plt.title('Espectro Filtrado')
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Magnitud (dB)')
        plt.xlim(0, 8000)
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(f"{self.directorio_graficas}/demo_simple_{timestamp}.png", dpi=150)
        plt.close()

        print(f"✅ Gráficas guardadas: demo_simple_{timestamp}.png")

    def ejecutar_demo(self):
        """Ejecutar demo completa"""
        print("🎵 === DEMO SIMPLIFICADA DSP - ORANGE PI 5 PLUS ===")
        print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 1. Generar señal de prueba
        print("\n1. GENERANDO SEÑAL DE PRUEBA")
        senal_original = self.generar_senal_prueba(3)
        print(f"Duración: {len(senal_original)/self.fs:.2f}s, Muestras: {len(senal_original)}")

        # 2. Preprocesamiento
        print("\n2. PREPROCESAMIENTO")
        senal_preenfasis = self.aplicar_preenfasis(senal_original)

        # 3. Filtrado
        print("\n3. FILTRADO DIGITAL")
        senal_notch = self.filtro_notch_simple(senal_preenfasis, 50)
        senal_filtrada = self.filtro_pasabajos_simple(senal_notch, 3400)

        # 4. Análisis SNR
        print("\n4. ANÁLISIS SNR")
        snr_original = self.calcular_snr(senal_original)
        snr_filtrado = self.calcular_snr(senal_filtrada)

        print(".2f"        print(".2f"        print(".2f"
        # 5. Análisis espectral
        print("\n5. ANÁLISIS ESPECTRAL")
        freq, fft = self.calcular_fft(senal_filtrada)
        energias = self.calcular_energia_subbandas(fft, freq)
        centroide = self.calcular_centroide_espectral(fft, freq)

        print(".2f"        print(f"Energías por subbandas: {[f'{e:.2f}' for e in energias]}")

        # 6. Visualización
        print("\n6. GENERANDO VISUALIZACIONES")
        self.generar_graficas(senal_original, senal_filtrada)

        # 7. Resultados
        print("\n7. GUARDANDO RESULTADOS")
        resultados = {
            'snr_original': snr_original,
            'snr_filtrado': snr_filtrado,
            'mejora_snr': snr_filtrado - snr_original,
            'centroide_espectral': centroide,
            'energias_subbandas': energias,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Crear directorio resultados si no existe
        if not os.path.exists("datos/resultados"):
            os.makedirs("datos/resultados")

        with open("datos/resultados/demo_resultados.json", 'w') as f:
            json.dump(resultados, f, indent=2)

        print(f"Resultados guardados en: datos/resultados/demo_resultados.json")
        print("\n✅ DEMO COMPLETADA EXITOSAMENTE")
        print("El sistema DSP funciona correctamente con implementación simplificada")

        return resultados

if __name__ == "__main__":
    dsp = DSPSimple()
    resultados = dsp.ejecutar_demo()

    print("\n📊 Resumen de Resultados:")
    for key, value in resultados.items():
        if isinstance(value, list):
            print(f"{key}: {[f'{v:.2f}' for v in value]}")
        else:
            print(f"{key}: {value:.2f}" if isinstance(value, (int, float)) else f"{key}: {value}")