"""
Módulo para preprocesamiento de señales de audio
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class Preprocesador:
    def __init__(self, config):
        self.config = config
        self.alpha = config.alpha_preenfasis
        
    def aplicar_preenfasis(self, senal):
        """
        Aplica filtro de preénfasis: y[n] = x[n] - alpha * x[n-1]
        """
        senal_preenfasis = np.zeros_like(senal)
        senal_preenfasis[0] = senal[0]
        
        for i in range(1, len(senal)):
            senal_preenfasis[i] = senal[i] - self.alpha * senal[i-1]
            
        # Alternativa vectorizada (más eficiente)
        # senal_preenfasis = np.append(senal[0], senal[1:] - self.alpha * senal[:-1])
        
        return senal_preenfasis
    
    def respuesta_frecuencia_preenfasis(self):
        """
        Calcula respuesta en frecuencia del filtro de preénfasis
        """
        w, h = signal.freqz([1, -self.alpha], [1], worN=2000, fs=self.config.fs)
        
        return w, h
    
    def normalizar_senal(self, senal):
        """
        Normaliza señal entre -1 y 1
        """
        max_val = np.max(np.abs(senal))
        if max_val > 0:
            return senal / max_val
        return senal
    
    def remover_offset(self, senal):
        """
        Remueve componente DC de la señal
        """
        return senal - np.mean(senal)
    
    def recortar_silencio(self, senal, umbral=0.01):
        """
        Recorta silencios al inicio y final de la señal
        """
        # Encontrar índices donde la señal supera el umbral
        indices_activos = np.where(np.abs(senal) > umbral)[0]
        
        if len(indices_activos) == 0:
            return senal
            
        inicio = max(0, indices_activos[0] - 100)  # Margen de 100 muestras
        fin = min(len(senal), indices_activos[-1] + 100)
        
        return senal[inicio:fin]
    
    def obtener_estadisticas(self, senal):
        """
        Calcula estadísticas básicas de la señal
        """
        return {
            'rms': np.sqrt(np.mean(senal**2)),
            'pico_maximo': np.max(np.abs(senal)),
            'media': np.mean(senal),
            'desviacion_estandar': np.std(senal)
        }