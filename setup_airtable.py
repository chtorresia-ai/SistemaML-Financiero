#!/usr/bin/env python3
"""
Script para configurar automáticamente Airtable con los campos requeridos
para SistemaML-Financiero

USO:
    python setup_airtable.py <AIRTABLE_API_KEY> <BASE_ID> <TABLE_ID>
"""

import sys
import requests
from typing import List, Dict

# Campos requeridos en la tabla de Airtable
REQUIRED_FIELDS = [
    {"name": "RazonSocial", "type": "singleLineText"},
    {"name": "Ingresos_Anuales", "type": "number"},
    {"name": "Gastos_Operacionales", "type": "number"},
    {"name": "Activos_Totales", "type": "number"},
    {"name": "Pasivos_Totales", "type": "number"},
    {"name": "Empleados", "type": "number"},
    {"name": "Rentabilidad_Predicha", "type": "number"},
    {"name": "RiesgoFinanciero_Score", "type": "number"},
    {"name": "Clasificacion_Riesgo", "type": "singleLineText"},
]

class AirtableSetup:
    def __init__(self, api_key: str, base_id: str, table_id: str):
        self.api_key = api_key
        self.base_id = base_id
        self.table_id = table_id
        self.base_url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables/{table_id}/fields"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def get_existing_fields(self) -> List[Dict]:
        """Obtiene los campos existentes en la tabla"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            if response.status_code == 200:
                return response.json().get("fields", [])
            else:
                print(f"Error al obtener campos: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error de conexión: {e}")
            return []

    def create_field(self, field_name: str, field_type: str) -> bool:
        """Crea un nuevo campo en la tabla"""
        payload = {
            "name": field_name,
            "type": field_type
        }
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers=self.headers
            )
            if response.status_code in [200, 201]:
                print(f"✓ Campo '{field_name}' creado exitosamente")
                return True
            else:
                print(f"✗ Error al crear '{field_name}': {response.status_code}")
                print(f"  Respuesta: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Error al crear '{field_name}': {e}")
            return False

    def setup(self):
        """Configura todos los campos requeridos"""
        print("🔧 Iniciando configuración de Airtable...\n")
        
        existing_fields = self.get_existing_fields()
        existing_names = {f["name"] for f in existing_fields}
        
        print(f"Campos existentes: {existing_names}\n")
        print("Creando campos faltantes...\n")
        
        created = 0
        for field in REQUIRED_FIELDS:
            if field["name"] not in existing_names:
                if self.create_field(field["name"], field["type"]):
                    created += 1
            else:
                print(f"✓ Campo '{field['name']}' ya existe")
        
        print(f"\n✅ Configuración completada: {created} campos creados")

def main():
    if len(sys.argv) < 4:
        print("\nUSO: python setup_airtable.py <AIRTABLE_API_KEY> <BASE_ID> <TABLE_ID>")
        print("\nEjemplo:")
        print("  python setup_airtable.py patYouApiKey123 appAbcDefGhi123 tblXyzUvw123")
        sys.exit(1)
    
    api_key = sys.argv[1]
    base_id = sys.argv[2]
    table_id = sys.argv[3]
    
    setup = AirtableSetup(api_key, base_id, table_id)
    setup.setup()

if __name__ == "__main__":
    main()
