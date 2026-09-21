# Descubrimiento de una Nueva Partícula

Plan de trabajo y tareas del equipo para el desarrollo del proyecto.

## Integrantes

| Nombre | Rol |
|---|---|
|Valderrama| Coordinador |
|Jhon Yepes| Simulación numérica |
|Abiud Villamizar | Análisis de datos |
|Rafael Lemus | Manuscrito |
|Juan Velazques|Con salud gracias a Dios|

## Estructura del repositorio

```
descubrimiento-particula/
├── README.md
├── requirements.txt
├── datos/
│   ├── crudos/
│   └── procesados/
├── codigo/
│   ├── simulacion.py
│   ├── analisis.py
│   └── graficas.py
├── resultados/
│   ├── figuras/
│   └── tablas/
├── manuscrito/
│   ├── articulo.md
│   └── referencias.bib
└── bitacora/
    └── decisiones.md
```

## Cronograma y tareas semanales

### Semana 1 — Planteamiento del problema

- [ ] Redactar la pregunta de investigación en `README.md`.
- [ ] Redactar la hipótesis física.
- [ ] Definir el rango de energía y los parámetros del experimento/simulación.
- [ ] Subir `requirements.txt` con las bibliotecas a usar.
- [ ] Cada integrante crea su rama personal (`simulacion-numerica`, `analisis-datos`, `manuscrito-introduccion`).

**Responsable de revisión:** Coordinador/a.

### Semana 2 — Simulación inicial

- [ ] Desarrollar `codigo/simulacion.py` con la primera versión del modelo.
- [ ] Fijar semillas aleatorias y documentar unidades físicas en el código.
- [ ] Subir datos crudos a `datos/crudos/`.
- [ ] Hacer al menos 3 commits describiendo avances concretos.
- [ ] Abrir Pull Request de la rama `simulacion-numerica` hacia `main`.
- [ ] Etiquetar la versión: `v0.1-primera-simulacion`.

**Responsable de revisión:** integrante de análisis de datos.

### Semana 3 — Procesamiento y análisis preliminar

- [ ] Transformar los datos crudos y guardarlos en `datos/procesados/`.
- [ ] Desarrollar `codigo/analisis.py`.
- [ ] Generar primeras tablas en `resultados/tablas/`.
- [ ] Hacer commits frecuentes con mensajes claros (ej. "Corrige unidades de energía en el análisis").
- [ ] Abrir Pull Request de la rama `analisis-datos`.
- [ ] Etiquetar la versión: `v0.5-analisis-preliminar`.

**Responsable de revisión:** coordinador/a.

### Semana 4 — Visualización de resultados

- [ ] Desarrollar `codigo/graficas.py`.
- [ ] Generar figuras automáticas en `resultados/figuras/`.
- [ ] Revisar que las figuras tengan unidades y leyendas correctas.
- [ ] Hacer commit y push de las figuras finales.
- [ ] Registrar en `bitacora/decisiones.md` los criterios usados para elegir el tipo de gráfica.

**Responsable de revisión:** integrante de simulación numérica.

### Semana 5 — Consolidación de resultados

- [ ] Verificar que `simulacion.py`, `analisis.py` y `graficas.py` se ejecuten sin errores desde cero.
- [ ] Revisar y fusionar todas las ramas pendientes a `main`.
- [ ] Etiquetar la versión: `v1.0-resultados-consolidados`.
- [ ] Hacer una copia de respaldo de los datos grandes fuera de GitHub (repositorio institucional o académico).

**Responsable de revisión:** todo el equipo.

### Semana 6 — Redacción del manuscrito

- [ ] Redactar `manuscrito/articulo.md` con introducción, métodos, resultados y discusión.
- [ ] Completar `manuscrito/referencias.bib`.
- [ ] Insertar las figuras y tablas finales en el manuscrito.
- [ ] Cada integrante revisa una sección distinta mediante Pull Request.

**Responsable de revisión:** coordinador/a.

### Semana 7 — Revisión final y entrega

- [ ] Revisión cruzada completa del manuscrito por todos los integrantes.
- [ ] Corregir observaciones señaladas en los Pull Requests.
- [ ] Verificar reproducibilidad total del proyecto (ejecución desde `requirements.txt` hasta las figuras finales).
- [ ] Etiquetar la versión final: `v2.0-version-final-manuscrito`.
- [ ] Confirmar que existan copias del repositorio en GitHub y localmente en al menos dos equipos distintos.

**Responsable de revisión:** todo el equipo.

## Reglas generales para todas las semanas

- Cada tarea completada requiere un commit con mensaje descriptivo.
- Ningún cambio se sube directamente a `main`: siempre mediante Pull Request revisado por otro integrante.
- Los avances y problemas se registran en `bitacora/decisiones.md`.
- Las entregas semanales se revisan los **viernes**; los Pull Requests deben estar abiertos como máximo el **jueves**.
