from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
from sklearn.preprocessing import StandardScaler
import uvicorn

app = FastAPI(
    title="SistemaML Financiero",
    description="API para análisis financiero y scoring de riesgo empresarial",
    version="1.0.0"
)

class EmpresaInput(BaseModel):
    razon_social: str
    ingresos_anuales: float
    gastos_operacionales: float
    activos_totales: float
    pasivos_totales: float
    empleados: int

class EmpresaOutput(BaseModel):
    rentabilidad_predicha: float
    riesgo_financiero_score: float
    clasificacion_riesgo: str
    recomendacion: str

@app.get("/")
def root():
    return {"mensaje": "API SistemaML Financiero activo. Visite /docs para documentación"}

@app.post("/predict", response_model=EmpresaOutput)
def predict(empresa: EmpresaInput):
    try:
        # Validaciones básicas
        if empresa.ingresos_anuales <= 0:
            raise HTTPException(status_code=400, detail="Ingresos deben ser positivos")
        if empresa.activos_totales <= 0:
            raise HTTPException(status_code=400, detail="Activos deben ser positivos")
        
        # Cálculo de ratios financieros
        margen_operacional = (empresa.ingresos_anuales - empresa.gastos_operacionales) / empresa.ingresos_anuales
        roi = (empresa.ingresos_anuales - empresa.gastos_operacionales) / empresa.activos_totales if empresa.activos_totales > 0 else 0
        endeudamiento = empresa.pasivos_totales / empresa.activos_totales if empresa.activos_totales > 0 else 1
        ingresos_por_empleado = empresa.ingresos_anuales / empresa.empleados if empresa.empleados > 0 else 0
        
        # Rentabilidad predicha (0-100)
        rentabilidad = min(100, max(0, (margen_operacional * 50 + roi * 100 + 50)))
        
        # Score de riesgo (0-100, 100=mayor riesgo)
        riesgo_score = min(100, max(0, (endeudamiento * 40 + (1 - margen_operacional) * 30 + 30)))
        
        # Clasificación del riesgo
        if riesgo_score < 30:
            clasificacion = "BAJO"
            recomendacion = "Empresa con perfil de bajo riesgo. Apta para operaciones normales."
        elif riesgo_score < 60:
            clasificacion = "MEDIO"
            recomendacion = "Empresa con riesgo moderado. Monitoreo recomendado."
        else:
            clasificacion = "ALTO"
            recomendacion = "Empresa con alto riesgo financiero. Revisar antes de operaciones."
        
        return EmpresaOutput(
            rentabilidad_predicha=round(rentabilidad, 2),
            riesgo_financiero_score=round(riesgo_score, 2),
            clasificacion_riesgo=clasificacion,
            recomendacion=recomendacion
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
