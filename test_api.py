#!/usr/bin/env python3
"""
Pruebas automatizadas para la API SistemaML-Financiero

USO:
    pytest test_api.py  -v
    o
    python -m pytest test_api.py -v
"""

import requests
import json
from typing import Dict

# Configuración
BASE_URL = "http://localhost:8000"
TEST_EMPRESA_DATA = {
    "razon_social": "Empresa Test S.A.",
    "ingresos_anuales": 1000000,
    "gastos_operacionales": 600000,
    "activos_totales": 2000000,
    "pasivos_totales": 800000,
    "empleados": 50
}

class TestSistemaMLAPI:
    """
Pruebas para la API del Sistema ML de Análisis Financiero
    """

    def test_health_endpoint(self):
        """Prueba que el endpoint /health responde correctamente"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✅ Health check passed")

    def test_root_endpoint(self):
        """Prueba que el endpoint / responde con mensaje correcto"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert "SistemaML" in response.json()["mensaje"]
        print("✅ Root endpoint passed")

    def test_predict_with_valid_data(self):
        """Prueba /predict con datos válidos"""
        response = requests.post(
            f"{BASE_URL}/predict",
            json=TEST_EMPRESA_DATA
        )
        assert response.status_code == 200
        data = response.json()
        
        # Validaciones
        assert "rentabilidad_predicha" in data
        assert "riesgo_financiero_score" in data
        assert "clasificacion_riesgo" in data
        assert "recomendacion" in data
        
        # Rango de valores
        assert 0 <= data["rentabilidad_predicha"] <= 100
        assert 0 <= data["riesgo_financiero_score"] <= 100
        assert data["clasificacion_riesgo"] in ["BAJO", "MEDIO", "ALTO"]
        
        print("✅ Predict with valid data passed")
        print(f"  Rentabilidad: {data['rentabilidad_predicha']}")
        print(f"  Riesgo: {data['riesgo_financiero_score']}")
        print(f"  Clasificación: {data['clasificacion_riesgo']}")

    def test_predict_with_invalid_negative_ingresos(self):
        """Prueba /predict rechaza ingresos negativos"""
        invalid_data = TEST_EMPRESA_DATA.copy()
        invalid_data["ingresos_anuales"] = -1000
        
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_data
        )
        assert response.status_code == 400
        print("✅ Negative ingresos validation passed")

    def test_predict_with_invalid_activos(self):
        """Prueba /predict rechaza activos invalidos"""
        invalid_data = TEST_EMPRESA_DATA.copy()
        invalid_data["activos_totales"] = -1000
        
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_data
        )
        assert response.status_code == 400
        print("✅ Negative activos validation passed")

    def test_predict_multiple_empresas(self):
        """Prueba con múltiples empresas con diferentes ratios"""
        test_cases = [
            # Empresa rentable con bajo riesgo
            {
                "razon_social": "Empresa Exitosa",
                "ingresos_anuales": 2000000,
                "gastos_operacionales": 500000,
                "activos_totales": 3000000,
                "pasivos_totales": 500000,
                "empleados": 100
            },
            # Empresa con riesgo moderado
            {
                "razon_social": "Empresa Moderada",
                "ingresos_anuales": 1000000,
                "gastos_operacionales": 800000,
                "activos_totales": 1500000,
                "pasivos_totales": 1000000,
                "empleados": 50
            },
            # Empresa con alto riesgo
            {
                "razon_social": "Empresa Riesgosa",
                "ingresos_anuales": 500000,
                "gastos_operacionales": 450000,
                "activos_totales": 800000,
                "pasivos_totales": 700000,
                "empleados": 20
            }
        ]
        
        for empresa in test_cases:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=empresa
            )
            assert response.status_code == 200
            data = response.json()
            print(f"✅ {empresa['razon_social']}: {data['clasificacion_riesgo']}")

def run_manual_tests():
    """Ejecuta las pruebas manualmente"""
    print("\n🔍 Iniciando pruebas manuales de la API...\n")
    
    test_suite = TestSistemaMLAPI()
    
    try:
        print("1. Probando endpoint /health")
        test_suite.test_health_endpoint()
        print()
        
        print("2. Probando endpoint /")
        test_suite.test_root_endpoint()
        print()
        
        print("3. Probando /predict con datos válidos")
        test_suite.test_predict_with_valid_data()
        print()
        
        print("4. Probando validación de ingresos negativos")
        test_suite.test_predict_with_invalid_negative_ingresos()
        print()
        
        print("5. Probando validación de activos negativos")
        test_suite.test_predict_with_invalid_activos()
        print()
        
        print("6. Probando múltiples empresas")
        test_suite.test_predict_multiple_empresas()
        print()
        
        print("\n✅ ¡Todas las pruebas pasaron correctamente!\n")
        
    except AssertionError as e:
        print(f"\n✗ Error en prueba: {e}\n")
    except requests.exceptions.ConnectionError:
        print(f"\n✗ No se puede conectar a {BASE_URL}")
        print("  Asegúrate de que el servidor esté corriendo: python main.py\n")

if __name__ == "__main__":
    run_manual_tests()
