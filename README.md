# Proyecto DSP - Procesamiento Digital de Señales de Voz

**Orange Pi 5 Plus - Universidad Distrital Francisco José de Caldas**

**Estudiante:** NICOLAS ENRIQUE RUIZ VEGA
**Código:** 20251583005
**Curso:** Procesamiento Digital de Señales I
**Profesor:** Dr. Jorge Andrés Puerto Acosta

## 📋 Descripción

Sistema completo de procesamiento digital de señales para voz que implementa captura, filtrado, análisis espectral y transmisión digital según las especificaciones del proyecto final DSP I.

## 🏗️ Arquitectura del Sistema

```
├── config.py              # Configuración del sistema
├── captura_audio.py       # Captura y manejo de audio
├── preprocesamiento.py    # Filtro de preénfasis
├── filtros_digitales.py   # Filtros notch y paso-bajo
├── analisis_espectral.py  # FFT, STFT, características espectrales
├── visualizacion.py       # Generación de gráficos
├── comunicacion.py        # Cliente MQTT
├── utils.py              # Utilidades del sistema
└── main_avance.py        # Script principal del avance
```

## 🚀 Instalación y Ejecución

### En Orange Pi 5 Plus:

```bash
# Clonar o copiar proyecto
cd /home/orangepi/Proyecto_DSP_2025

# Instalar dependencias
pip3 install -r requirements.txt

# Ejecutar verificación del sistema
python3 -c "from utils import verificar_dependencias; verificar_dependencias()"

# Ejecutar el avance
python3 main_avance.py
```

### Dependencias Requeridas:
- Python 3.8+
- numpy
- scipy
- matplotlib
- sounddevice
- paho-mqtt
- portaudio (para audio)

## 📊 Funcionalidades Implementadas

### ✅ Entrega Parcial (29 Noviembre)
- [x] Captura de señales de voz
- [x] Preprocesamiento: filtro de preénfasis
- [x] Filtrado digital: notch 50/60 Hz + paso-bajo 3.4 kHz
- [x] Análisis de SNR antes/después
- [x] FFT y análisis espectral básico
- [x] Visualizaciones: señales, espectros, espectrogramas
- [x] Comunicación MQTT para transmisión de datos

### 🔄 Pipeline de Procesamiento
1. **Captura**: Audio WAV a 16 kHz
2. **Preénfasis**: y[n] = x[n] - α·x[n-1] (α=0.97)
3. **Filtrado Notch**: Eliminación de ruido 50/60 Hz
4. **Filtrado LPF**: Corte en 3.4 kHz (ventana Hamming)
5. **Análisis Espectral**: FFT, STFT, energías, centroide
6. **Visualización**: Gráficos automáticos guardados
7. **Transmisión**: Datos via MQTT (broker.hivemq.com)

## 📁 Estructura de Directorios

```
/Proyecto_DSP_2025/
├── datos/
│   ├── audio/           # Archivos WAV grabados
│   └── resultados/      # JSON con métricas
├── graficas/            # PNG generados automáticamente
├── logs/               # Logs del sistema
├── requirements.txt    # Dependencias Python
└── README.md          # Esta documentación
```

## 📈 Resultados Esperados

- **SNR Mejorado**: ~3-5 dB de mejora con filtrado
- **Centroide Espectral**: ~2-4 kHz para voz masculina
- **Visualizaciones**: 3 gráficos por ejecución
- **MQTT**: Publicación automática de métricas

## 🎯 Próximos Pasos (Entrega Final)

- [ ] Implementación GPIO en Orange Pi
- [ ] Demo funcional con LED
- [ ] Informe completo (10-15 páginas)
- [ ] Presentación Beamer
- [ ] Comunicación RS232 alternativa

```bash
python3 -c "from utils import verificar_sistema; verificar_sistema()"
```

---

**Desarrollado por:** NICOLAS ENRIQUE RUIZ VEGA (20251583005)
**Fecha:** Noviembre 2025
**Versión:** 1.0.0