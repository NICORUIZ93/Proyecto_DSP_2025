"""
Módulo para captura y manejo de audio
"""

import numpy as np
try:
    import sounddevice as sd
    import soundfile as sf
    import librosa
except ImportError:
    print("⚠️  Módulos de audio no disponibles, usando modo simulado")
    sd = None
    sf = None
    librosa = None
import os
from datetime import datetime

class CapturadorAudio:
    def __init__(self, config):
        self.config = config
        self.fs = config.fs
        self.canales = config.canales
        
    def grabar_audio(self, archivo_salida, duracion=None):
        """
        Graba audio desde el micrófono
        """
        if duracion is None:
            duracion = self.config.duracion_grabacion
            
        print(f"Grabando {duracion}s de audio...")
        
        try:
            # Grabar audio
            audio = sd.rec(
                int(duracion * self.fs),
                samplerate=self.fs,
                channels=self.canales,
                dtype='float32'
            )
            sd.wait()  # Esperar hasta que termine la grabación
            
            # Convertir a array 1D si es estéreo
            audio = audio.flatten()
            
            # Guardar archivo WAV
            sf.write(archivo_salida, audio, self.fs)
            print(f"Audio guardado en: {archivo_salida}")
            
            return audio
            
        except Exception as e:
            print(f"Error grabando audio: {e}")
            # Crear señal de prueba si falla la grabación
            return self.generar_senal_prueba(duracion)
    
    def cargar_audio(self, archivo_entrada):
        """
        Carga archivo de audio existente
        """
        try:
            audio, fs = librosa.load(archivo_entrada, sr=self.fs)
            print(f"Audio cargado: {archivo_entrada}")
            return audio, fs
        except Exception as e:
            print(f"Error cargando audio: {e}")
            # Generar señal de prueba si no existe el archivo
            return self.generar_senal_prueba(3), self.fs
    
    def generar_senal_prueba(self, duracion):
        """
        Genera señal de prueba senoidal con ruido
        """
        t = np.linspace(0, duracion, int(duracion * self.fs))
        
        # Señal senoidal de 440 Hz (LA)
        senal_limpia = 0.5 * np.sin(2 * np.pi * 440 * t)
        
        # Ruido en bajas frecuencias (50 Hz)
        ruido_50hz = 0.1 * np.sin(2 * np.pi * 50 * t)
        
        # Ruido blanco
        ruido_blanco = 0.05 * np.random.randn(len(t))
        
        # Combinar señales
        senal_completa = senal_limpia + ruido_50hz + ruido_blanco
        
        # Aplicar envolvente para simular palabra
        envolvente = np.ones_like(t)
        inicio = int(0.2 * len(t))
        fin = int(0.8 * len(t))
        envolvente[:inicio] = np.linspace(0, 1, inicio)
        envolvente[fin:] = np.linspace(1, 0, len(t) - fin)
        
        senal_completa *= envolvente
        
        print("Generada señal de prueba (440 Hz + ruido 50 Hz + ruido blanco)")
        
        return senal_completa
    
    def listar_archivos_audio(self, directorio):
        """
        Lista archivos de audio en directorio
        """
        extensiones = ['.wav', '.mp3', '.flac']
        archivos = []
        
        for archivo in os.listdir(directorio):
            if any(archivo.lower().endswith(ext) for ext in extensiones):
                archivos.append(os.path.join(directorio, archivo))
                
        return archivos