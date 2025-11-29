"""
Módulo para diseño e implementación de filtros digitales
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class FiltrosDigitales:
    def __init__(self, config):
        self.config = config
        self.fs = config.fs
        
    def diseñar_filtro_notch(self, f0, r=None):
        """
        Diseña filtro notch digital para frecuencia f0
        
        H(z) = [1 - 2cos(w0)z^{-1} + z^{-2}] / [1 - 2r·cos(w0)z^{-1} + r^2·z^{-2}]
        """
        if r is None:
            r = self.config.r_notch
            
        w0 = 2 * np.pi * f0 / self.fs
        
        # Coeficientes del filtro
        b = [1, -2 * np.cos(w0), 1]
        a = [1, -2 * r * np.cos(w0), r * r]
        
        return b, a
    
    def aplicar_filtro_notch(self, senal, f0, r=None):
        """
        Aplica filtro notch a la señal
        """
        b, a = self.diseñar_filtro_notch(f0, r)
        senal_filtrada = signal.lfilter(b, a, senal)
        
        return senal_filtrada
    
    def diseñar_filtro_pasabajos(self, fc, orden=None, ventana=None):
        """
        Diseña filtro FIR pasabajos usando método de ventana
        
        h[n] = (ωc/π) · sinc(ωc/π · (n - M/2)) · w[n]
        """
        if orden is None:
            orden = self.config.orden_fir
        if ventana is None:
            ventana = self.config.ventana_fir
            
        nyquist = self.fs / 2
        fc_normalizada = fc / nyquist
        
        # Diseñar filtro
        if ventana == 'hamming':
            taps = signal.firwin(orden, fc_normalizada, window='hamming')
        elif ventana == 'hann':
            taps = signal.firwin(orden, fc_normalizada, window='hann')
        elif ventana == 'blackman':
            taps = signal.firwin(orden, fc_normalizada, window='blackman')
        else:
            taps = signal.firwin(orden, fc_normalizada)
            
        return taps
    
    def aplicar_filtro_pasabajos(self, senal, fc, orden=None):
        """
        Aplica filtro pasabajos FIR a la señal
        """
        taps = self.diseñar_filtro_pasabajos(fc, orden)
        senal_filtrada = signal.convolve(senal, taps, mode='same')
        
        return senal_filtrada
    
    def respuesta_frecuencia_filtro(self, b, a=None, n_points=2000):
        """
        Calcula respuesta en frecuencia de un filtro
        """
        if a is None:  # Filtro FIR
            w, h = signal.freqz(b, worN=n_points, fs=self.fs)
        else:  # Filtro IIR
            w, h = signal.freqz(b, a, worN=n_points, fs=self.fs)
            
        return w, h
    
    def analizar_filtro(self, b, a=None, nombre="Filtro"):
        """
        Análisis completo de un filtro
        """
        w, h = self.respuesta_frecuencia_filtro(b, a)
        
        # Magnitud en dB
        magnitud_db = 20 * np.log10(np.abs(h) + 1e-10)
        
        # Fase en grados
        fase = np.angle(h, deg=True)
        
        # Retardo de grupo si es IIR
        if a is not None:
            w_gd, gd = signal.group_delay((b, a), fs=self.fs)
        else:
            w_gd, gd = w, np.zeros_like(w)
            
        return {
            'frecuencias': w,
            'magnitud': np.abs(h),
            'magnitud_db': magnitud_db,
            'fase': fase,
            'frecuencias_gd': w_gd,
            'retardo_grupo': gd
        }
    
    def calcular_ancho_banda(self, w, h, nivel_db=-3):
        """
        Calcula ancho de banda del filtro a nivel específico en dB
        """
        magnitud_db = 20 * np.log10(np.abs(h) + 1e-10)
        
        # Encontrar frecuencia de corte
        idx = np.where(magnitud_db >= nivel_db)[0]
        if len(idx) > 0:
            return w[idx[-1]] - w[idx[0]]
        return 0