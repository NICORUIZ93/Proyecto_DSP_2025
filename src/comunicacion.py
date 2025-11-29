#!/usr/bin/env python3
"""
Módulo de comunicación MQTT para el proyecto DSP
Orange Pi 5 Plus - Procesamiento Digital de Señales
"""

import json
import time
try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("⚠️  Módulo paho-mqtt no disponible, comunicación MQTT deshabilitada")
    mqtt = None
from datetime import datetime

class ComunicadorMQTT:
    """Clase para manejar comunicación MQTT de datos procesados"""

    def __init__(self, config, broker="broker.hivemq.com", port=1883, topic="dsp/proyecto/voz"):
        """Inicializar cliente MQTT"""
        self.config = config
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = None

        # Inicializar cliente
        self.conectar()

    def conectar(self):
        """Conectar al broker MQTT"""
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_publish = self.on_publish
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            print(f"✅ Conectado a MQTT broker: {self.broker}:{self.port}")
        except Exception as e:
            print(f"❌ Error conectando a MQTT: {e}")
            self.client = None

    def on_connect(self, client, userdata, flags, rc):
        """Callback de conexión"""
        if rc == 0:
            print("✅ Conectado exitosamente al broker MQTT")
        else:
            print(f"❌ Fallo de conexión MQTT, código: {rc}")

    def on_publish(self, client, userdata, mid):
        """Callback de publicación"""
        print(f"✅ Mensaje publicado (ID: {mid})")

    def publicar_datos(self, datos):
        """Publicar datos procesados via MQTT"""
        if self.client is None:
            print("❌ Cliente MQTT no conectado")
            return False

        try:
            # Preparar mensaje JSON
            mensaje = {
                "timestamp": datetime.now().isoformat(),
                "tipo": "datos_espectrales",
                "datos": datos
            }

            payload = json.dumps(mensaje)

            # Publicar
            result = self.client.publish(self.topic, payload, qos=1)
            result.wait_for_publish()

            print(f"✅ Datos publicados en topic '{self.topic}': {datos}")
            return True

        except Exception as e:
            print(f"❌ Error publicando datos: {e}")
            return False

    def publicar_evento(self, evento, valor=None):
        """Publicar un evento específico"""
        datos_evento = {
            "evento": evento,
            "valor": valor,
            "timestamp": datetime.now().isoformat()
        }
        return self.publicar_datos(datos_evento)

    def desconectar(self):
        """Desconectar del broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            print("✅ Desconectado de MQTT broker")