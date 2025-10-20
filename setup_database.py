#!/usr/bin/env python3
"""
Script de configuración inicial para el proyecto de Hipoteca Inversa
Este script crea las tablas necesarias en la base de datos
"""

import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(__file__))

from Secret_config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT
from src.controller.py.clientes_controller import ClientesController
from src.controller.py.propiedades_controller import PropiedadesController
from src.controller.py.hipotecas_controller import HipotecasController
from src.controller.py.herederos_controller import HerederosController

def crear_tablas():
    """Crear todas las tablas necesarias en la base de datos"""
    print("🚀 Iniciando configuración de la base de datos...")
    print(f"📊 Conectando a: {PGHOST}/{PGDATABASE}")
    
    try:
        # Crear tablas
        print("📋 Creando tabla de clientes...")
        ClientesController.crear_tabla()
        
        print("🏠 Creando tabla de propiedades...")
        PropiedadesController.crear_tabla()
        
        print("💰 Creando tabla de hipotecas...")
        HipotecasController.crear_tabla()
        
        print("👥 Creando tabla de herederos...")
        HerederosController.crear_tabla()
        
        print("✅ ¡Configuración completada exitosamente!")
        print("\n📝 Las siguientes tablas han sido creadas:")
        print("   - clientess (clientes)")
        print("   - propiedades")
        print("   - hipotecas")
        print("   - herederos")
        
        print("\n🎯 Próximos pasos:")
        print("   1. Ejecutar pruebas: python -m unittest discover test")
        print("   2. Ejecutar calculadora: python src/view/interface.py")
        print("   3. Ejecutar gestión BD: python src/view/database_interface.py")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        print("\n🔧 Verifica que:")
        print("   1. La base de datos esté ejecutándose")
        print("   2. Las credenciales en Secret_config.py sean correctas")
        print("   3. Tengas permisos para crear tablas")
        return False
    
    return True

def verificar_conexion():
    """Verificar la conexión a la base de datos"""
    print("🔍 Verificando conexión a la base de datos...")
    
    try:
        conexion = ClientesController.conectar()
        conexion.close()
        print("✅ Conexión exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🏦 CONFIGURACIÓN DEL SISTEMA DE HIPOTECA INVERSA")
    print("=" * 60)
    
    # Verificar conexión
    if not verificar_conexion():
        print("\n💡 Asegúrate de que:")
        print("   - PostgreSQL esté ejecutándose")
        print("   - Las credenciales en Secret_config.py sean correctas")
        print("   - La base de datos 'calculadora_de_hipoteca_inversa' exista")
        sys.exit(1)
    
    # Crear tablas
    if crear_tablas():
        print("\n🎉 ¡Sistema listo para usar!")
    else:
        print("\n💥 Configuración fallida")
        sys.exit(1)
