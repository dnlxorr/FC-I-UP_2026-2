descubrimiento-particula/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── .gitignore
│
├── datos/
│   ├── crudos/
│   ├── procesados/
│   └── README.md
│
├── codigo/
│   ├── simulacion.py
│   ├── analisis.py
│   └── graficas.py
│
├── resultados/
│   ├── figuras/
│   └── tablas/
│
├── manuscrito/
│   ├── articulo.md
│   └── referencias.bib
│
└── bitacora/
    └── decisiones.md



Propuesta de Flujo de Trabajo (Workflow) del Equipo
Para garantizar el 100% de reproducibilidad y evitar la pérdida de datos o financiamiento (como en el caso de estudio de Karthik Ram), nuestro equipo implementará el siguiente flujo de trabajo colaborativo sobre la estructura de directorios planteada:

1. Ramas (Branches) para Exploración Segura
Se prohíbe trabajar directamente sobre la rama principal. El repositorio se dividirá de la siguiente manera:

main / develop: Contendrá únicamente código funcional, datos validados y la versión estable del manuscrito.

Ramas de exploración (Features): Para cualquier experimento nuevo, crearemos ramas temporales con nombres descriptivos (ej. analisis-colisiones, ajuste-graficas). Esto nos permite explorar hipótesis sin miedo a dañar el trabajo estable del resto del equipo.

2. Commit Logs como Bitácora de Laboratorio
El historial de Git será nuestro diario de laboratorio oficial. Quedan descartados los mensajes genéricos (como "actualización" o "cambios"). Cada commit debe explicar el por qué del cambio científico:

Formato incorrecto: git commit -m "script modificado"

Formato correcto: git commit -m "Se ajusta la tolerancia de la simulación en simulacion.py a 0.001 para capturar la nueva partícula"

3. Repositorios Remotos (GitHub) a prueba de pérdida de datos
Para asegurar que ninguna falla local en nuestros equipos nos haga perder la investigación, estableceremos la regla del Push Diario. Al finalizar cada sesión de trabajo, todos los avances locales deben sincronizarse con GitHub.
Además, la integración a la rama principal se hará obligatoriamente mediante Pull Requests, requiriendo que al menos un compañero de equipo (por ejemplo, que Daniel o Rafael revisen el código propuesto) apruebe los cambios antes de fusionarlos, garantizando así la calidad y reproducibilidad del experimento.