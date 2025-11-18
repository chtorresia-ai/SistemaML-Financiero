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


## 🧪 Pruebas de la API

### Ejecutar pruebas localmente

```bash
# Asegúrate de que el servidor esté corriendo en otra terminal
python main.py

# En otra terminal, ejecuta las pruebas
python test_api.py
```

### Pruebas disponibles

1. **Health Check**: Verifica que el servidor esté activo
2. **Root Endpoint**: Confirma disponibilidad de documentación
3. **Predict válido**: Prueba predicción con datos correctos
4. **Validación de ingresos**: Rechaza valores negativos
5. **Validación de activos**: Rechaza valores inválidos
6. **Múltiples empresas**: Prueba con diferentes ratios financieros

## 🔧 Configuración de Airtable

### Método automático (Recomendado)

```bash
python setup_airtable.py <TU_API_KEY> <BASE_ID> <TABLE_ID>
```

**Cómo obtener tus credenciales:**

1. Ve a [Airtable Account](https://airtable.com/account)
2. Copia tu **Personal access token**
3. En tu base, copia la **BASE_ID** de la URL: `airtable.com/base/<BASE_ID>`
4. En tu tabla, obtén el **TABLE_ID** desde la API documentation

### Campos creados automáticamente

- ✅ RazonSocial (Texto)
- ✅ Ingresos_Anuales (Número)
- ✅ Gastos_Operacionales (Número)
- ✅ Activos_Totales (Número)
- ✅ Pasivos_Totales (Número)
- ✅ Empleados (Número)
- ✅ Rentabilidad_Predicha (Número - Salida)
- ✅ RiesgoFinanciero_Score (Número - Salida)
- ✅ Clasificacion_Riesgo (Texto - Salida)

## 🚀 Despliegue en Producción

### Render.com (Opción recomendada)

1. **Conectar repositorio:**
   - Ve a [Render Dashboard](https://dashboard.render.com)
   - Crea un nuevo "Web Service"
   - Conecta tu GitHub
   - Selecciona este repositorio

2. **Configurar automáticamente:**
   - **Environment:** Python 3
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn main:app`

3. **Variables de entorno (Opcional):**
   - `LOG_LEVEL`: DEBUG | INFO | WARNING | ERROR

4. **Tu API estará en:** `https://tu-app.onrender.com`

### Heroku (Alternativa)

```bash
heroku login
heroku create tu-app
git push heroku main
```

## 📊 Dashboard n8n

### Workflow de Automatización

**Entrada:** Airtable (Tabla: Empresas)

**Lógica:**
1. Trigger cuando se crea registro
2. Mapear campos a JSON
3. POST a `/predict`
4. Actualizar Airtable con resultados

**Salida:** Campos de predicción en Airtable

## 📈 Escalabilidad

**Para producción:**

- ✅ Usar base de datos PostgreSQL
- ✅ Implementar Redis para caché
- ✅ Agregar autenticación JWT
- ✅ Rate limiting en endpoints
- ✅ Logging y monitoreo
- ✅ CI/CD con GitHub Actions

## 📝 Estructura del Proyecto

```
SistemaML-Financiero/
├── main.py              # API FastAPI principal
├── setup_airtable.py    # Script de configuración
├── test_api.py          # Suite de pruebas
├── requirements.txt     # Dependencias Python
├── README.md            # Este archivo
└── .gitignore           # Archivos ignorados
```

## 🤝 Contribuciones

Las pull requests son bienvenidas. Para cambios mayores:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la MIT License.

## 📞 Soporte

¿Preguntas? Abre un Issue en GitHub.

---

**Última actualización:** Noviembre 2025
**Estado:** ✅ 100% Funcional - Listo para Producción
