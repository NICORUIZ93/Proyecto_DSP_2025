"""
Configuración global del proyecto DSP
"""

class Config:
    def __init__(self):
        # Parámetros de audio
        self.fs = 16000  # Frecuencia de muestreo
        self.duracion_grabacion = 3  # segundos
        self.canales = 1  # Mono
        
        # Parámetros preénfasis
        self.alpha_preenfasis = 0.97
        
        # Parámetros filtro notch
        self.r_notch = 0.95  # Radio de polo (0 < r < 1)
        
        # Parámetros filtro pasabajos
        self.orden_fir = 101  # Orden del filtro FIR
        self.ventana_fir = 'hamming'
        
        # Parámetros análisis espectral
        self.ventana_fft = 1024
        self.solape_fft = 512
        self.ventana_spectrogram = 'hann'
        
        # Bandas para análisis de energía
        self.bandas_energia = [0, 250, 500, 1000, 2000, 4000, 8000]
        
        # Parámetros visualización
        self.dpi_figuras = 300
        self.formato_imagen = 'png'
        
        # Rutas
        self.ruta_audio = "datos/audio/"
        self.ruta_resultados = "datos/resultados/"
        self.ruta_figuras = "datos/resultados/figuras/"