"""
Módulo para análisis espectral de señales
"""

import numpy as np
from scipy import signal
import json
import matplotlib.pyplot as plt

class AnalizadorEspectral:
    def __init__(self, config):
        self.config = config
        self.fs = config.fs
        
    def calcular_fft(self, senal, ventana=None, n_fft=None):
        """
        Calcula FFT de la señal
        """
        if n_fft is None:
            n_fft = self.config.ventana_fft
        if ventana is None:
            ventana = self.config.ventana_spectrogram
            
        # Aplicar ventana
        if ventana == 'hann':
            win = signal.windows.hann(len(senal))
        elif ventana == 'hamming':
            win = signal.windows.hamming(len(senal))
        else:
            win = np.ones(len(senal))
            
        senal_ventaneada = senal * win
        
        # Calcular FFT
        fft_compleja = np.fft.rfft(senal_ventaneada, n=n_fft)
        frecuencias = np.fft.rfftfreq(n_fft, 1/self.fs)
        magnitud = np.abs(fft_compleja)
        
        return frecuencias, magnitud
    
    def calcular_espectrograma(self, senal, ventana=None, solape=None, n_fft=None):
        """
        Calcula espectrograma usando STFT
        """
        if n_fft is None:
            n_fft = self.config.ventana_fft
        if ventana is None:
            ventana = self.config.ventana_spectrogram
        if solape is None:
            solape = self.config.solape_fft
            
        f, t, Sxx = signal.spectrogram(
            senal,
            fs=self.fs,
            window=ventana,
            nperseg=n_fft,
            noverlap=solape,
            scaling='density'
        )
        
        # Convertir a dB
        Sxx_db = 10 * np.log10(Sxx + 1e-10)
        
        return f, t, Sxx_db
    
    def calcular_snr(self, senal, metodo='silicio'):
        """
        Calcula relación señal-ruido (SNR) en dB
        
        SNR = 10·log10(P_señal / P_ruido)
        """
        if metodo == 'silicio':
            # Asumir primeros 1000 samples como ruido
            if len(senal) > 2000:
                ruido = senal[:1000]
                senal_util = senal[1000:]
            else:
                # Para señales cortas, usar percentil bajo como ruido
                umbral = np.percentile(np.abs(senal), 10)
                ruido = senal[np.abs(senal) < umbral]
                senal_util = senal[np.abs(senal) >= umbral]
                
        elif metodo == 'segmentacion':
            # Método más avanzado con segmentación por energía
            umbral = 0.1 * np.max(np.abs(senal))
            mascara_senal = np.abs(senal) > umbral
            mascara_ruido = ~mascara_senal
            
            senal_util = senal[mascara_senal]
            ruido = senal[mascara_ruido]
            
        else:
            raise ValueError("Método no válido")
        
        if len(senal_util) == 0 or len(ruido) == 0:
            return 0
            
        potencia_senal = np.mean(senal_util**2)
        potencia_ruido = np.mean(ruido**2)
        
        if potencia_ruido == 0:
            return float('inf')
            
        snr_linear = potencia_senal / potencia_ruido
        return 10 * np.log10(snr_linear)
    
    def calcular_energia_subbandas(self, fft, frecuencias, bandas=None):
        """
        Calcula energía en subbandas espectrales
        """
        if bandas is None:
            bandas = self.config.bandas_energia
            
        energias = []
        
        for i in range(len(bandas) - 1):
            mascara = (frecuencias >= bandas[i]) & (frecuencias < bandas[i + 1])
            if np.any(mascara):
                energia = np.sum(fft[mascara]**2)
                energias.append(energia)
            else:
                energias.append(0)
                
        return energias
    
    def calcular_centroide_espectral(self, fft, frecuencias):
        """
        Calcula centroide espectral
        
        C = Σ(f · |X(f)|) / Σ(|X(f)|)
        """
        if np.sum(fft) == 0:
            return 0
            
        centroide = np.sum(frecuencias * fft) / np.sum(fft)
        return centroide
    
    def calcular_ancho_banda_espectral(self, fft, frecuencias, percentil=90):
        """
        Calcula ancho de banda espectral
        """
        if np.sum(fft) == 0:
            return 0
            
        # Calcular distribución acumulativa
        energia_total = np.cumsum(fft)
        if energia_total[-1] == 0:
            return 0
            
        energia_normalizada = energia_total / energia_total[-1]
        
        # Encontrar frecuencia donde se alcanza el percentil
        idx = np.where(energia_normalizada >= percentil/100)[0]
        if len(idx) > 0:
            return frecuencias[idx[0]]
        return frecuencias[-1]
    
    def guardar_resultados(self, resultados, archivo_salida):
        """
        Guarda resultados en archivo JSON
        """
        # Convertir numpy arrays a listas para JSON
        resultados_json = {}
        for key, value in resultados.items():
            if isinstance(value, (np.ndarray, np.generic)):
                resultados_json[key] = value.tolist() if hasattr(value, 'tolist') else float(value)
            else:
                resultados_json[key] = value
                
        with open(archivo_salida, 'w') as f:
            json.dump(resultados_json, f, indent=4)
            
        print(f"Resultados guardados en: {archivo_salida}")