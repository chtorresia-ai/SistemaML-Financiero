# SistemaML - Análisis Financiero

## 🚀 Descripción Rápida
Sistema de ML en la nube para análisis financiero y scoring de riesgo empresarial. Integración automática entre:
- **Airtable**: Base de datos visual
- **n8n**: Automatización de flujos
- **Render**: Despliegue en la nube

## 📄 Instrucciones de Uso RÁPIDO (5 Minutos)

### Paso 1: Verificar que GitHub está listo ✅
Este repositorio contiene:
- `main.py` - API FastAPI lista para producción
- `requirements.txt` - Todas las dependencias

### Paso 2: Desplegar en Render (1 minuto)
1. Ve a https://render.com/
2. Haz clic en "New +" → "Web Service"
3. Conecta GitHub y selecciona este repositorio
4. Render configurará automáticamente:
   - **Runtime**: Python 3
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. ¡Espera 2 minutos y tendrás una URL pública! (ej: `https://tuservicio.onrender.com`)

### Paso 3: Configurar Airtable (3 minutos)
1. Ve a https://airtable.com/
2. Crea una tabla "Empresas" con estos campos:
   - RazonSocial (Texto)
   - Ingresos_Anuales (Número)
   - Gastos_Operacionales (Número)
   - Activos_Totales (Número)
   - Pasivos_Totales (Número)
   - Empleados (Número)
   - Rentabilidad_Predicha (Número) - SALIDA
   - RiesgoFinanciero_Score (Número) - SALIDA
   - Clasificacion_Riesgo (Texto) - SALIDA

3. Crea un formulario en Airtable para entrada de datos

### Paso 4: Automatizar con n8n (1 minuto)
1. Ve a https://n8n.cloud/
2. Crea un nuevo workflow
3. Agrega estos nodos:
   - **Airtable Trigger**: Cuando se crea un registro
   - **HTTP Request**: POST a `https://TU_URL_RENDER.com/predict`
   - **Airtable Update**: Actualiza el registro con resultados

## 🧮 Qué Hace el Sistema

Para cada empresa, calcula:
- **Rentabilidad Predicha**: 0-100 (mayor = mejor)
- **Riesgo Financiero**: 0-100 (mayor = más riesgo)
- **Clasificación**: BAJO / MEDIO / ALTO

### Fórmulas
- Rentabilidad = (Margen Operacional × 50) + (ROI × 100) + 50
- Riesgo = (Endeudamiento × 40) + (1 - Margen) × 30 + 30

## 📡 API Endpoints

### POST /predict
```json
{
  "razon_social": "Empresa S.A.",
  "ingresos_anuales": 1000000,
  "gastos_operacionales": 600000,
  "activos_totales": 2000000,
  "pasivos_totales": 800000,
  "empleados": 50
}
```

Respuesta:
```json
{
  "rentabilidad_predicha": 75.5,
  "riesgo_financiero_score": 35.2,
  "clasificacion_riesgo": "BAJO",
  "recomendacion": "Empresa con perfil de bajo riesgo..."
}
```

## 🔧 Troubleshooting

**¿La API no responde?**
- Verifica la URL en Render: `https://TU_URL.onrender.com/docs`
- Debe mostrar documentación interactiva

**¿n8n no conecta?**
- Copia la URL exacta de Render
- Verifica el endpoint: `/predict`
- Usa método: POST

## 📊 Siguientes Pasos
- Agregar más ratios financieros
- Integrar datos históricos
- Entrenar modelos ML más avanzados
- Agregar más empresas

---
**Creado para análisis financiero automático ✨**
