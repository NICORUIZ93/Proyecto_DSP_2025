#!/usr/bin/env python3
"""
Script principal para el avance del proyecto DSP
Procesamiento Digital de Señales de Voz - Orange Pi 5 Plus

Estudiante: NICOLAS ENRIQUE RUIZ VEGA
Código: 20251583005
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Para uso en Orange Pi sin interfaz gráfica
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime

# Importar módulos personalizados
from config import Config
from captura_audio import CapturadorAudio
from preprocesamiento import Preprocesador
from filtros_digitales import FiltrosDigitales
from analisis_espectral import AnalizadorEspectral
from visualizacion import Visualizador
from comunicacion import ComunicadorMQTT
from utils import verificar_sistema, crear_directorios

def main():
    """Función principal del avance del proyecto"""
    
    print("=== AVANCE PROYECTO DSP - ORANGE PI 5 PLUS ===")
    print(f"Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Verificar sistema
    verificar_sistema()
    
    # Crear directorios necesarios
    crear_directorios()
    
    # Cargar configuración
    config = Config()
    
    # Inicializar módulos
    capturador = CapturadorAudio(config)
    preprocesador = Preprocesador(config)
    filtros = FiltrosDigitales(config)
    analizador = AnalizadorEspectral(config)
    visualizador = Visualizador(config)
    comunicador = ComunicadorMQTT(config)
    
    try:
        # 1. Captura de audio (usar archivo existente o grabar nuevo)
        print("\n1. CAPTURA DE AUDIO")
        archivo_audio = "datos/audio/muestra_avance.wav"
        
        # Si no existe archivo, grabar uno nuevo
        if not os.path.exists(archivo_audio):
            print("Grabando nueva muestra de audio...")
            capturador.grabar_audio(archivo_audio, duracion=3)
        else:
            print("Usando archivo de audio existente...")
        
        # Cargar audio
        senal_original, fs = capturador.cargar_audio(archivo_audio)
        print(f"Duración: {len(senal_original)/fs:.2f}s, Muestras: {len(senal_original)}")
        
        # 2. Preprocesamiento
        print("\n2. PREPROCESAMIENTO")
        senal_preenfasis = preprocesador.aplicar_preenfasis(senal_original)
        
        # 3. Filtrado digital
        print("\n3. FILTRADO DIGITAL")
        senal_notch = filtros.aplicar_filtro_notch(senal_preenfasis, 50)
        senal_filtrada = filtros.aplicar_filtro_pasabajos(senal_notch, 3400)
        
        # 4. Análisis de SNR
        print("\n4. ANÁLISIS DE SNR")
        snr_original = analizador.calcular_snr(senal_original)
        snr_filtrado = analizador.calcular_snr(senal_filtrada)
        
        print(f"SNR original: {snr_original:.2f} dB")
        print(f"SNR filtrado: {snr_filtrado:.2f} dB")
        print(f"Mejora: {snr_filtrado - snr_original:.2f} dB")
        
        # 5. Análisis espectral
        print("\n5. ANÁLISIS ESPECTRAL")
        frecuencias, fft_original = analizador.calcular_fft(senal_original)
        frecuencias, fft_filtrada = analizador.calcular_fft(senal_filtrada)
        
        # Espectrograma
        f, t, espectrograma = analizador.calcular_espectrograma(senal_filtrada)
        
        # Características espectrales
        energias = analizador.calcular_energia_subbandas(fft_filtrada, frecuencias)
        centroide = analizador.calcular_centroide_espectral(fft_filtrada, frecuencias)
        
        print(f"Centroide espectral: {centroide:.2f} Hz")
        print(f"Energías por subbandas: {[f'{e:.2f}' for e in energias]}")
        
        # 6. Visualización
        print("\n6. GENERACIÓN DE VISUALIZACIONES")
        visualizador.graficas_comparativas(
            senal_original, 
            senal_filtrada,
            fft_original,
            fft_filtrada,
            espectrograma, f, t
        )
        
        # 7. Guardar resultados
        print("\n7. GUARDANDO RESULTADOS")
        resultados = {
            'snr_original': snr_original,
            'snr_filtrado': snr_filtrado,
            'mejora_snr': snr_filtrado - snr_original,
            'centroide_espectral': centroide,
            'energias_subbandas': energias,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        analizador.guardar_resultados(resultados, "datos/resultados/resultados_avance.json")

        # 8. Comunicación MQTT
        print("\n8. PUBLICACIÓN DE DATOS VIA MQTT")
        comunicador.publicar_datos(resultados)

        print("\n✅ AVANCE COMPLETADO EXITOSAMENTE")
        print(f"Resultados guardados en: datos/resultados/")
        print("Datos publicados via MQTT")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())